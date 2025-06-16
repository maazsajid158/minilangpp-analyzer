from tokenizer import tokenize

class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children or []

    def __repr__(self, level=0):
        indent = '  ' * level
        children_str = ''.join(child.__repr__(level+1) if isinstance(child, ASTNode) else str(child) for child in self.children)
        return f"{indent}{self.type}({self.value})\n{children_str}"

symbol_table = {}

def parse_tokens(tokens):
    ast = []
    i = 0

    def expect(expected_type, expected_value=None):
        nonlocal i
        if i >= len(tokens):
            raise SyntaxError("Unexpected end of input")
        token_type, token_value = tokens[i]
        if token_type != expected_type or (expected_value and token_value != expected_value):
            raise SyntaxError(f"Expected {expected_type} {expected_value}, got {token_type} {token_value}")
        i += 1
        return token_value

    def parse_function():
        nonlocal i
        expect("KEYWORD", "int")
        func_name = expect("ID")
        expect("SYMBOL", "(")
        params = []
        while i < len(tokens) and tokens[i][1] != ")":
            if tokens[i][1] == ",":
                i += 1
            if i < len(tokens) and tokens[i][1] == ")":
                break
            param_type = expect("KEYWORD", "int")
            param_name = expect("ID")
            params.append((param_type, param_name))
            symbol_table[param_name] = param_type
        expect("SYMBOL", ")")
        expect("SYMBOL", "{")
        body = []
        while i < len(tokens) and tokens[i][1] != "}":
            stmt = parse_statement()
            body.append(stmt)
        expect("SYMBOL", "}")
        return ASTNode("Function", func_name, [ASTNode("Params", params), ASTNode("Body", None, body)])

    def parse_statement():
        nonlocal i
        if tokens[i][1] == "int":
            return parse_declaration()
        elif tokens[i][1] == "if":
            return parse_if()
        elif tokens[i][1] == "return":
            i += 1
            expr = parse_expression()
            expect("SYMBOL", ";")
            return ASTNode("Return", None, [expr])
        elif tokens[i][0] == "ID":
            var = tokens[i][1]
            i += 1
            expect("SYMBOL", "=")
            expr = parse_expression()
            expect("SYMBOL", ";")
            return ASTNode("Assign", var, [expr])
        else:
            raise SyntaxError(f"Unknown statement: {tokens[i]}")

    def parse_declaration():
        nonlocal i
        expect("KEYWORD", "int")
        var_name = expect("ID")
        expect("SYMBOL", "=")
        expr = parse_expression()
        expect("SYMBOL", ";")
        symbol_table[var_name] = "int"
        return ASTNode("Declare", var_name, [expr])

    def parse_if():
        nonlocal i
        expect("KEYWORD", "if")
        expect("SYMBOL", "(")
        condition = parse_expression()
        expect("SYMBOL", ")")
        expect("SYMBOL", "{")
        then_branch = []
        while i < len(tokens) and tokens[i][1] != "}":
            then_branch.append(parse_statement())
        expect("SYMBOL", "}")
        else_branch = []
        if i < len(tokens) and tokens[i][1] == "else":
            i += 1
            expect("SYMBOL", "{")
            while i < len(tokens) and tokens[i][1] != "}":
                else_branch.append(parse_statement())
            expect("SYMBOL", "}")
        return ASTNode("If", None, [condition, ASTNode("Then", None, then_branch), ASTNode("Else", None, else_branch)])

    def parse_expression():
        def parse_primary():
            nonlocal i
            if tokens[i][0] == "NUMBER":
                val = tokens[i][1]
                i += 1
                return ASTNode("Number", val)
            elif tokens[i][0] == "ID":
                val = tokens[i][1]
                i += 1
                if i < len(tokens) and tokens[i][1] == "(":
                    i += 1
                    args = []
                    while i < len(tokens) and tokens[i][1] != ")":
                        if tokens[i][1] == ",":
                            i += 1
                        args.append(parse_expression())
                    expect("SYMBOL", ")")
                    return ASTNode("FuncCall", val, args)
                return ASTNode("Var", val)
            else:
                raise SyntaxError(f"Invalid expression near {tokens[i]}")

        def parse_binary_expression():
            nonlocal i
            left = parse_primary()
            while i < len(tokens) and tokens[i][0] == "OP":
                op = tokens[i][1]
                i += 1
                right = parse_primary()
                left = ASTNode("BinOp", op, [left, right])
            return left

        return parse_binary_expression()

    while i < len(tokens):
        ast.append(parse_function())

    return ast, symbol_table
