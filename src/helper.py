from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError("Invalid text_type")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b",value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i",value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code",value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a",value=text_node.text, props={
                "href": text_node.url
            })
        case TextType.IMAGE:
            return LeafNode(tag="img",value="", props={
                "src": text_node.url,
                "alt": text_node.text
            })


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_text = node.text.split(delimiter)
            for i in range(0, len(split_text), 3):
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                if i + 1 < len(split_text):
                    new_nodes.append(TextNode(split_text[i+1], text_type))
                if i + 2 < len(split_text):
                    new_nodes.append(TextNode(split_text[i+2], TextType.TEXT))
        else:
            new_nodes.append(node)

        return new_nodes
