import glob
import os
import re
import shutil

from leafnode import LeafNode
from textnode import TextNode


def elipsis(content, length):
    if len(content) > length:
        return content[:length] + "..."

    return content


def rm_glob_recursive(glob_pattern):
    for path in glob.glob(glob_pattern):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def copy_recursive(src, dst):
    if os.path.exists(dst):
        all_dirs = []

        for cwd, dirs, files in os.walk(dst):
            for file in files:
                file_path = os.path.join(cwd, file)
                print("rm    " + file_path)
                os.unlink(file_path)
            for dir in dirs:
                dir_path = os.path.join(cwd, dir)
                all_dirs.append(dir_path)

        for dir_path in reversed(all_dirs):
            print("rmdir " + dir_path)
            os.rmdir(dir_path)

        os.rmdir(dst)

    os.makedirs(dst, exist_ok=True)

    for src_cwd, dirs, files in os.walk(src):
        segments = src_cwd.split(os.sep)
        dst_cwd = os.sep.join([dst, *segments[1:]])

        for dir in dirs:
            dir_path = os.path.join(dst_cwd, dir)
            print(f"mkdir {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
        for file in files:
            input_file = os.path.join(src_cwd, file)
            output_file = os.path.join(dst_cwd, file)
            with open(input_file, "rb") as ifp:
                with open(output_file, "wb") as ofp:
                    print(f"cp    {input_file} -> {output_file}")
                    ofp.write(ifp.read())


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError(f"input node must be a TextNode: {text_node=}")

    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text, None)
        case "bold":
            return LeafNode("b", text_node.text, None)
        case "italic":
            return LeafNode("i", text_node.text, None)
        case "code":
            return LeafNode("code", text_node.text, None)
        case "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "image":
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"unknown TextNode type provided: {text_node.text_type=}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type == "text":
            current_text_node_type = old_node.text_type
            buffer = ""

            for token in as_token_stream(old_node.text):
                if token == delimiter:
                    new_nodes.append(TextNode(buffer, current_text_node_type, None))

                    # if the current symbol list matches the old node text type,
                    # we know we have parsed the end delimiter
                    if old_node.text_type == current_text_node_type:
                        current_text_node_type = text_type
                    else:
                        current_text_node_type = old_node.text_type

                    buffer = ""
                else:
                    buffer += token

            if len(buffer) > 0:
                if current_text_node_type != old_node.text_type:
                    raise ValueError(f"TextNode is missing a close delimiter: {delimiter=}, {old_node.text=}")

                new_nodes.append(TextNode(buffer, current_text_node_type, None))
        else:
            new_nodes.append(old_node)

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type == "text":
            buffer = old_node.text

            for image in extract_markdown_images(buffer):
                head, tail = old_node.text.split(f"![{image[0]}]({image[1]})", maxsplit=1)

                new_nodes.append(TextNode(head, "text", None))
                new_nodes.append(TextNode(image[0], "image", image[1]))

                buffer = tail

            if len(buffer) > 0:
                new_nodes.append(TextNode(buffer, "text", None))
        else:
            new_nodes.append(old_node)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type == "text":
            buffer = old_node.text

            for image in extract_markdown_links(buffer):
                head, tail = old_node.text.split(f"[{image[0]}]({image[1]})", maxsplit=1)

                new_nodes.append(TextNode(head, "text", None))
                new_nodes.append(TextNode(image[0], "link", image[1]))

                buffer = tail

            if len(buffer) > 0:
                new_nodes.append(TextNode(buffer, "text", None))
        else:
            new_nodes.append(old_node)

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, "text", None)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    nodes = split_nodes_delimiter(nodes, "_", "italic")
    nodes = split_nodes_delimiter(nodes, "`", "code")

    return nodes


def extract_markdown_images(text):
    results = []

    for match in re.finditer(r"!\[(.*?)\]\((.*?)\)", text):
        results.append((match.group(1), match.group(2)))

    return results


def extract_markdown_links(text):
    results = []

    for match in re.finditer(r"\[(.*?)\]\((.*?)\)", text):
        results.append((match.group(1), match.group(2)))

    return results


def as_token_stream(text):
    cursor = 0
    buffer = ""

    while cursor < len(text):
        char = text[cursor]

        if char in ("*", "`", "_"):
            if len(buffer) > 0:
                yield buffer
                buffer = ""

        if char == "`":
            yield char
            cursor += 1
            continue

        if char == "*":
            if cursor + 1 < len(text) and text[cursor + 1] == "*":
                yield "**"
                cursor += 2
            else:
                yield "*"
                cursor += 1

            continue

        if char == "_":
            yield "_"
            cursor += 1
            continue

        buffer += char
        cursor += 1

    if len(buffer) > 0:
        yield buffer
