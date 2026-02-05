# Amazon EMR HBase 그레이스풀 스케일링 구현하기

> 해당 문서는 아래 링크를 요약한 내용입니다. 자세한 내용은 아래 링크 참고 바랍니다.
> https://aws.amazon.com/ko/blogs/big-data/implement-amazon-emr-hbase-graceful-scaling/

## 개요
EMR HBase 클러스터를 운영 할 때 scale-in 또는 scale-out을 할 수 있다. (예를 들어, 단기적인 병렬 연산을 위해)  
이 때 EMR Task Node에서 HBase region server를 실행하게 되는데 스팟 인스턴스가 중단되면 region server도 예기치 않게 종료될 수 있다.

WAL를 활성화하지 않은 HBase는 region server의 예기치 않은 종료 때문에 서버 복구 중 WAL split을 유발하게 되고 이는 부하를 가져온다.
또한 Table의 일관성을 깨뜨릴 수도 있다. 
때문에 HBase를 graceful 하게 스케일링하는 해야하며, 여기서는 region server를 정상 종료하는 방법을 다룬다.
(테스트는 7.3.0, 6.15.0, 5.36.2 버전에서 이루어졌으니 참고)

## 솔루션 개요
- 스크립트를 통해 Region들을 자동으로 이동
  - HBase의 내장 스크립트 graceful_stop.sh 실행 (graceful scaling in)
  - region을 다른 region server로 이동시켜, 노드를 decommission할 때 WAL splits을 방지할 수 있다. (이동은 HDFS web에서 볼수 있다.)
- decommission 우선 순위 상승 설정
- region server들을 정상적으로 decommission
- EMR **설정**을 통해 **task node에 region server가 프로비저닝되지 않도록 방지** 
  - 클러스터를 시작할 때 인스턴스 그룹 별로 software configurations를 설정한다. 
- EMR **Steps**를 통해 task node에 region server가 프로비저닝되지 않도록 방지
  - 기존 클러스터의 경우, task node에서 HBase region server를 종료하는 Step을 사용한다. 
  - 또는 태스크 인스턴스 그룹의 HBase storage `rootdir`를 재구성한다. (storage에 관여하지 않도록 설정을 변경하는거 같은데 이건 잘 모르겠음)

## 솔루션
실행 중인 EMR 클러스터에서, modify-instance-groups 명령어와 EC2InstanceIdsToTerminate를 사용하여 종료 할수 있다.
```bash
aws emr modify-instance-groups \
  --instance-groups InstanceGroupId=ig-xxxxx,EC2InstanceIdsToTerminate=i-1234567890abcdef0,i-0987654321fedcba0
```
이런식으로 지정하여 즉시 종료하게 되면 복제본이 사라질 수 도 있고 예기치 않은 이슈가 발생할 수 있다.

이를 해결하기 위해서는 오히려 instacne id를 지정하지 않고 instance 수만 명시하여 modify-instance-groups를 사용하자.
이럴 경우 EMR은 graceful하게 decommission을 한다.

그러나 주의 할점은 EMR에서 HBase에 대한 graceful은 지원하지 않는 다는 것이다. (YARN, HDFS은 지원)
따라서 아래의 두가지 방법을 통해 해결해보자.
- 방법 1: 해제 우선 순위 조정
- 방법 2: Region 수동 이동 (노드 종료 전에)

### 방법 1: 크기 조정을 통한 HBase 리전 서버 해제
EMR에서 코어 노드의 해제 우선순위를 높이는 가장 쉬운 방법 중 하나는 인스턴스 컨트롤러 heartbeat을 줄이는 것이다.
- blog_HBase_graceful_decommission.sh의 move_regions를 EMR step으로 설정한다. 
   - Region을 다른 region server로 이동하고 region server와 인스턴스 컨트롤러의 프로세스를 종료시킴 
   - 파라미터로 대상 region server인 targetRS와 S3Path도 제공해야 한다. 
     - targetRS: 해제 대상 리전 서버의 프라이빗 DNS
     - S3Path: Region 마이그레이션 스크립트의 위치
   - 이 step은 region의 이동이 발생하므로 피크 시간이 아닐 때 하자
   - 해당 스크립트는 ssh 자격 증명을 통한 노드 액세스를 한다. **role** 확인 잘할 것~

> 상기 스크립트는 링크 참고) https://aws-blogs-artifacts-public.s3.us-east-1.amazonaws.com/artifacts/BDB-2672/blog_HBase_graceful_decommission.sh

