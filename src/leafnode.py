from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is not None and not isinstance(self.value, str):
            raise ValueError(f"invalid value: {self.value=}")

        value = self.value or ""

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{value}</{self.tag}>"
