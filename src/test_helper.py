import unittest

from blocknode import BlockType
from helper import block_to_block_type, block_to_html_node, code_block_to_html_node, extract_markdown_images, extract_markdown_links, heading_block_to_html_node, markdown_to_blocks, markdown_to_html_node, ordered_list_block_to_html_node, quote_block_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_node_to_html_node, text_to_textnodes, unordered_list_block_to_html_node
from textnode import TextNode, TextType

class TestHelper(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_img(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://picsum.photos/200/300")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "https://picsum.photos/200/300",
            "alt": "This is an image node"
        })

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://picsum.photos/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {
            "href": "https://picsum.photos/",
        })

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.props, None)

    def test_split_nodes_delimiter_for_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_for_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_for_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_with_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with [link1](https://i.imgur.com/zjjcJKZ.png) [link2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link1", "https://i.imgur.com/zjjcJKZ.png"), ("link2", "https://i.imgur.com/zjjcJKZ.png")], matches)

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
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        text_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_nodes
        )

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

    def test_block_to_block_type_paragraph(self):
        block = "This is **bolded** paragraph"
        block_type = block_to_block_type(block)

        self.assertEqual(
            BlockType.PARAGRAPH,
            block_type
        )

    def test_block_to_block_type_heading_h1(self):
        block = "# This is h1 heading"
        block_type = block_to_block_type(block)

        self.assertEqual(
            BlockType.HEADING,
            block_type
        )

    def test_block_to_block_type_heading_h6(self):
        block = "###### This is h6 heading"
        block_type = block_to_block_type(block)

        self.assertEqual(
            BlockType.HEADING,
            block_type
        )

    def test_block_to_block_type_code_clock(self):
        block = '```print("Hello World")```'
        block_type = block_to_block_type(block)

        self.assertEqual(
            BlockType.CODE,
            block_type
        )

    def test_block_to_block_type_quote_clock(self):
        block = "> Knowing is not enough, we must apply"

        block_type = block_to_block_type(block)

        self.assertEqual(
            BlockType.QUOTE,
            block_type
        )

    def test_block_to_block_type_unorderd_list(self):
        block = "- This is a list\n- with items"
        block_type = block_to_block_type(block)

        self.assertEqual(
            BlockType.UNORDERED_LIST,
            block_type
        )

    def test_block_to_block_type_orderd_list(self):
        block = "1. This is a list\n2. with items"
        block_type = block_to_block_type(block)

        self.assertEqual(
            BlockType.ORDERED_LIST,
            block_type
        )

    def test_heading_block_to_html_node(self):
        block = "### This is title"

        html_node = heading_block_to_html_node(block)

        self.assertEqual(
            "<h3>This is title</h3>",
            html_node.to_html()
        )

    def test_code_block_to_html_node(self):
        block = '```print("Hello World")\n- This is list```'

        html_node = code_block_to_html_node(block)

        self.assertEqual(
            '<pre><code>print("Hello World")\n- This is list</code></pre>',
            html_node.to_html()
        )

    def test_quote_block_to_html_node(self):
        block = ">This is quote\n>this is **next** line"

        html_node = quote_block_to_html_node(block)

        self.assertEqual(
            '<blockquote><p>This is quote</p><p>this is <b>next</b> line</p></blockquote>',
            html_node.to_html()
        )

    def test_unordered_list_block_to_html_node(self):
        block = "- This is unordered list\n- this is _next_ item"

        html_node = unordered_list_block_to_html_node(block)

        self.assertEqual(
            '<ul><li>This is unordered list</li><li>this is <i>next</i> item</li></ul>',
            html_node.to_html()
        )

    def test_ordered_list_block_to_html_node(self):
        block = "1. This is ordered list\n2. this is _next_ item"

        html_node = ordered_list_block_to_html_node(block)

        self.assertEqual(
            '<ol><li>This is ordered list</li><li>this is <i>next</i> item</li></ol>',
            html_node.to_html()
        )

    def test_block_to_html_node(self):
        block = "### This is title"
        block_type = BlockType.HEADING

        html_node = block_to_html_node(block, block_type)

        self.assertEqual(
            "<h3>This is title</h3>",
            html_node.to_html()
        )

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
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            html
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
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
            html
        )
if __name__ == "__main__":
    unittest.main()
