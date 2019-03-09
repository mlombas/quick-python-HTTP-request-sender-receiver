def print_json(json, func=print, indent_char=" "):
    indent_level = 0
    in_string = "" #stores the type of quotes the string we are inside has or empty string if not in string
    line = ""
    def flush():
        nonlocal line
        func(indent_char * indent_level + line)
        line = ""

    for c in json:
        if c in "\"\'":
            if c == in_string:
                in_string = ""
            elif in_string == "":
                in_string = c
                    
        if in_string:
            line += c
        elif not c.isspace():
            line += c
            if c in "([{":
                flush()
                indent_level += 1
            elif c in ")]}":
                line = line[:-1]
                flush()
                indent_level -= 1
                line += c
            elif c == ",":
                flush()
    flush()

