from conversions import markdown_to_html_node, extract_title
import os
import shutil

def main():
    copy_to_directory("static", "public")
    generate_pages_recursive("content", "template.html", "public")


def copy_to_directory(src, dest):
    if not os.path.exists(src):
        raise Exception(f"{src} not found")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    src_files = os.listdir(src)
    for file in src_files:
        filepath = os.path.join(src, file)
        destpath = os.path.join(dest, file)
        if os.path.isfile(filepath):
            print(f"Copying {filepath} to {destpath}")
            shutil.copy(filepath, destpath)
        else: 
            print(f"Creating {destpath}")
            copy_to_directory(filepath, destpath)

def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise Exception(f"{from_path} not found")
    if not os.path.exists(template_path):
        raise Exception("Template not found")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path, "r")
    tf = open(template_path, "r")
    file = f.read()
    template = tf.read()
    f.close()
    tf.close()

    content = markdown_to_html_node(file).to_html()
    title = extract_title(file)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    new = open(dest_path, "w")
    new.write(page)
    new.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_files = os.listdir(dir_path_content)
    for file in dir_files:
        filepath_from = os.path.join(dir_path_content, file)
        if file.endswith(".md"):
            filepath_dest = os.path.join(dest_dir_path, f"{file[:-3]}.html")
            generate_page(filepath_from, template_path, filepath_dest)
        if os.path.isdir(filepath_from):
            filepath_dest = os.path.join(dest_dir_path, file)
            generate_pages_recursive(filepath_from, template_path, filepath_dest)


if __name__ == "__main__":
    main()
