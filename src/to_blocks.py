from enum import Enum

def markdown_to_blocks(markdown):
    new_list_of_blockstrings = []
    list_of_blockstrings = markdown.split("\n\n")
    for i in range(len(list_of_blockstrings)):
        list_of_blockstrings[i] = list_of_blockstrings[i].strip()
        if list_of_blockstrings[i] != "":
            new_list_of_blockstrings.append(list_of_blockstrings[i])
    return new_list_of_blockstrings



class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    HTML_BLOCK = "html_block" # <-- NEW

def block_to_type(markdown):
    if markdown.startswith("<"): # If it starts with an HTML tag
        return BlockType.HTML_BLOCK
    if markdown.startswith(("# ","## ","### ","#### ","##### ","###### ",)):
        return BlockType.HEADING
    if markdown.split("\n")[0].startswith("```") and markdown.split("\n")[-1].startswith("```"):
        if len(markdown.split("\n")) > 1:
            return BlockType.CODE
    
    if markdown.startswith(">"):
        lines = markdown.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if markdown.startswith("- "):
        lines = markdown.split("\n")
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST


    if markdown.startswith("1. "):
        lines = markdown.split("\n")
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
    
