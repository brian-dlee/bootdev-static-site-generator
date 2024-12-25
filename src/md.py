import logging

from parentnode import ParentNode
from leafnode import LeafNode
from utils import elipsis, text_node_to_html_node, text_to_textnodes


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]

    raise Exception("The provided markdown does not contain an h1 level heading tag")


def markdown_to_blocks(markdown):
    blocks = []
    buffer = ""

    for line in markdown.split("\n"):
        if len(line.strip()) == 0:
            if len(buffer.strip()) > 0:
                blocks.append(buffer.rstrip())
                buffer = ""
            continue

        buffer += line.strip() + "\n"

    if len(buffer.strip()) > 0:
        blocks.append(buffer.strip())

    return blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    root_node = ParentNode("div", children)

    for block_i, block in enumerate(blocks):
        block_type = block_to_block_type(block)

        logging.debug(f"Block {block_i}: {block_type=} {elipsis(block, 36)!r}")

        match block_type:
            case "heading":
                node = LeafNode(get_h_tag(block), block.lstrip("# "))
            case "code":
                node = LeafNode("code", block.strip("`").strip())
            case "quote":
                node = LeafNode("blockquote", strip_block_quote_markers(block))
            case "unordered_list":
                ul_children = []

                for li in extract_unordered_list_items(block):
                    li_children = []

                    for t in text_to_textnodes(li):
                        li_children.append(text_node_to_html_node(t))

                    ul_children.append(ParentNode("li", li_children))

                node = ParentNode("ul", ul_children)
            case "ordered_list":
                ol_children = []

                for li in extract_ordered_list_items(block):
                    li_children = []

                    for t in text_to_textnodes(li):
                        li_children.append(text_node_to_html_node(t))

                    ol_children.append(ParentNode("li", li_children))

                node = ParentNode("ol", ol_children)
            case "paragraph":
                p_children = []

                for t in text_to_textnodes(block):
                    p_children.append(text_node_to_html_node(t))

                node = ParentNode("p", p_children)

        children.append(node)

    return root_node


def extract_ordered_list_items(block):
    elements = []
    for line in block.split("\n"):
        prefix = f"{len(elements) + 1}. "
        if line.startswith(prefix):
            elements.append(line[len(prefix) :].strip())
        elif len(elements) > 0:
            elements[-1] += " " + line.strip()
    return elements


def extract_unordered_list_items(block):
    elements = []
    for line in block.split("\n"):
        if line.startswith("- ") or line.startswith("* "):
            elements.append(line[2:].strip())
        elif len(elements) > 0:
            elements[-1] += " " + line.strip()
    return elements


def get_h_tag(block):
    degree = 0
    for char in block:
        if char == "#":
            degree += 1
        else:
            break

    assert 1 <= degree <= 6, "H1 through H6 are the only valid header tags"

    return f"h{degree}"


def strip_block_quote_markers(block):
    content = ""
    for line in block.split("\n"):
        content += line.lstrip(">").strip() + " "
    return content.rstrip()


def block_to_block_type(markdown):
    for i in range(6):
        if markdown.startswith("#" * i + " "):
            return "heading"

    if markdown.startswith("```") and markdown.endswith("```"):
        return "code"

    lines = markdown.split("\n")

    if all([line.startswith("> ") for line in lines]):
        return "quote"

    if all([line.startswith("* ") or line.startswith("- ") for line in lines]):
        return "unordered_list"

    order_list_number = 1
    is_ordered_list = True
    for line in lines:
        if line.startswith(f"{order_list_number}. "):
            order_list_number += 1
        else:
            is_ordered_list = False

    if is_ordered_list:
        return "ordered_list"

    return "paragraph"
