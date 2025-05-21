
import re
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

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text = node.text
            matches = extract_markdown_images(text)
            last_idx = 0

            for alt, src in matches:
                img_markdown = f"![{alt}]({src})"
                idx = text.find(img_markdown, last_idx)
                if idx != -1:
                    if idx > last_idx:
                        new_nodes.append(TextNode(text[last_idx:idx], TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.IMAGE, src))
                    last_idx = idx + len(img_markdown)

            if last_idx < len(text):
                new_nodes.append(TextNode(text[last_idx:], TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text = node.text
            matches = extract_markdown_links(text)
            last_idx = 0

            for alt, src in matches:
                link_markdown = f"[{alt}]({src})"
                idx = text.find(link_markdown, last_idx)
                if idx != -1:
                    if idx > last_idx:
                        new_nodes.append(TextNode(text[last_idx:idx], TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.LINK, src))
                    last_idx = idx + len(link_markdown)

            if last_idx < len(text):
                new_nodes.append(TextNode(text[last_idx:], TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes
