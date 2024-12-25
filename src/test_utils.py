import unittest

from textnode import TextNode
from utils import as_token_stream, extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


class UtilsTestCase(unittest.TestCase):
    def test_as_symbol_stream(self):
        self.assertEqual(
            list(as_token_stream("a **new** node with *inline elements* to `split` off")),
            [
                "a ",
                "**",
                "new",
                "**",
                " node with ",
                "*",
                "inline elements",
                "*",
                " to ",
                "`",
                "split",
                "`",
                " off"
            ]
        )

    def test_split_nodes_delimiter(self):
        self.assertEqual(
            split_nodes_delimiter(
                [
                    TextNode("a **new** node with *inline elements* to `split` off", "text", None),
                ],
                "*",
                "italic"
            ),
            [
                TextNode("a **new** node with ", "text", None),
                TextNode("inline elements", "italic", None),
                TextNode(" to `split` off", "text", None),
            ]
        )

    def test_split_nodes_image(self):
        self.assertEqual(
            split_nodes_image(
                [
                    TextNode("an ![image](https://site.com/image.png) I love", "text", None),
                ],
            ),
            [
                TextNode("an ", "text", None),
                TextNode("image", "image", "https://site.com/image.png"),
                TextNode(" I love", "text", None),
            ]
        )

    def test_split_nodes_link(self):
        self.assertEqual(
            split_nodes_link(
                [
                    TextNode("a [site](https://site.com) I hate", "text", None),
                ],
            ),
            [
                TextNode("a ", "text", None),
                TextNode("site", "link", "https://site.com"),
                TextNode(" I hate", "text", None),
            ]
        )

    def test_extract_markdown_images(self):
        self.assertEqual(
            extract_markdown_images("abc ![alt](https://site.com/image.png) def"),
            [
                ("alt", "https://site.com/image.png")
            ]
        )

    def test_extract_markdown_links(self):
        self.assertEqual(
            extract_markdown_links("abc [alt](https://site.com) def"),
            [
                ("alt", "https://site.com")
            ]
        )

    def test_text_to_textnodes(self):
        self.assertEqual(
            text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"),
            [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://boot.dev"),
            ]
        )

if __name__ == "__main__":
    unittest.main()

