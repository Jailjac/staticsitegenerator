from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import conversions

def main():
    testNode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(testNode)


if __name__ == "__main__":
    main()

