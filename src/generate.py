import logging
import os
import pathlib

from md import extract_title, markdown_to_html_node
from utils import elipsis


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as fp:
        source_contents = fp.read()

    with open(template_path) as fp:
        template_contents = fp.read()

    logging.debug(f"Reading {elipsis(source_contents, 36)!r}")

    node = markdown_to_html_node(source_contents)

    logging.debug(f"Encoding node to html {node!r}")

    html = node.to_html()
    title = extract_title(source_contents)

    response = template_contents
    response = response.replace("{{ Title }}", title)
    response = response.replace("{{ Content }}", html)

    with open(dest_path, "w") as fp:
        fp.write(response)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    src_root_path = pathlib.Path(dir_path_content)
    dst_root_path = pathlib.Path(dest_dir_path)

    for cwd, _, files in src_root_path.walk():
        for file in map(pathlib.Path, files):
            src_file_path = cwd / file
            dst_file_path = dst_root_path / strip_prefix_path(cwd, src_root_path) / file.with_suffix(".html")

            if file.suffix.lower() == ".md":
                os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)

                generate_page(src_file_path, template_path, dst_file_path)


def strip_prefix_path(path, prefix):
    return pathlib.Path(*path.parts[len(prefix.parts) :])
