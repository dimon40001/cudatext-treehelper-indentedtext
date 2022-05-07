from math import floor


def get_level(line):
    line = str.expandtabs(line, tabsize=4)
    spaces_count = len(line) - len(str.lstrip(line))
    level = 1 + floor(spaces_count / 4)
    return level


def get_headers(filename, lines):
    '''
    gets tuples in format
    ((x1, y1, x2, y2), level, title, icon)

    field "icon": 0-based index of icon from standard imagelist, or -1 if icon not used.
        0: folder
        1: parts1
        2: parts2
        3: parts3
        4: box
        5: func
        6: arrow1
        7: arrow2
    '''

    # opt_icon = ini_read(filename, section, keyname, value)
    # opt_ignore_odd tabulation
    # opt_tab size

    r = []
    i = 0
    while i < len(lines):
        line = lines[i]
        level = get_level(line)

        full_stripped = str.strip(line)
        if len(full_stripped) == 0:
            i = i + 1
            continue

        spaces_count = len(line) - len(str.lstrip(line))
        if spaces_count % 4 != 0:
            i = i + 1
            continue

        i2 = i + 1
        while i2 < len(lines):
            level_next = get_level(lines[i2])
            # goto first non-empty line
            if level_next != level:
                break
            i2 = i2 + 1
        # if next line is same, out line is leaf
        # if next line is deeper - it's node
        # if next line is shallower - it's a leaf

        if level_next > level:
            node_text = "L" + str(level) + " - " + full_stripped[:20]
            icon = 0
            r.append(((0, i, 0, i + 1), level, node_text, icon))
        else:
            node_text = "L" + str(level) + " - " + full_stripped[:20]
            icon = -1
            r.append(((0, i, 0, i + 1), level, node_text, icon))
        i = i + 1
    return r
