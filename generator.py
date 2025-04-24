import os


def generate_readme(root_path=".", entry_exclude=None):
    if entry_exclude is None:
        entry_exclude = []

    readme_path = os.path.join(root_path, "README.md")
    contents = ["# 문서 목록\n"]

    for entry in sorted(os.listdir(root_path)):
        full_path = os.path.join(root_path, entry)
        if os.path.isdir(full_path) and entry not in entry_exclude:
            contents.append(f"## {entry}\n")

            md_files = [f for f in sorted(os.listdir(full_path)) if f.endswith(".md")]
            for md_file in md_files:
                rel_path = os.path.join(entry, md_file)
                contents.append(f"- [{md_file}]({rel_path})")
            contents.append("")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(contents))


if __name__ == "__main__":
    exclude_list = [".idea", "venv", ".git", "__pycache__"]
    generate_readme(entry_exclude=exclude_list)
