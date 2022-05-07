import os
from math import floor
from cudatext import *

tab_size = 4
op_file = "plugins.ini"
op_section = "cuda_tree_indentedtext"
fn_config = os.path.join(app_path(APP_DIR_SETTINGS), op_file)


def str_to_bool(string):
    return string.upper() in ("TRUE", "YES", "1")


'''
gets tuples in format
((x1, y1, x2, y2), level, title, icon)
'''


def get_headers(filename, lines):
    def get_level(line):
        line = str.expandtabs(line, tab_size)
        spaces_count = len(line) - len(str.lstrip(line))
        if spaces_count % tab_size == 0:
            level = 1 + floor(spaces_count / tab_size)
        else:
            level = -1
        return level

    def is_empty_line(line):
        stripped = str.strip(line)
        line_is_empty = len(stripped) == 0
        if line_is_empty:
            return True
        for ignore_line_prefix in op_exclude_lines_starting_with.split(","):
            if stripped.startswith(ignore_line_prefix):
                return True
        return False

    op_node_icon = int(ini_read(op_file, op_section, "node_icon", "0"))
    op_leaf_icon = int(ini_read(op_file, op_section, "leaf_icon", "6"))
    op_max_tree_text_length = int(ini_read(op_file, op_section, "max_tree_text_length", "40"))

    op_level1_is_always_node = str_to_bool(ini_read(op_file, op_section, "level1_is_always_node", "True"))
    op_display_leaves = str_to_bool(ini_read(op_file, op_section, "display_leaves", "True"))
    op_respect_markdown_paragraphs = str_to_bool(ini_read(op_file, op_section, "respect_markdown_paragraphs", "True"))

    op_exclude_lines_starting_with = ini_read(op_file, op_section, "exclude_lines_starting_with", "---,===")
    op_markdown_list_marks = ini_read(op_file, op_section, "markdown_list_marks", "+,-,*,.")

    r = []
    i = -1
    while i < len(lines):
        i = i + 1

        # check if reached end of file
        if i >= len(lines):
            break

        # parse current line
        line = str.expandtabs(lines[i], tab_size)  # required for making proper tree text
        text = str.strip(line)
        level = get_level(line)
        text_position = len(lines[i]) - len(str.lstrip(lines[i]))
        if len(text) > op_max_tree_text_length:
            text = text[:op_max_tree_text_length] + "..."

        # skip empty lines and improperly tabulated
        if is_empty_line(line) or level == -1:
            continue

        # THEN we have to determine if it's a leaf or not
        # find position of first non-empty line after line-in-question
        i2 = i + 1
        while i2 < len(lines):
            if is_empty_line(lines[i2]):
                i2 = i2 + 1
            else:
                break

        # if we have reached end of file then do nothing, otherwise create nodes
        if i2 < len(lines):
            level_next = get_level(lines[i2])
        else:
            level_next = 0  # meaning there will be no more leaves or subnodes

        # if next line is deeper - it's a node
        if level_next > level:
            r.append(((text_position, i, text_position, i + 1), level, text, op_node_icon))
        # if next line is same, out line is leaf -> decide on markdown
        # if next line is shallower - current is a leaf
        else:

            # decide for icon for Level1 if configured
            if level == 1 and op_level1_is_always_node:
                icon = op_node_icon
            else:
                icon = op_leaf_icon

            # create leaf if it's configured if not (op_respect_markdown_paragraphs and i2 == i+1): 
            if op_display_leaves:
                prev_line = lines[i - 1]

                should_consider_as_item = True

                # dont add the leaf if respecting markdown
                if (not is_empty_line(prev_line)) and (
                        level == get_level(prev_line)) and op_respect_markdown_paragraphs:

                    should_consider_as_item = False

                    # extra check for settings of markdown lists
                    if not is_empty_line(op_markdown_list_marks):
                        for force_include_line_prefix in op_markdown_list_marks.split(","):
                            if str.lstrip(lines[i]).startswith(force_include_line_prefix):
                                should_consider_as_item = True
                                break

                if should_consider_as_item:
                    r.append(((text_position, i, text_position, i + 1), level, text, icon))

    return r


class Command:
    op_node_icon = 0
    op_leaf_icon = 6
    op_level1_is_always_node = True
    op_display_leaves = True
    op_respect_markdown_paragraphs = True
    op_exclude_lines_starting_with = "---,==="
    op_max_tree_text_length = 40
    op_markdown_list_marks = "+,-,*,."

    def __init__(self):
        self.load_ops()

    def load_ops(self):
        op_node_icon = int(ini_read(op_file, op_section, "node_icon", str(self.op_node_icon)))
        op_leaf_icon = int(ini_read(op_file, op_section, "leaf_icon", str(self.op_leaf_icon)))
        op_max_tree_text_length = int(
            ini_read(op_file, op_section, "max_tree_text_length", str(self.op_max_tree_text_length)))

        op_level1_is_always_node = str_to_bool(
            ini_read(op_file, op_section, "level1_is_always_node", str(self.op_level1_is_always_node)))
        op_display_leaves = str_to_bool(ini_read(op_file, op_section, "display_leaves", str(self.op_display_leaves)))
        op_respect_markdown_paragraphs = str_to_bool(
            ini_read(op_file, op_section, "respect_markdown_paragraphs", str(self.op_respect_markdown_paragraphs)))

        op_exclude_lines_starting_with = ini_read(op_file, op_section, "exclude_lines_starting_with",
                                                  self.op_exclude_lines_starting_with)
        op_markdown_list_marks = ini_read(op_file, op_section, "markdown_list_marks", self.op_markdown_list_marks)

    def save_ops(self):
        ini_write(fn_config, op_section, 'node_icon', str(self.op_node_icon))
        ini_write(fn_config, op_section, 'leaf_icon', str(self.op_leaf_icon))
        ini_write(fn_config, op_section, 'max_tree_text_length', str(self.op_max_tree_text_length))

        ini_write(fn_config, op_section, 'level1_is_always_node', str(self.op_level1_is_always_node))
        ini_write(fn_config, op_section, 'display_leaves', str(self.op_display_leaves))
        ini_write(fn_config, op_section, 'respect_markdown_paragraphs', str(self.op_respect_markdown_paragraphs))

        ini_write(fn_config, op_section, 'exclude_lines_starting_with', self.op_exclude_lines_starting_with)
        ini_write(fn_config, op_section, 'markdown_list_marks', self.op_markdown_list_marks)

    def config(self):
        self.save_ops()
        file_open(fn_config)
