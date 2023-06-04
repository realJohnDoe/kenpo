import os
import re


def replace_wikilinks(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    # Replace wikilinks with markdown links
    content = re.sub(r"\[\[(.*?)\]\]", replace_wikilink_with_header(file_path), content)

    with open(file_path, "w") as file:
        file.write(content)


def replace_wikilink_with_header(file_path):
    def replace(match):
        target_file = match.group(1)
        target_file_path = os.path.join(os.path.dirname(file_path), target_file + ".md")
        with open(target_file_path, "r") as target_file:
            target_content = target_file.read()
            header_match = re.search(r"^#+ (.+)$", target_content, re.MULTILINE)
            if header_match:
                return header_match.group(1)
            else:
                return target_file

    return replace


# Replace wikilinks in all markdown files in a directory
def replace_all_wikilinks(directory):
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(subdir, file)
                replace_wikilinks(file_path)


# Example usage
replace_all_wikilinks("/docs")
