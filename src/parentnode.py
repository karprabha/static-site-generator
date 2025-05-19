from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required!")

        if not self.children:
            raise ValueError("children is required!")

        return f"<{self.tag}>{''.join(map(lambda x: x.to_html(), self.children))}</{self.tag}>"
