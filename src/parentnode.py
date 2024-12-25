import logging

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not isinstance(self.tag, str):
            raise ValueError(f"invalid tag value: {self.tag=}")

        if not isinstance(self.children, list):
            raise ValueError(f"invalid children value: {self.children=}")

        result = f"<{self.tag}{self.props_to_html()}>"

        for i, child in enumerate(self.children):
            if not isinstance(child, HTMLNode):
                raise ValueError(f"invalid child, all children must extend HTMLNode: {i=}, {child=}")

            logging.debug(f"Encoding child node to html {child!r}")

            result += child.to_html()

        result += f"</{self.tag}>"

        return result
