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

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_snd_image(self):
        node = TextNode("Hello World!", TextType.NORMAL, url="puppy.png")
        with self.assertRaises(ValueError) as err:
            new_nodes = split_nodes_delimiter([node], ' ', TextType.IMAGE)
        self.assertEqual(str(err.exception), "split_node_delimiter can only split bold, italics, or code text")
 
    def test_snd_bold(self):
        node = TextNode("Hello **World**!", TextType.NORMAL)
        expected = [
            TextNode("Hello ", TextType.NORMAL),
            TextNode("World", TextType.BOLD),
            TextNode("!", TextType.NORMAL)
        ]
        self.assertListEqual(split_nodes_delimiter([node], '**', TextType.BOLD), expected)

    def test_snd_italics(self):
        node = TextNode("Hello *There* World!", TextType.NORMAL)
        expected = [
            TextNode("Hello ", TextType.NORMAL),
            TextNode("There", TextType.ITALIC),
            TextNode(" World!", TextType.NORMAL)
        ]
        self.assertListEqual(split_nodes_delimiter([node], '*', TextType.ITALIC), expected)

    def test_snd_code(self):
        node = TextNode("Type `print('Hello World!')`", TextType.NORMAL)
        expected = [
            TextNode("Type ", TextType.NORMAL),
            TextNode("print('Hello World!')", TextType.CODE)
        ]
        self.assertListEqual(split_nodes_delimiter([node], '`', TextType.CODE), expected)

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
        self.assertListEqual(split_nodes_delimiter([node1, node2], '**', TextType.BOLD), expected)

    def test_snd_multiple_in_one(self):
        node = TextNode("*Well* look what *we have* here.", TextType.NORMAL)
        expected = [
            TextNode("Well", TextType.ITALIC),
            TextNode(" look what ", TextType.NORMAL),
            TextNode("we have", TextType.ITALIC),
            TextNode(" here.", TextType.NORMAL)
        ]
        self.assertListEqual(split_nodes_delimiter([node], '*', TextType.ITALIC), expected)

    def test_snd_no_conversion(self):
        node = TextNode("Whoops, All Normal", TextType.NORMAL)
        expected = [
            TextNode("Whoops, All Normal", TextType.NORMAL)
        ]
        self.assertListEqual(split_nodes_delimiter([node], '`', TextType.CODE), expected)

    def test_snd_no_closing(self):
        node = TextNode("Uh **oh!", TextType.NORMAL)
        with self.assertRaises(Exception) as err:
            split_nodes_delimiter([node], '**', TextType.CODE)
        self.assertEqual(str(err.exception), "Missing Closing Delimiter")

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images_no_image(self):
        text = "This isn't an image. At all. Sorry."
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_image_almost_image(self):
        text = "This ![might[]](beanimage?). It's not though"
        self.assertEqual(extract_markdown_images(text), [])
    
    def test_extract_image_one(self):
        text = "Finally! An image![Alt Text](Url)"
        expect = [
            ("Alt Text", "Url")
        ]
        self.assertEqual(extract_markdown_images(text), expect)

    def test_extract_image_multiple(self):
        text = "Finally! ![one image](puppy.png) and ![two image](kitten.png)"
        expect = [
            ("one image", "puppy.png"),
            ("two image", "kitten.png")
        ]
        self.assertEqual(extract_markdown_images(text), expect)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_link_no_link(self):
        text = "A link? Never heard of one"
        self.assertEqual(extract_markdown_links(text), [])
    
    def test_extract_link_image(self):
        text = "Heres an image ![alt text](url)"
        self.assertEqual(extract_markdown_links(text), [])
    
    def test_extract_link_one(self):
        text = "Here is a [link](www.google.com) for you"
        expect = [
            ("link", "www.google.com")
        ]
        self.assertEqual(extract_markdown_links(text), expect)

    def test_extract_link_multiple(self):
        text = "Here is [one link](www.google.com) and another [two link](www.youtube.com)"
        expect = [
            ("one link", "www.google.com"),
            ("two link", "www.youtube.com")
        ]
        self.assertEqual(extract_markdown_links(text), expect)

