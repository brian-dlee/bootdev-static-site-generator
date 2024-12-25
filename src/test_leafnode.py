import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "This is a p tag", {"style": "text-align: center;"})
        self.assertEqual(node.to_html(), f"<p style=\"text-align: center;\" >This is a p tag</p>")


if __name__ == "__main__":
    unittest.main()

