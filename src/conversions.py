import re

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
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

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node.copy())
        else: 
            current_text = node.text
            for image in images:
                lsplit, rsplit = current_text.split(f"![{image[0]}]({image[1]})", 1)
                if lsplit != "":
                    new_nodes.append(TextNode(lsplit, node.text_type))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                current_text = rsplit
            if current_text != "":
                new_nodes.append(TextNode(current_text, node.text_type))

    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node.copy())
        else: 
            current_text = node.text
            for link in links:
                lsplit, rsplit = current_text.split(f"[{link[0]}]({link[1]})", 1)
                if lsplit != "":
                    new_nodes.append(TextNode(lsplit, node.text_type))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                current_text = rsplit
            if current_text != "":
                new_nodes.append(TextNode(current_text, node.text_type))

    return new_nodes

def text_to_nodes(text):
    bold_text = split_nodes_delimiter([TextNode(text, TextType.NORMAL)], "**", TextType.BOLD)
    italics_text = split_nodes_delimiter(bold_text, "*", TextType.ITALIC)
    code_text = split_nodes_delimiter(italics_text, "`", TextType.CODE)
    image_nodes = split_nodes_images(code_text)
    link_nodes = split_nodes_links(image_nodes)
    return link_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks = map(lambda s : s.strip().strip("\n"), blocks)
    return [s for s in blocks if s != ""]