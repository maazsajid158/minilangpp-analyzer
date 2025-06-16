def generate_TAC(ast):
    code = []
    temp_count = 0

    def new_temp():
        nonlocal temp_count
        temp = f"t{temp_count}"
        temp_count += 1
        return temp

    def visit(node):
        if node.type == "Number":
            return node.value
        elif node.type == "Var":
            return node.value
        elif node.type == "Assign":
            rhs = visit(node.children[0])
            code.append(f"{node.value} = {rhs}")
        elif node.type == "Declare":
            rhs = visit(node.children[0])
            code.append(f"{node.value} = {rhs}")
        elif node.type == "FuncCall":
            args = [visit(arg) for arg in node.children]
            result = new_temp()
            code.append(f"{result} = call {node.value}({', '.join(args)})")
            return result
        elif node.type == "Return":
            val = visit(node.children[0])
            code.append(f"return {val}")
        elif node.type == "BinOp":
            left = visit(node.children[0])
            right = visit(node.children[1])
            result = new_temp()
            code.append(f"{result} = {left} {node.value} {right}")
            return result
        elif node.type == "If":
            cond = visit(node.children[0])
            code.append(f"if {cond} goto THEN")
        for child in node.children:
            if isinstance(child, node.__class__):
                visit(child)

    for tree in ast:
        visit(tree)

    return code
