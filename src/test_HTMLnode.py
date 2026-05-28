import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from split_delim import split_nodes_delimiter
from regx_and_to_TextNode import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from to_blocks import markdown_to_blocks,BlockType, block_to_type
from block_to_html import markdown_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_something_specific(self):
        node = HTMLNode("a", "click me", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html2(self):
        node = HTMLNode("a", "click me", None, {"href": "https://example.com", "target": "https://target.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="https://target.com"')

    def test_something_specific2(self):
        node = HTMLNode("a", "click me", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",)
    
    def test_parent_with_multiple_leaf_children(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold"),
            LeafNode(None, " plain "),
            LeafNode("i", "italic"),
        ])
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold</b> plain <i>italic</i></p>"
        )

    def test_parent_without_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode(None, "text")]).to_html()


    def test_parent_without_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()
    def test_nested_parents_multiple_levels(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("p", [
                    LeafNode(None, "deep text")
                ])
            ])
        ])
        self.assertEqual(
            node.to_html(),
            "<div><section><p>deep text</p></section></div>"
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_invalid_type(self):
        node = TextNode("oops", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)



    #tests for split_delim here

    def test_valid_delim(self):
        #arrange:
        input_data = TextNode("this is a code here: `print(hello world)` and mic drop", TextType.TEXT)
        #act
        result = split_nodes_delimiter([input_data], "`", TextType.CODE)
        #expected_result
        expected_result = [
            TextNode("this is a code here: ", TextType.TEXT),
            TextNode("print(hello world)", TextType.CODE),
            TextNode(" and mic drop", TextType.TEXT),
        ]
        #assert
        self.assertEqual(result, expected_result)

    def test_valid_no_delim(self):
        #arrange:
        input_data = TextNode("this is not a code here: print(hello world) and mic drop", TextType.TEXT)
        #act
        result = split_nodes_delimiter([input_data], "`", TextType.CODE)
        #expected_result
        expected_result = [TextNode("this is not a code here: print(hello world) and mic drop", TextType.TEXT)]
        #assert
        self.assertEqual(result, expected_result)

    #image regex test
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://wikipedia.org"),
            ],
            matches,
        )



    #test to_textNode_from image and link now:
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://wikipedia.org"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    #test the final thing now:
    def test_text_to_textNode1(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(node)
        expected =[
            TextNode("This is ", TextType.TEXT), 
            TextNode("text", TextType.BOLD), 
            TextNode(" with an ",TextType.TEXT), 
            TextNode("italic", TextType.ITALIC), 
            TextNode(" word and a ",TextType.TEXT), 
            TextNode("code block",TextType.CODE), 
            TextNode(" and an ", TextType.TEXT), 
            TextNode("obi wan image",TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
            TextNode(" and a ", TextType.TEXT), 
            TextNode("link",TextType.LINK, "https://boot.dev")
        ]
        self.assertListEqual(expected,nodes)

    #testing the new to_block function
    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                ],
            )

    def test_quote(self):
            block = ">line one\n>line two"
            self.assertEqual(block_to_type(block), BlockType.QUOTE)
        
    def test_quote_missing_marker(self):
            block = ">line one\nline two without marker"
            self.assertEqual(block_to_type(block), BlockType.PARAGRAPH)


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    
    def test_paragraphs2(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )




if __name__ == "__main__":
    unittest.main()