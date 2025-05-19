import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_none_value(self):
        try:
            node = LeafNode("p", None)
            node.to_html()
        except ValueError as e:
            self.assertEqual(str(e), "All leaf nodes must have a value.")

if __name__ == "__main__":
    unittest.main()
