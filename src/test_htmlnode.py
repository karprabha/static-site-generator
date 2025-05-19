import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_args(self):
        node = HTMLNode(tag="a", value="click me",props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_without_args(self):
        node = HTMLNode(tag="a", value="click me")
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_with_single_arg(self):
        node = HTMLNode(tag="a", value="click me",props={
            "href": "https://www.google.com",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

if __name__ == "__main__":
    unittest.main()
