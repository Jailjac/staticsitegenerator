from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node):
    tag, value, props = None, text_node.text, None
    match text_node.text_type:
        case TextType.NORMAL:
            pass
        case TextType.BOLD:
            tag = "b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.CODE:
            tag = "code"
        case TextType.LINK:
            tag = "a"
            props = {"href" : text_node.url}
        case TextType.IMAGE:
            tag = "img"
            value = ""
            props = {"src" : text_node.url, "alt" : text_node.text}
        case _:
            raise Exception("Invalid TextType")
    
    return LeafNode(tag, value, props)

def split_node_delimiter(old_nodes, delimiter, text_type):
    if text_type not in [TextType.BOLD, TextType.ITALIC, TextType.CODE]:
        raise ValueError("split_node_delimiter can only split bold, italics, or code text")
    new_nodes = []
    for node in old_nodes:
        if node.text.count(delimiter) % 2 == 1:
            raise Exception("Missing Closing Delimiter")
        if node.text_type == TextType.NORMAL:
            new_text = node.text.split(delimiter)
            for i in range(len(new_text)):
                if new_text[i] != "":
                    if i % 2 == 0:
                        new_nodes.append(TextNode(new_text[i], node.text_type, node.url))
                    else:
                        new_nodes.append(TextNode(new_text[i], text_type, node.url))
        else: 
            new_nodes.append(node.copy())
    return new_nodes

