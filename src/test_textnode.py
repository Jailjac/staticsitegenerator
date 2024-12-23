import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq_all(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This isn't a text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_noteq_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_noteq_plus_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertNotEqual(node, node2)

    def test_eq_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

if __name__ == "__main__":
    print("Testing Text Node")
    unittest.main()