참고)
EMR 5.x에서 **마스터 노드가 hbase:meta 리전을 호스팅하는 리전 서버 역할도 수행**한다.
따라서 일반 리전을 마스터 노드로 이동하려고 하면 스크립트가 멈춰버린다. 이 때는 maxthreads 매개변수를 증가 시키자, 이것도 안될 수 있다. ???
- 이게 s3 기반 저장 구조를 가지면서 hdfs와 패턴이 달라서 이렇게 되었다는데 좀 이상하다.

아래는 blog_HBase_graceful_decommission.sh를 EMR step로 사용하여 move_regions 함수를 호출하는 스크립트 사용 예시다.
### Step 구성
```
Step 타입: Custom JAR
이름: Move HRegions
JAR 위치: s3://<region>.elasticmapreduce/libs/script-runner/script-runner.jar
Main class: 없음
arguments:s3://yourbucket/your/step/location/blog_HBase_graceful_decommission.sh move_regions <your-secret-id> <targetRS: target_region_server_private_DNS> <S3Path: S3 location>
Action on failure:Continue
```

### 실행 예시
```
Step 타입: Custom JAR
이름: Move HRegions
JAR 위치: s3://us-west-2.elasticmapreduce/libs/script-runner/script-runner.jar
Main class: None
Arguments: s3://yourbucket/your/step/location/blog_HBase_graceful_decommission.sh your-secret-id stop_and_check_task_rs ig-ABCDEFGH12345 s3://yourbucket/yourpath/
Action on failure:Continue
```

웹 UI에서는  region 이동 후 해당 대상 Region Server에 region이 0개인 것을 볼 수 있다.
이제 region이 0개 인것을 확인 했으니 stop_RS_IC 함수가 decommission 대상 노드에서 HBase RegionServer 및 instance controller 프로세스를 중단한다.

#### 주의사항:
- 이 스크립트는 Amazon EMR 5.30.0 이상 버전에서 사용 가능하다. (5.x 미만 요즘에 잘 안쓰니 큰 문제는 없을거 같다.)

이 스텝이 성공적으로 완료된 후, **EMR 콘솔에서 scale-in**을 수행하고, 노드를 줄여보자!
EMR이 실제 instance controller의 heartbeat 손실을 감지하기까지는 몇 분 정도 지연될 수 있으니 기다려야한다. 
웃긴건 사실 이래도 decommission 우선순위를 높인 것일 뿐 실제로 대상이 된다고 보장할 수 는 없다.
이 때는 방법 2로 넘어가자!

### 방법 2: 대상 코어 노드를 수동으로 decommission
modify-instance-groups의 EC2InstanceIdsToTerminate 옵션을 사용하여 해당 노드를 종료할 수 있다. 
앞서 말했지만 hdfs block 이슈나 hbase splitting 이슈가 발생 할 수 있다. 따라서 피크 시간이 아닐 때 하자! (점검 때나 하라는 소리)
1. blog_HBase_graceful_decommission.sh를 EMR Step으로 실행하여 move_hregions 함수를 수행하자
2. 그다음 통일 스크립트에서 terminate_ec2 함수를 EMR Step으로 실행하자 
   - 대상 인스턴스 그룹 ID와 종료할 인스턴스 ID를 스크립트에 전달해야 한다.
   - 이 함수는 modify-instance-groups의 EC2InstanceIdsToTerminate 옵션을 통해 한 번에 하나의 노드만 종료 시킨다. (연속 종료 방지)
   - 이 함수는 block 복제본을 체크하며 진행한다. 
     - hdfs dfs admin -report를 수행하여 under-replicating, corrupted, missing 확인 및 복구 
     - 이 때도 role 확인 잘하자, elasticmapreduce:ModifyInstanceGroups 있어야 함

### terminate_ec2 함수를 EMR Step에서 호출하는 구문
```
Step 타입: Custom JAR
이름: Terminate EC2
JAR 위치: s3://<region>.elasticmapreduce/libs/script-runner/script-runner.jar
Main class: 없음
Arguments:s3://yourbucket/your/step/location/blog_HBase_graceful_decommission.sh terminate_ec2 <your-secret-id> <instance_groupID> <target_EC2_Instance_ID>
실패 시 동작: Continue
```
### 예시
```
Step 타입: Custom JAR
이름: Terminate EC2
JAR 위치: s3://us-west-2.elasticmapreduce/libs/script-runner/script-runner.jar
Arguments: s3://yourbucket/your/step/location/blog_HBase_graceful_decommission.sh terminate_ec2 your-secret-id ig-ABCDEFGH12345 i-1234567890abcdef
실패 시 동작: Continue
```
HDFS decommission 진행 상황은 name node ui Overview에서 볼 수 있다. 
Datanodes 페이지에서 decommission 대상 노드는 초록색 체크 표시가 없으며, Decommissioning 섹션에 표시되니 참고

