import os
import shutil

def copy_static_page(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    helper_function(src, dst)


def helper_function(src, dst):

    if os.path.exists(src):
        list_of_contents = os.listdir(src)
        
        for content in list_of_contents:
            path_to_content = os.path.join(src, content)
            
            if os.path.isfile(path_to_content):
                shutil.copy(path_to_content, os.path.join(dst, content))
            else:
                path_to_dest_content = os.path.join(dst, content)
                os.mkdir(path_to_dest_content)
                helper_function(path_to_content, path_to_dest_content)

    