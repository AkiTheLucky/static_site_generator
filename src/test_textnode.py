import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_URL(self):
        node = TextNode("This is a link node", TextType.LINK, "www.4chan.org")
        node2 = TextNode("This is a link node", TextType.LINK, "www.4chan.org")
        self.assertEqual(node, node2)
    def test_URL_none(self):
        node = TextNode("This is a link node", TextType.LINK, None)
        node2 = TextNode("This is a link node", TextType.LINK, None)
        self.assertEqual(node, node2)
    def test_URL_diff(self):
        node = TextNode("This is a link node", TextType.LINK, "www.4chan.org")
        node2 = TextNode("This is a link node", TextType.LINK, None)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()