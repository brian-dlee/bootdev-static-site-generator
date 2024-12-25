class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_html(self):
        if self.props:
            return " " + " ".join([f'{k}="{v}"' for k, v in self.props.items()]) + " "
        return ""

    def to_html(self):
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.tag=}, {self.value=}, {self.children=}, {self.props=}"
