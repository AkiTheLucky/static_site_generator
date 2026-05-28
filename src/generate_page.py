from block_to_html import markdown_to_html_node
import os

def extract_title(markdown):
    first_line = markdown.split("\n")[0]
    if first_line.startswith("# ") is False:
        raise Exception("no h1 header")
    h1_header = first_line.lstrip("#").strip()
    return h1_header


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, os.path.join(dest_dir_path, "index.html"))
        return
    #if dir path content doesnt point to a file, it might point to a dir. check each sub directory
    list_of_paths = os.listdir(dir_path_content)
    for pathie in list_of_paths:
        src_path = os.path.join(dir_path_content, pathie)
        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, os.path.join(dest_dir_path, pathie))

        elif os.path.isfile(src_path) and src_path.endswith(".md"):  
            dest_file_path = os.path.join(dest_dir_path, pathie)
            dest_file_path = dest_file_path.replace(".md",".html")
            generate_page(src_path,template_path, dest_file_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    #read md file index and store contents in variable
    
    with open(from_path) as f:
        md_content = f.read()
    
    with open(template_path) as f:
        template_content = f.read()
    md_as_html_string = markdown_to_html_node(md_content).to_html()
    page_title = extract_title(md_content)
    
    final_html_page = template_content.replace("{{ Title }}", page_title).replace("{{ Content }}", md_as_html_string)

    dir_portion = os.path.dirname(dest_path)
    if dir_portion:
        os.makedirs(dir_portion, exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(final_html_page)
