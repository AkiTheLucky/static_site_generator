from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            if delimiter in old_node.text:
                
                split_list = old_node.text.split(delimiter)
                if len(split_list) % 2 == 0:
                    raise ValueError("no closing delimiter")
                for index, piece in enumerate(split_list):
                    if piece == "":
                        continue
                    if index % 2 == 0:

                        new_node = TextNode(piece, TextType.TEXT)
                    else:
                        new_node = TextNode(piece, text_type)
                    new_nodes.append(new_node)
            else:
                new_nodes.append(old_node)
    return new_nodes