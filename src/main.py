from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    testNode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(testNode)

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
        


if __name__ == "__main__":
    main()

