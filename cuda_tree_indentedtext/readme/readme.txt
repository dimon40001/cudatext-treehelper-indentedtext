TreeHelper plugin for "Text IMproved" lexer

author: Dmitry Fedorov, https://github.com/dimon40001
license: MIT

Builds code tree based on idea of indentation (Python-like tabs or 4x spaces) with some additional configurable features
like icon selection, ability to recognize paragraphs and show or hide lines with particular prefixes.

Recommended for Text IMproved lexer but works well with any sort of indented text.

Configurable through `plugins.ini` file, section `cuda_tree_indentedtext`.

Configurable parameters with default values:

node_icon=0
    Icon to display for the node in tree. -1 to show no icon.

leaf_icon=6
    Icon to display for the leaf in tree. -1 to show no icon.

max_tree_text_length=40
    Max length of the item text in the tree. Otherwise truncated to specified length and adds "..."

level1_is_always_node=True
    Always show root level (levels are 1-numbered) icon as node

display_leafs=True

respect_markdown_paragraphs=True

exclude_lines_starting_with=---,===
    Comma-separated values.
    Can be used as visual separator is not part of the tree and can be used as comment over the new block

markdown_list_marks=+,-,*,.
