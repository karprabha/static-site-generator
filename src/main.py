from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError("Invalid text_type")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.value)
        case TextType.BOLD:
            return LeafNode(tag="b",value=text_node.value)
        case TextType.ITALIC:
            return LeafNode(tag="i",value=text_node.value)
        case TextType.CODE:
            return LeafNode(tag="code",value=text_node.value)
        case TextType.LINK:
            return LeafNode(tag="a",value=text_node.value, props={
                "href": text_node.url
            })
        case TextType.IMAGE:
            return LeafNode(tag="img",value="", props={
                "src": text_node.url,
                "alt": ""
            })

def main():
    print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))
    print(HTMLNode(tag="a", value="click me",props={
        "href": "https://www.google.com",
        "target": "_blank",
    }))

if __name__ == "__main__":
    main()
