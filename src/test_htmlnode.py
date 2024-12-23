import unittest

from htmlnode import HTMLNode, LeafNode

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

    def test_leaf_to_html_no_value(self):
        node = LeafNode(tag = "p", value= None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(tag = None, value="Tagless little loser", props={"href":"virus.com"})
        self.assertEqual(node.to_html(), "Tagless little loser")

    def test_leaf_to_html_no_props(self):
        node = LeafNode(tag="h1", value="Propless in Seattle")
        self.assertEqual(node.to_html(), "<h1>Propless in Seattle</h1>")
    
    def test_leaf_to_html_full(self):
        node = LeafNode(tag="p", value="I've got the full package", props={"href" : "google.com", "img" : "puppy.png"})
        self.assertEqual(node.to_html(), '<p href="google.com" img="puppy.png">I\'ve got the full package</p>')


if __name__ == "__main__":
    unittest.main()