
from copy_static import copy_static_page
from generate_page import generate_pages_recursive
import sys

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

def main():
    copy_static_page("static", "docs")
    generate_pages_recursive(basepath, "content", "template.html", "docs")
    
main()