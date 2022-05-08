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

    def get_leaf_icon(level):
        if level == 1 and op_always_show_root_level_as_node_icon:
            icon = op_node_icon
        else:
            icon = op_leaf_icon
        return icon

    def line_starts_with(line, prefixes):
        if len(prefixes) != 0:
            for prefix in prefixes.split(","):
                if str.lstrip(line).startswith(prefix):
                    return True
        return False

    def is_empty_line(line):
        return len(str.strip(line)) == 0 or line_starts_with(line, op_hide_lines_with_prefixes)

    def get_level(line):
        line = str.expandtabs(line, tab_size)
        space_count = len(line) - len(str.lstrip(line))
        if space_count % tab_size == 0 and not is_empty_line(line):
            level = 1 + floor(space_count / tab_size)
        else:
            level = -1
        return level

    def get_item_text(l3):
        item_text = str.strip(l3)
        if len(item_text) > op_max_tree_text_length:
            item_text = item_text[:op_max_tree_text_length] + "..."
        return item_text

    op_node_icon = int(ini_read(op_file, op_section, "node_icon", "0"))
    op_leaf_icon = int(ini_read(op_file, op_section, "leaf_icon", "6"))
    op_max_tree_text_length = int(ini_read(op_file, op_section, "max_tree_text_length", "40"))

    op_always_show_root_level_as_node_icon = str_to_bool(
        ini_read(op_file, op_section, "always_show_root_level_as_node_icon", "True"))
    op_display_leaves = str_to_bool(ini_read(op_file, op_section, "display_leaves", "True"))
    op_paragraphs_separated_by_empty_line = str_to_bool(
        ini_read(op_file, op_section, "paragraphs_separated_by_empty_line", "True"))

    op_hide_lines_with_prefixes = ini_read(op_file, op_section, "hide_lines_with_prefixes", "---,===")
    op_always_show_items_with_prefixes = ini_read(op_file, op_section, "always_show_items_with_prefixes", "+,-,*,.")

    r = []
    i = -1
    lines_count = len(lines)
    while i < lines_count:
        i = i + 1

        if i >= lines_count:
            break

        line = str.expandtabs(lines[i], tab_size)  # required for making proper tree text
        level = get_level(line)
        text_position = len(lines[i]) - len(str.lstrip(lines[i]))
        text = get_item_text(line)

        if level < 1:
            continue

        i2 = i + 1
        while i2 < lines_count:
            while is_empty_line(lines[i2]) or get_level(lines[i2]) < 1:
                i2 = i2 + 1

            if op_paragraphs_separated_by_empty_line and level == get_level(lines[i2]):
                if not line_starts_with(lines[i2], op_always_show_items_with_prefixes):
                    i2 = i2 + 1
                else:
                    break
            else:
                break

        # if we have reached end of file then do nothing, otherwise create nodes
        if i2 < lines_count:
            next_level = get_level(lines[i2])
        else:
            next_level = -1  # meaning there will be no more leaves or subnodes

        # if next line is deeper - it's a node
        if next_level > level:
            r.append(((text_position, i, text_position, i + 1), level, text, op_node_icon))

            # skip to already known next relevant position and get back, since counter will be increased
            # in the beginning of next iteration
            i = i2 - 1

        # if next line is same, out line is leaf -> decide on markdown
        # if next line is shallower - current is a leaf
        else:
            icon = get_leaf_icon(level)

            # create leaf if it's configured if not (op_paragraphs_separated_by_empty_line and i2 == i+1): 
            if op_display_leaves:
                # add leaf and if paragraphs are respected - skip items with same level and not starting with prefix
                r.append(((text_position, i, text_position, i + 1), level, text, icon))

                # skip same level items
                if op_paragraphs_separated_by_empty_line:
                    while i + 1 < lines_count and level == get_level(lines[i + 1]):
                        if not line_starts_with(lines[i + 1], op_always_show_items_with_prefixes):
                            i = i + 1
                        else:
                            break

    return r


class Command:
    op_node_icon = 0
    op_leaf_icon = 6
    op_always_show_root_level_as_node_icon = True
    op_display_leaves = True
    op_paragraphs_separated_by_empty_line = True
    op_hide_lines_with_prefixes = "---,==="
    op_max_tree_text_length = 40
    op_always_show_items_with_prefixes = "+,-,*,."

    def __init__(self):
        self.load_ops()

    def load_ops(self):
        op_node_icon = int(ini_read(op_file, op_section, "node_icon", str(self.op_node_icon)))
        op_leaf_icon = int(ini_read(op_file, op_section, "leaf_icon", str(self.op_leaf_icon)))
        op_max_tree_text_length = int(
            ini_read(op_file, op_section, "max_tree_text_length", str(self.op_max_tree_text_length)))

        op_always_show_root_level_as_node_icon = str_to_bool(
            ini_read(op_file, op_section, "always_show_root_level_as_node_icon",
                     str(self.op_always_show_root_level_as_node_icon)))
        op_display_leaves = str_to_bool(ini_read(op_file, op_section, "display_leaves", str(self.op_display_leaves)))
        op_paragraphs_separated_by_empty_line = str_to_bool(
            ini_read(op_file, op_section, "paragraphs_separated_by_empty_line",
                     str(self.op_paragraphs_separated_by_empty_line)))

        op_hide_lines_with_prefixes = ini_read(op_file, op_section, "hide_lines_with_prefixes",
                                               self.op_hide_lines_with_prefixes)
        op_always_show_items_with_prefixes = ini_read(op_file, op_section, "always_show_items_with_prefixes",
                                                      self.op_always_show_items_with_prefixes)

    def save_ops(self):
        ini_write(fn_config, op_section, 'node_icon', str(self.op_node_icon))
        ini_write(fn_config, op_section, 'leaf_icon', str(self.op_leaf_icon))
        ini_write(fn_config, op_section, 'max_tree_text_length', str(self.op_max_tree_text_length))

        ini_write(fn_config, op_section, 'always_show_root_level_as_node_icon',
                  str(self.op_always_show_root_level_as_node_icon))
        ini_write(fn_config, op_section, 'display_leaves', str(self.op_display_leaves))
        ini_write(fn_config, op_section, 'paragraphs_separated_by_empty_line',
                  str(self.op_paragraphs_separated_by_empty_line))

        ini_write(fn_config, op_section, 'hide_lines_with_prefixes', self.op_hide_lines_with_prefixes)
        ini_write(fn_config, op_section, 'always_show_items_with_prefixes', self.op_always_show_items_with_prefixes)

    def config(self):
        self.save_ops()
        file_open(fn_config)
