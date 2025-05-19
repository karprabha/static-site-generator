from htmlnode import HTMLNode
from textnode import TextNode, TextType


def main():
    print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))
    print(HTMLNode(tag="a", value="click me",props={
        "href": "https://www.google.com",
        "target": "_blank",
    }))

if __name__ == "__main__":
    main()
