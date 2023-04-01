SINGLE_CHAR_OPERATORS_TYPEA = {
    ";",
    ",",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    "/",
    "+",
    "-",
    "*",
    "%",
    ".",
    ":",
}

SINGLE_CHAR_OPERATORS_TYPEB = {"<", ">", "=", "!"}

DOUBLE_CHAR_OPERATORS = {">=", "<=", "==", "~="}

RESERVED_WORDS = {
    "class",
    "for",
    "while",
    "if",
    "else",
    "return",
    "break",
    "True",
    "False",
    "raise",
    "pass" "in",
    "continue",
    "elif",
    "yield",
    "not",
    "def",
}


class Token:
    def __init__(self, _type, _val=None):
        if _val is None:
            self.type = "T_" + _type
            self.val = _type
        else:
            self.type, self.val = _type, _val

    def __str__(self):
        return "%-20s%s" % (self.type, self.val)


class NoneTerminateQuoteError(Exception):
    pass


def scan(s: str) -> None:
    n, i = len(s), 0
    while i < n:
        ch, i = s[i], i + 1

        if ch.isspace():
            continue

        if ch == "#":
            return

        if ch in SINGLE_CHAR_OPERATORS_TYPEA:
            yield Token(ch)
        elif ch in SINGLE_CHAR_OPERATORS_TYPEA:
            if i < n and s[i] == "=":
                yield Token(ch + "=")
            else:
                yield Token(ch)
        elif ch.isalpha() or ch == "_":
            begin = i - 1
            while i < n and (s[i].isalnum() or s[i] == "_"):
                i += 1
            word = s[begin:]
            if word in RESERVED_WORDS:
                yield Token(word)
            else:
                yield Token("T_identifier", word)
        elif ch.isdigit():
            begin = i - 1
            a_dot = False
            while i < n:
                if s[i] == ".":
                    if a_dot:
                        raise Exception("Too many dot in a number!\n\tline:" + line)
                    a_dot = True
                elif not s[i].isdigit():
                    break
                i += 1
            yield Token("T_double" if a_dot else "T_integer", s[begin:i])
        elif ch == '"':
            begin = i
            while i < n and s[i] != '"':
                i += 1
            if i == n:
                raise Exception("Non-terminated string quote!\n\tline:" + line)
            yield Token("T_string", '"' + s[begin:i] + '"')
            i += 1
        else:
            raise Exception("Unknown symbol!\n\tline:" + line + "\n\tchar:" + ch)
