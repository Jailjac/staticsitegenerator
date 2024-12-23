import unittest

from main import text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import LeafNode

class TestTextNodeToHtml(unittest.TestCase):
    def tn_to_html_normal(self):
        t_node = TextNode("Hello World", TextType.NORMAL, "Error")
        l_node = text_node_to_html_node(t_node)
        self.assertEqual(l_node.to_html, 'Hello World')

    def tn_to_html_bold(self):
        t_node = TextNode("Hello World", TextType.BOLD, "Error")
        l_node = text_node_to_html_node(t_node)
        self.assertEqual(l_node.to_html, '<b>Hello World</b>')

    def tn_to_html_italics(self):
        t_node = TextNode("Hello World", TextType.ITALIC, "Error")
        l_node = text_node_to_html_node(t_node)
        self.assertEqual(l_node.to_html, '<i>Hello World</i>')

    def tn_to_html_code(self):
        t_node = TextNode("Hello World", TextType.CODE, "Error")
        l_node = text_node_to_html_node(t_node)
        self.assertEqual(l_node.to_html, '<code>Hello World</code>')

    def tn_to_html_link(self):
        t_node = TextNode("Hello World", TextType.LINK, "google.com")
        l_node = text_node_to_html_node(t_node)
        self.assertEqual(l_node.to_html, '<a href="google.com">Hello World</a>')

    def tn_to_html_image(self):
        t_node = TextNode("Hello World", TextType.IMAGE, "puppy.png")
        l_node = text_node_to_html_node(t_node)
        self.assertEqual(l_node.to_html, '<img src="puppy.png" alt="Hello World"></img>')

    def tn_to_html_error(self):
        t_node = TextNode("Hello World", TextType.HEADER)
        with self.assertRaises(Exception) as err:
            l_node = text_node_to_html_node(t_node)
        self.assertEqual(str(err.exception), "Invalid TextType")