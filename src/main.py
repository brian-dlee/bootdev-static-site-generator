import logging
import os

from textnode import TextNode
from utils import copy_recursive, rm_glob_recursive
from generate import generate_pages_recursive


def main():
    level = logging.DEBUG if os.getenv("DEBUG") == "1" else logging.INFO
    logging.basicConfig(level=level)

    rm_glob_recursive("public/*")
    print(TextNode("This is a text node", "bold", "https://www.boot.dev"))
    copy_recursive("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
