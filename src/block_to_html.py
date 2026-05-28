#now is time for the big boys

#imports
from to_blocks import BlockType, block_to_type, markdown_to_blocks
from textnode import TextNode, text_node_to_html_node, TextType
from htmlnode import ParentNode
from regx_and_to_TextNode import text_to_textnodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_type(block)
        #check each type of block: 1. check for heading and pass to heading helper function
        if block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))

        elif block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))

        # ... etc for each block type
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))



        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))



        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_to_html_node(block))

        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_to_html_node(block))



    return ParentNode("div", children)



#helper function heading_to_html_node(block)
def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
            if level > 6:
                raise ValueError
        else:
            break
        
    text = block[level + 1:]
    if text == "":
        raise ValueError("no text after heading")
    list_of_children = text_to_children(text)
    return ParentNode(f"h{level}", list_of_children)

#helper function paragraph_to_html_node(block)
#Split the block on "\n" to get a list of lines and Join them back together with " " (a space)
def paragraph_to_html_node(block):
    block_split = block.split("\n")
    block = " ".join(block_split)
    if block == "":
        raise ValueError("no text")
    list_of_children = text_to_children(block)

    return ParentNode("p", list_of_children)


#3rd helper function for code
def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")

    block = block[4:-3]

    if block == "":
        raise ValueError("no text")

    new_textnode = TextNode(block, TextType.TEXT)
    new_htmlnode = text_node_to_html_node(new_textnode)
    inner_parent = ParentNode("code", [new_htmlnode])
    outer_parent = ParentNode("pre", [inner_parent])

    return outer_parent

#4th helper function for quotes

def quote_to_html_node(block):
    block_split = block.split("\n")
    block_split_stripped = []
    for line in block_split:
        if line.startswith(">") is False:
            raise ValueError("not a valid quote")
        new_line = line.lstrip(">").strip()
        block_split_stripped.append(new_line)

    block = " ".join(block_split_stripped)
    if block == "":
        raise ValueError("no text")
    list_of_children = text_to_children(block)

    return ParentNode("blockquote", list_of_children)

#5th helper for unordered_to_html_node(block)
def unordered_to_html_node(block):
    block_split = block.split("\n")
    block_split_stripped = []
    for block in block_split:
        block = block[2:]
        list_of_children = text_to_children(block)
        
        block_split_stripped.append(ParentNode("li", list_of_children))
    

    return ParentNode("ul", block_split_stripped)

# 6th helper for ordered_to_html_node(block)
def ordered_to_html_node(block):
    block_split = block.split("\n")
    block_split_stripped = []
    for block in block_split:
        block = block.split(". ", 1)[1]
        list_of_children = text_to_children(block)
        
        block_split_stripped.append(ParentNode("li", list_of_children))
    

    return ParentNode("ol", block_split_stripped)



#2nd helper function, text_to_children(text)
def text_to_children(text):
    list_of_TextNodes = text_to_textnodes(text)
    children = []
    #turn each into an HTML Node
    for textynode in list_of_TextNodes:
        children.append( text_node_to_html_node(textynode))
    return children

