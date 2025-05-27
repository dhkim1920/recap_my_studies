import os


def generate_readme(root_path=".", entry_exclude=[]):
    readme_path = os.path.join(root_path, "README.md")
    contents = ["# 문서 목록\n"]

    def walk_md_files(current_path, depth=0):
        entries = sorted(os.listdir(current_path))
        for entry in entries:
            full_path = os.path.join(current_path, entry)
            rel_path = os.path.relpath(full_path, root_path).replace("\\", "/")

            if os.path.isdir(full_path):
                if entry not in entry_exclude:
                    contents.append(f"## {rel_path}\n")
                    walk_md_files(full_path, depth + 1)
            elif entry.endswith(".md") and entry != "README.md":
                contents.append(f"- [{entry}]({rel_path})")

    walk_md_files(root_path)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(contents))


if __name__ == "__main__":
    exclude_list = [".idea", "venv", ".git", "__pycache__", "image", "images"]
    generate_readme(entry_exclude=exclude_list)
