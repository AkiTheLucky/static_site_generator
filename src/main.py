
from copy_static import copy_static_page
from generate_page import generate_pages_recursive

def main():
    copy_static_page("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    
main()