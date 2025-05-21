import os
import shutil

from helper import extract_title, markdown_to_html_node

def clean_dir(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"Removed file: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Removed directory: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def copy_dir(src_path, dest_path):
    os.makedirs(dest_path, exist_ok=True)
    for item in os.listdir(src_path):
        s = os.path.join(src_path, item)
        d = os.path.join(dest_path, item)
        try:
            if os.path.isfile(s):
                shutil.copy2(s, d)
                print(f"Copied file: {s} to {d}")
            elif os.path.isdir(s):
                copy_dir(s, d)
        except Exception as e:
            print(f"Failed to copy {s} to {d}. Reason: {e}")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, encoding='utf-8') as file:
        markdown = file.read()

    with open(template_path, encoding='utf-8') as file:
        template = file.read()

    title = extract_title(markdown)
    html_string = markdown_to_html_node(markdown).to_html()

    output = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    with open(dest_path, 'w', encoding='utf-8') as file:
        file.write(output)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    os.makedirs(dest_dir_path, exist_ok=True)
    for item in os.listdir(dir_path_content):
        s = os.path.join(dir_path_content, item)

        # Change .md to .html for the destination file
        if os.path.isfile(s) and s.endswith(".md"):
            filename = os.path.splitext(item)[0] + ".html"
            d = os.path.join(dest_dir_path, filename)
            try:
                generate_page(s, template_path, d)
                print(f"Generated {d} from {s}")
            except Exception as e:
                print(f"Failed to generate {s} to {d}. Reason: {e}")

        elif os.path.isdir(s):
            d = os.path.join(dest_dir_path, item)
            generate_pages_recursive(s, template_path, d)

def main():
    public_path = "./public"
    static_path = "./static"

    os.makedirs(public_path, exist_ok=True)
    clean_dir(public_path)

    if os.path.exists(static_path):
        copy_dir(static_path, public_path)
    else:
        print(f"Source path '{static_path}' does not exist. Nothing to copy.")

    content_path = "./content"
    template_path = "./template.html"
    dest_path = "./public"

    generate_pages_recursive(content_path, template_path, dest_path)

if __name__ == "__main__":
    main()
