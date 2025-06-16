def check_semantics(ast, symbol_table):
    errors = []
    declared = set(symbol_table.keys())

    def visit(node):
        if node.type == "Var" and node.value not in declared:
            errors.append(f"Undeclared variable: {node.value}")
        for child in node.children:
            if isinstance(child, node.__class__):
                visit(child)

    for tree in ast:
        visit(tree)

    return errors
