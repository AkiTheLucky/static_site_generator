import re
from textnode import TextType, TextNode
from split_delim import split_nodes_delimiter

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

    #turn image and link strings into textnodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        
        images = extract_markdown_images(old_node.text)
        remaining_text = old_node.text
        if len(images) ==0:
            new_nodes.append(old_node)
            continue
        for alt, url in images:
            sections = remaining_text.split(f"![{alt}]({url})", 1)
            new_img_node = TextNode(alt, TextType.IMAGE, url)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(new_img_node)
            remaining_text = sections[1]

        
        if remaining_text != "":
            remaining_node = TextNode(remaining_text, TextType.TEXT)
            new_nodes.append(remaining_node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        
        links = extract_markdown_links(old_node.text)
        remaining_text = old_node.text
        if len(links) ==0:
            new_nodes.append(old_node)
            continue
        for alt, url in links:
            sections = remaining_text.split(f"[{alt}]({url})", 1)
            new_link_node = TextNode(alt, TextType.LINK, url)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(new_link_node)
            remaining_text = sections[1]

        
        if remaining_text != "":
            remaining_node = TextNode(remaining_text, TextType.TEXT)
            new_nodes.append(remaining_node)
    return new_nodes


# all texts to textnodes:

def text_to_textnodes(text):
    
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

