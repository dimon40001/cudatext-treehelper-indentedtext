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

always_show_root_level_as_node_icon=True
    Always show root level (levels are 1-numbered) icon as node

display_leaves=True
    Display items considered to be final leaves. Typcally it means items not containing other subitems.
    Option may clutter the tree with lots of items.

paragraphs_separated_by_empty_line=True
    Respect Markdown paragraphs (lines of text irrespective of line breaks separated by one or more empty lines). And
    make tree item only from the first line of the text block.

    This is example of
    a single paragraph
    as seen by Markdown
    Next comes second paragraph

    Separated with an empty line.

hide_lines_with_prefixes=---,===
    Comma-separated values.
    Can be used as visual separator is not part of the tree and can be used as comment over the new block

always_show_items_with_prefixes=+,-,*,.
    This is useful when `paragraphs_separated_by_empty_line` is enabled. So that lists (Markdown style) are still
    rendered as separate items even if there is no empty line between them.

    In the example below all items will be present in the tree if this option is configured.
    Otherwise all items will "collaps" as a single paragraph named "+item1" because there's no empty lines in between.

    Somelist:
        +item1
        *item2
        -item3
        .item4
