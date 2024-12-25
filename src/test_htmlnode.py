import unittest

from htmlnode import HTMLNode


class HTMLNodeTestCase(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", None, None, {"href": "http://site.com"})

        self.assertEqual(node.props_to_html(), " href=\"http://site.com\" ")


if __name__ == "__main__":
    unittest.main()

