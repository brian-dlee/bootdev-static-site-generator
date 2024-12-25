import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        children = [
            LeafNode("b", "a"),
            LeafNode("i", "b"),
            LeafNode("code", "c"),
        ]
        node = ParentNode(children, tag="div")

        self.assertEqual(node.to_html(), f"<div><b>a</b><i>b</i><code>c</code></div>")


if __name__ == "__main__":
    unittest.main()

