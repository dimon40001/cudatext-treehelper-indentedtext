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
level1_is_always_node=True
display_leafs=True
respect_markdown_paragraphs=True
exclude_lines_starting_with=---,===
markdown_list_marks=+,-,*,.
```

author: Dmitry Fedorov, https://github.com/dimon40001
license: MIT