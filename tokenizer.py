# tokenizer.py

import re

KEYWORDS = {"int", "if", "else", "return"}
SYMBOLS = {"{", "}", "(", ")", ";", ">", "=", ","}

token_specification = [
    ("NUMBER",    r'\d+'),
    ("ID",        r'[A-Za-z_]\w*'),
    ("SYMBOL",    r'[{}();>=,]'),
    ("OP",        r'[+\-*/%]'),
    ("SKIP",      r'[ \t]+'),
    ("NEWLINE",   r'\n'),
    ("MISMATCH",  r'.')
]

token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

def tokenize(code):
    tokens = []
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "NUMBER":
            tokens.append(("NUMBER", value))
        elif kind == "ID":
            if value in KEYWORDS:
                tokens.append(("KEYWORD", value))
            else:
                tokens.append(("ID", value))
        elif kind in ["SYMBOL", "OP"]:
            tokens.append((kind, value))
        elif kind in ["SKIP", "NEWLINE"]:
            continue
        elif kind == "MISMATCH":
            raise RuntimeError(f"Unexpected character {value}")
    return tokens