## EMR task node에 HBase RegionServer를 배치하지 않도록 방지하는 방법
신규 클러스터에서는 EMR HBase 클러스터를 시작할 때, 마스터와 코어 그룹에만 HBase 설정을 구성하고, task node에는 설정을 비워둔다. 
이렇게 하면 task node에 HBase Region Server가 배치되지 않습니다.

### 예시:
마스터 및 코어 인스턴스 그룹에서 HBase 설정은 다음과 같음:
```json
[
    {
        "Classification": "hbase",
        "Properties": {
            "hbase.emr.storageMode": "s3"
         }
    },
    {
        "Classification": "hbase-site",
        "Properties": {
            "hbase.rootdir": "s3://my/HBase/on/S3/RootDir/"
        }
    }
]
```

태스크 인스턴스 그룹에는 HBase 설정이 전혀 없음:
```json
[]
```

## task node에서 HBase Region Server 배포 중지하기
기존 EMR HBase 클러스터에서, blog_HBase_graceful_decommission.sh의 stop_and_check_task_rs 인자를 전달하여 EMR Step으로 실행하면,
태스크 인스턴스 그룹 내 노드에서 HBase Region Server를 중지할 수 있다.
이 스크립트는 태스크 인스턴스 그룹 ID와 task node에 공유할 스크립트를 저장할 S3 경로가 필요하다.

### stop_and_check_task_rs를 호출하는 EMR Step 구문
```
Step 타입: Custom JAR
이름: Stop HBase Region servers on Task Nodes
JAR 위치: s3://<region>.elasticmapreduce/libs/script-runner/script-runner.jar
Arguments:s3://yourbucket/your/step/location/blog_HBase_graceful_decommission.sh stop_and_check_task_rs <your-secret-id> <instance_groupID> <S3 경로>
실패 시 동작: Continue
```
### 실행 예시
```
Step type: Custom JAR
Name: Stop Hbase Region servers on Task Nodes
JAR location :s3://us-west-2.elasticmapreduce/libs/script-runner/script-runner.jar
Main class :None
Arguments :s3://yourbucket/your/step/location/ blog_HBase_graceful_decommission.sh your-secret-id stop_and_check_task_rs ig-ABCDEFGH12345 s3://yourbucket/yourpath/
Action on failure:Continue
```

위 Step은 단순히 기존 task node에서 HBase Region Server를 중지하는 것뿐만 아니라, 새로운 task node가 이후 HBase Regio nServer를 실행하지 않도록 하기 위해 인스턴스 그룹도 재구성 및 scale-in한다.

### 상세 절차
1. blog_HBase_graceful_decommission.sh의 move_regions 함수를 사용하여, 태스크 그룹 내의 Regions를 다른 노드로 이동시키고, 해당 노드의 RegionServer를 중지
2. 해당 task node에서 Region Server가 정상적으로 중지되었는지 확인한 후, 스크립트는 해당 태스크 인스턴스 그룹을 reconfigure
3. 이때의 hbase.rootdir을 존재하지 않는 위치로 지정하여, 해당 그룹에서 HBase가 제대로 동작하지 않도록 설정
### 설정 예시
```json
[
    {
        "Classification": "hbase-site",
        "Properties": {
            "hbase.rootdir": "hdfs://non/existing/location"
        }
    },
    {
        "Classification": "hbase",
        "Properties": {
            "hbase.emr.storageMode": "hdfs"
        }
    }
]
```
4. 태스크 인스턴스 그룹의 상태가 다시 RUNNING으로 전환되면, 스크립트는 이 태스크 그룹의 인스턴스 수를 0으로 scale-in
5. 이후의 자동 스케일 아웃 이벤트에서 새롭게 추가되는 task node들은 더 이상 HBase Region Server를 실행하지 않게 됨

## 결론
HBase graceful 지원 안하므로 써야한다.

## 참고
7.x에도 아직 미지원인 듯