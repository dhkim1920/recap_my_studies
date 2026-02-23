# zram

## zram이란?
- zram은 RAM을 압축해서 블록 디바이스(`/dev/zram0` 등)로 제공하는 커널 기능이다.
- 여기에 swap을 올리면 zram swap이 된다. 
  - 참고) k8s에서 zram도 일반 swap과 동일하게 취급되므로 주의

## zram(및 zram swap) 켜져 있는지 확인
```bash
# swap으로 zram이 올라가 있는지
swapon --show

# /proc/swaps에서 zram 확인
cat /proc/swaps

# zram 디바이스 존재 여부
ls -l /dev/zram*
```
- `swapon --show` 또는 `/proc/swaps`에 `/dev/zram0`가 있으면 zram swap이 켜진 상태이다.

## zram swap 끄기(즉시)

```bash
# zram swap만 끄기
sudo swapoff /dev/zram0

# 여러 개면 전체 끄기
sudo swapoff -a
```

## zram swap 켜기(즉시)
- zram 디바이스가 이미 있고 swap 서명이 있으면
```bash
sudo mkswap /dev/zram0
sudo swapon /dev/zram0
```

## 재부팅 후 자동으로 켜지는 zram 끄기(영구)
- 어떤 서비스가 켜는지부터 확인
```bash
systemctl list-unit-files | grep -i zram
systemctl list-units | grep -i zram
```

- 자주 쓰는 유닛 비활성화(존재하는 것만 적용)
```bash
sudo systemctl disable --now systemd-zram-setup@zram0 2>/dev/null || true
sudo systemctl disable --now zramswap.service 2>/dev/null || true
sudo systemctl disable --now zram-generator-defaults 2>/dev/null || true
```

- 적용 확인
```bash
swapon --show
```
