import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_none(self):
        node1 = HTMLNode(tag="p", value="Hello world!")
        self.assertEqual(node1.props_to_html(), "")

    def test_props_one(self):
        node1 = HTMLNode(props={"a":1})
        self.assertEqual(node1.props_to_html(), ' a="1"')

    def test_props_multiple(self):
        node1 = HTMLNode(props={"link":"google.com", "notes":"Search Engine"})
        self.assertEqual(node1.props_to_html(), ' link="google.com" notes="Search Engine"')


if __name__ == "__main__":
    unittest.main()