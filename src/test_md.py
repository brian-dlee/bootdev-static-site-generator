import unittest

from md import markdown_to_blocks


class MarkdownTestCase(unittest.TestCase):
    def test_markdown_to_blocks(self):
        self.assertEqual(
            markdown_to_blocks(
                """
                # This is a heading

                This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                * This is a list item
                * This is another list item
                """,
            ),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item",
            ]
        )


if __name__ == "__main__":
    unittest.main()
