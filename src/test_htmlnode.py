import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):
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

class TestParentNode(unittest.TestCase):
    def test_parent_no_children(self):
        node = ParentNode(tag="p", children=None)
        with self.assertRaises(ValueError) as err:
            node.to_html()
        
        self.assertEqual(str(err.exception), "ParentNode missing children")

    def test_parent_no_tag(self):
        node = ParentNode(tag=None, children=[LeafNode("h1", "Hello!")])
        with self.assertRaises(ValueError) as err:
            node.to_html()

        self.assertEqual(str(err.exception), "ParentNode missing tag")

    def test_parent_one_child(self):
        node = ParentNode(tag="p", children=[LeafNode(None, "Normal Text")])
        self.assertEqual(node.to_html(), "<p>Normal Text</p>")

    def test_parent_multiple_children(self):
        node = ParentNode("h1", [LeafNode("b", "Bold Text"), LeafNode("img", "Image Text", {"href" : "puppy.img"})])
        self.assertEqual(node.to_html(), '<h1><b>Bold Text</b><img href="puppy.img">Image Text</img></h1>')

    def test_parent_nested_children(self):
        node_inside = ParentNode("b", [LeafNode("i", "Bold and Italics"), LeafNode(None, "Just Bold")])
        node = ParentNode("p", [node_inside, LeafNode(None, "Normal Text")], {"r" : 132})
        self.assertEqual(node.to_html(), '<p r="132"><b><i>Bold and Italics</i>Just Bold</b>Normal Text</p>')

    
if __name__ == "__main__":
    print("Testing HTML")
    unittest.main()