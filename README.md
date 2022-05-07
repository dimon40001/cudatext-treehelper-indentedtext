# CudaText TreeHelper plugin for "Text IMproved" lexer

Builds code tree based on idea of indentation (Python-like tabs or 4x spaces) with some additional configurable features
like icon selection, ability to recognize paragraphs and show or hide lines with particular prefixes.

Recommended for Text IMproved lexer but works with any sort of indented text

Configurable through `plugins.ini` file

```ini
[cuda_tree_indentedtext]
node_icon=0
leaf_icon=6
max_tree_text_length=40
always_show_root_level_as_node_icon=True
display_leaves=True
paragraphs_separated_by_empty_line=True
hide_lines_with_prefixes=---,===
always_show_items_with_prefixes=+,-,*,.
```

author: Dmitry Fedorov, https://github.com/dimon40001
license: MIT
