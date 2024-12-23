import unittest

from conversions import *

class TestTextNodeToHtml(unittest.TestCase):
    def test_tn_to_html_normal(self):
        t_node = TextNode("Hello World", TextType.NORMAL, "Error")
        l_node = text_node_to_html_node(t_node)
        self.assertEqual(l_node.to_html(), 'Hello World')

    def test_tn_to_html_bold(self):
        t_node = TextNode("Hello World", TextType.BOLD, "Error")
        l_node = text_node_to_html_node(t_node)
        self.assertEqual(l_node.to_html(), '<b>Hello World</b>')

    def test_tn_to_html_italics(self):
        t_node = TextNode("Hello World", TextType.ITALIC, "Error")
        l_node = text_node_to_html_node(t_node)
        self.assertEqual(l_node.to_html(), '<i>Hello World</i>')

    def test_tn_to_html_code(self):
        t_node = TextNode("Hello World", TextType.CODE, "Error")
        l_node = text_node_to_html_node(t_node)
        self.assertEqual(l_node.to_html(), '<code>Hello World</code>')

    def test_tn_to_html_link(self):
        t_node = TextNode("Hello World", TextType.LINK, "google.com")
        l_node = text_node_to_html_node(t_node)
        self.assertEqual(l_node.to_html(), '<a href="google.com">Hello World</a>')

    def test_tn_to_html_image(self):
        t_node = TextNode("Hello World", TextType.IMAGE, "puppy.png")
        l_node = text_node_to_html_node(t_node)
        self.assertEqual(l_node.to_html(), '<img src="puppy.png" alt="Hello World"></img>')

    def test_tn_to_html_error(self):
        t_node = TextNode("Hello World", "header")
        with self.assertRaises(Exception) as err:
            l_node = text_node_to_html_node(t_node)
        self.assertEqual(str(err.exception), "Invalid TextType")

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_snd_image(self):
        node = TextNode("Hello World!", TextType.NORMAL, url="puppy.png")
        with self.assertRaises(ValueError) as err:
            new_nodes = split_node_delimiter([node], ' ', TextType.IMAGE)
        self.assertEqual(str(err.exception), "split_node_delimiter can only split bold, italics, or code text")
 
    def test_snd_bold(self):
        node = TextNode("Hello **World**!", TextType.NORMAL)
        expected = [
            TextNode("Hello ", TextType.NORMAL),
            TextNode("World", TextType.BOLD),
            TextNode("!", TextType.NORMAL)
        ]
        self.assertListEqual(split_node_delimiter([node], '**', TextType.BOLD), expected)

    def test_snd_italics(self):
        node = TextNode("Hello *There* World!", TextType.NORMAL)
        expected = [
            TextNode("Hello ", TextType.NORMAL),
            TextNode("There", TextType.ITALIC),
            TextNode(" World!", TextType.NORMAL)
        ]
        self.assertListEqual(split_node_delimiter([node], '*', TextType.ITALIC), expected)

    def test_snd_code(self):
        node = TextNode("Type `print('Hello World!')`", TextType.NORMAL)
        expected = [
            TextNode("Type ", TextType.NORMAL),
            TextNode("print('Hello World!')", TextType.CODE)
        ]
        self.assertListEqual(split_node_delimiter([node], '`', TextType.CODE), expected)

    def test_snd_multiple(self):
        node1 = TextNode("**Welcome** to the world!", TextType.NORMAL)
        node2 = TextNode("There is **so** much to see", TextType.NORMAL)
        expected = [
            TextNode("Welcome", TextType.BOLD),
            TextNode(" to the world!", TextType.NORMAL),
            TextNode("There is ", TextType.NORMAL),
            TextNode("so", TextType.BOLD),
            TextNode(" much to see", TextType.NORMAL)
        ]
        self.assertListEqual(split_node_delimiter([node1, node2], '**', TextType.BOLD), expected)

    def test_snd_multiple_in_one(self):
        node = TextNode("*Well* look what *we have* here.", TextType.NORMAL)
        expected = [
            TextNode("Well", TextType.ITALIC),
            TextNode(" look what ", TextType.NORMAL),
            TextNode("we have", TextType.ITALIC),
            TextNode(" here.", TextType.NORMAL)
        ]
        self.assertListEqual(split_node_delimiter([node], '*', TextType.ITALIC), expected)

    def test_snd_no_conversion(self):
        node = TextNode("Whoops, All Normal", TextType.NORMAL)
        expected = [
            TextNode("Whoops, All Normal", TextType.NORMAL)
        ]
        self.assertListEqual(split_node_delimiter([node], '`', TextType.CODE), expected)

    def test_snd_no_closing(self):
        node = TextNode("Uh **oh!", TextType.NORMAL)
        with self.assertRaises(Exception) as err:
            split_node_delimiter([node], '**', TextType.CODE)
        self.assertEqual(str(err.exception), "Missing Closing Delimiter")

if __name__ == "__main__":
    print("Testing Conversions")
    unittest.main()