class TestSplitNodesImages(unittest.TestCase):
    def test_sni_no_image(self):
        node = TextNode("No image here to split.", TextType.NORMAL)
        self.assertEqual(split_nodes_images([node]), [node])

    def test_sni_one_image(self):
        node = TextNode("One image ![alt text](url) right here", TextType.NORMAL)
        expect = [
            TextNode("One image ", TextType.NORMAL),
            TextNode("alt text", TextType.IMAGE, "url"),
            TextNode(" right here", TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_images([node]), expect)

    def test_sni_multiple_images(self):
        node = TextNode("![first image](first url)First Image, Second Image![second image](second url)", TextType.NORMAL)
        expect = [
            TextNode("first image", TextType.IMAGE, "first url"),
            TextNode("First Image, Second Image", TextType.NORMAL),
            TextNode("second image", TextType.IMAGE, "second url")
        ]
        self.assertEqual(split_nodes_images([node]), expect)

    def test_sni_multiple_nodes(self): 
        node1 = TextNode("![first image](first url)First Image, Second Image![second image](second url)", TextType.NORMAL)
        node2 = TextNode("Two images ![alt text](url)![altier text](urlier) right here", TextType.NORMAL)
        expect = [
            TextNode("first image", TextType.IMAGE, "first url"),
            TextNode("First Image, Second Image", TextType.NORMAL),
            TextNode("second image", TextType.IMAGE, "second url"),
            TextNode("Two images ", TextType.NORMAL),
            TextNode("alt text", TextType.IMAGE, "url"),
            TextNode("altier text", TextType.IMAGE, "urlier"),
            TextNode(" right here", TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_images([node1, node2]), expect)

    def test_sni_bold_image(self):
        node = TextNode("This ![image](image url) is bold!", TextType.BOLD)
        expect = [
            TextNode("This ", TextType.BOLD),
            TextNode("image", TextType.IMAGE, "image url"),
            TextNode(" is bold!", TextType.BOLD)
        ]
        self.assertEqual(split_nodes_images([node]), expect)

class TestSplitNodesLinks(unittest.TestCase):
    def test_snl_no_links(self):
        node = TextNode("No link here to split.", TextType.NORMAL)
        self.assertEqual(split_nodes_links([node]), [node])

    def test_snl_one_link(self):
        node = TextNode("One link [alt text](url) right here", TextType.NORMAL)
        expect = [
            TextNode("One link ", TextType.NORMAL),
            TextNode("alt text", TextType.LINK, "url"),
            TextNode(" right here", TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_links([node]), expect)

    def test_snl_multiple_images(self):
        node = TextNode("[first link](first url)First Link, Second Link[second link](second url)", TextType.NORMAL)
        expect = [
            TextNode("first link", TextType.LINK, "first url"),
            TextNode("First Link, Second Link", TextType.NORMAL),
            TextNode("second link", TextType.LINK, "second url")
        ]
        self.assertEqual(split_nodes_links([node]), expect)

    def test_sni_multiple_nodes(self): 
        node1 = TextNode("[first link](first url)First Link, Second Image![second image](second url)", TextType.NORMAL)
        node2 = TextNode("Two links [alt text](url)[altier text](urlier) right here", TextType.NORMAL)
        expect = [
            TextNode("first link", TextType.LINK, "first url"),
            TextNode("First Link, Second Image![second image](second url)", TextType.NORMAL),
            TextNode("Two links ", TextType.NORMAL),
            TextNode("alt text", TextType.LINK, "url"),
            TextNode("altier text", TextType.LINK, "urlier"),
            TextNode(" right here", TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_links([node1, node2]), expect)

class TestTextToNodes(unittest.TestCase):
    def test_tttn_none(self):
        text = "This is perfectly normal text with no added markdown."
        expect = [TextNode(text, TextType.NORMAL)]
        self.assertEqual(text_to_nodes(text), expect)

    def test_tttn_all(self):
        text = "This is **bold** and *italics* and `code` and ![image](image_url) and [link](link_url)"
        expect = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("italics", TextType.ITALIC),
            TextNode(" and ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "image_url"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "link_url")
        ]
        self.assertEqual(text_to_nodes(text), expect)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_mtb_none(self):
        text = ""
        self.assertEqual(markdown_to_blocks(text), [])

    def test_mtb_one(self):
        text = "This is one block"
        self.assertEqual(markdown_to_blocks(text), ["This is one block"])

    def test_mtb_multiple(self):
        text = "# This is a heading\n\nThis is a paragraph\n\n* This is list item one\n* This is list item two"
        expect = [
            "# This is a heading",
            "This is a paragraph",
            "* This is list item one\n* This is list item two"
        ]
        self.assertEqual(markdown_to_blocks(text), expect)

    def test_mtb_excess(self):
        text = "# Heading\n\n\n\n\n     paragraph     \n\n\n\n\n\n* List item"
        expect = [
            "# Heading",
            "paragraph",
            "* List item"
        ]
        self.assertEqual(markdown_to_blocks(text), expect)


if __name__ == "__main__":
    print("Testing Conversions")
    unittest.main()