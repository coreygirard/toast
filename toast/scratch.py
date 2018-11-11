import ast
from pprint import pprint

import astor


def deconstruct_Return(line):
    return ["Return", deconstruct_recurse(line.value)]


def deconstruct_BinOp(line):
    return [
        type(line.op).__name__,
        deconstruct_recurse(line.left),
        deconstruct_recurse(line.right),
    ]


def deconstruct_Name(line):
    return ["Name", line.id]


def deconstruct_Num(line):
    return ["Num", line.n]


def deconstruct_Assign(line):
    return [
        "Assign",
        deconstruct_recurse(line.targets),
        deconstruct_recurse(line.value),
    ]


def deconstruct_recurse(line):
    if isinstance(line, list):
        return [deconstruct_recurse(e) for e in line]

    typ = type(line).__name__
    if typ == "Return":
        return deconstruct_Return(line)
    elif typ == "BinOp":
        return deconstruct_BinOp(line)
    elif typ == "Name":
        return deconstruct_Name(line)
    elif typ == "Assign":
        return deconstruct_Assign(line)
    elif typ == "Num":
        return deconstruct_Num(line)

    raise TypeError(f"'{typ}' not handled")


def deconstruct_function(code):
    parsed_ast = ast.parse(code)
    o = parsed_ast.body[0].body
    return {
        "name": parsed_ast.body[0].name,
        "args": [a.arg for a in parsed_ast.body[0].args.args],
        "body": [deconstruct_recurse(line) for line in o],
    }


def reconstruct_recurse(a):
    head, *rest = a

    if head == "Return":
        return ast.Return(value=reconstruct_recurse(rest[0]))
    elif head == "Name":
        return ast.Name(rest[0], None)
    elif head == "Assign":
        return ast.Assign(
            targets=[reconstruct_recurse(rest[0][0])],
            value=reconstruct_recurse(rest[1]),
        )
    elif head == "Add":
        return ast.BinOp(
            left=reconstruct_recurse(rest[0]),
            op=ast.Add(),
            right=reconstruct_recurse(rest[1]),
        )

    raise TypeError(f"'{head}' not handled")


def reconstruct_function(a):
    code = """def f(a):
        return a + (b + c)
    """
    parsed_ast = ast.parse(code)

    parsed_ast.body[0].name = a["name"]
    parsed_ast.body[0].args.args = [ast.arg(a, None) for a in a["args"]]
    parsed_ast.body[0].body = [reconstruct_recurse(e) for e in a["body"]]

    return astor.to_source(parsed_ast)


'''
code = """def f(a):
    return a
"""

a = [
    ast.Return(value=ast.Name('a', None))
]

decon = deconstruct_function(code)
#pprint('decon', str(decon))
#o = reconstruct_function(decon)
#print(o)
#print(astor.to_source(o))
'''
