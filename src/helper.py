import re
from blocknode import BlockType
from leafnode import LeafNode
from parentnode import ParentNode
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

def text_to_textnodes(text):
    text_nodes = split_nodes_link(split_nodes_image([TextNode(text, TextType.TEXT)]))

    text_type_delimiter_map = {
        TextType.BOLD: "**",
        TextType.ITALIC: "_",
        TextType.CODE: "`"
    }

    for text_type in text_type_delimiter_map:
        text_nodes = split_nodes_delimiter(text_nodes, text_type_delimiter_map[text_type], text_type)

    return text_nodes

def markdown_to_blocks(markdown):
    blocks = list(
        filter(
            lambda x: x != "",
            map(
                lambda x: x.strip(),
                markdown.split("\n\n")
            )
        )
    )

    return blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6}\s+.+", block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split('\n')
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE

    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST

    if len(lines) > 0 and all(re.match(r'^\d+\.\s+', line) for line in lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    if text_nodes == None:
        return [text_node_to_html_node(TextNode(" ", TextType.TEXT))]

    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))

    if len(children) == 0:
        return [text_node_to_html_node(TextNode(" ", TextType.TEXT))]

    return children

def heading_block_to_html_node(block):
    cnt = 0
    for i in range(0, 6):
        if block[i] == "#":
            cnt += 1

    text = block[cnt:].strip()
    children = text_to_children(text)

    return ParentNode(f"h{cnt}", children)

def code_block_to_html_node(block):
    text = block[3:-3].strip()

    return ParentNode("pre", [text_node_to_html_node(TextNode(text, TextType.CODE))])

def quote_block_to_html_node(block):
    lines = list(
        map(
            lambda x: x[1:],
            block.split("\n")
        )
    )

    children = []
    for line in lines:
        children.append(ParentNode("p", text_to_children(line)))

    return ParentNode("blockquote", children)

def unordered_list_block_to_html_node(block):
    lines = list(
        map(
            lambda x: x[2:],
            block.split("\n")
        )
    )

    children = []
    for line in lines:
        children.append(ParentNode("li", text_to_children(line)))

    return ParentNode("ul", children)

def ordered_list_block_to_html_node(block):
    lines = list(
        map(
            lambda x: x.lstrip('0123456789. '),
            block.split("\n")
        )
    )

    children = []
    for line in lines:
        children.append(ParentNode("li", text_to_children(line)))

    return ParentNode("ol", children)

def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.HEADING:
            return heading_block_to_html_node(block)
        case BlockType.CODE:
            return code_block_to_html_node(block)
        case BlockType.QUOTE:
            return quote_block_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_block_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_block_to_html_node(block)
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_children(" ".join(block.split("\n"))))
        case _:
            raise ValueError("Invalid block type!!")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []
    for block in blocks:
        children.append(block_to_html_node(block, block_to_block_type(block)))

    return ParentNode("div", children)

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise ValueError("No h1 header found in the markdown.")
