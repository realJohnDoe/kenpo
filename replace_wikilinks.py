import os
import re


def replace_wikilink_with_header(source_file, file_paths):
    def replace(match):
        target_file = match.group(1)
        print(f"Replacing wikilink targeting {target_file}.")
        target_file_path_candidates = [
            f for f in file_paths if f.endswith(target_file + ".md")
        ]
        if not target_file_path_candidates:
            print("Did not find a matching file")
            return f"[[{target_file}]]"

        target_file_path = target_file_path_candidates[0]
        print(f"Found target file under {target_file_path}")
        with open(target_file_path, "r") as f:
            target_content = f.read()
            header_match = re.search(r"^# ([^#].+)$", target_content, re.MULTILINE)
            if header_match:
                title = header_match.group(1)
                print(f"Found header {title}")
                relative_path = os.path.relpath(
                    target_file_path, start=os.path.dirname(source_file)
                ).replace("\\", "/")
                print(f"Calculated relative target path: {relative_path}")
                return f"[{title}]({relative_path})"
            else:
                print("Found no header. Using the file name instead.")
                return f"[[{target_file}]]"

    return replace


def replace_wikilinks(file_paths):
    for source_file in file_paths:
        print(f"Replacing wikilinks in: {source_file}")
        with open(source_file, "r") as file:
            content = file.read()

        # Replace wikilinks with markdown links
        content = re.sub(
            r"\[\[(.*?)\]\]",
            replace_wikilink_with_header(source_file, file_paths),
            content,
        )

        with open(source_file, "w") as file:
            file.write(content)


# Replace wikilinks in all markdown files in a directory
def replace_all_wikilinks(directory):
    md_files = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(subdir, file)
                md_files.append(file_path)
    replace_wikilinks(md_files)


# Example usage
target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "docs"))
print(target_dir)
replace_all_wikilinks(target_dir)
