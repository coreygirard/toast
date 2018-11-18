import ast
from pprint import pprint

import toast

code = """
def test_source_to_ast_and_back():
    # convert to ast
    f_ast = toast.source_to_ast(f_source)
    assert f_ast == {"name": "f", "args": [], "body": [["Return", ["Num", 0]]]}

    # modify ast
    f_ast["body"][0][1][1] = 1

    # convert back to source
    f_source2 = toast.ast_to_source(f_ast)
"""

code = r"""
def f():
    something = 'aaa\nbbb\nccc'
    f_source = "".join(["def f():", "    return (1 + (2 - 3)) * (4 / 5)", ""])
    f_ast = toast.source_to_ast(f_source)
    assert f_ast == {
        "name": "f",
        "args": [],
        "body": [
            [
                "Return",
                [
                    "Mult",
                    ["Add", ["Num", 1], ["Sub", ["Num", 2], ["Num", 3]]],
                    ["Div", ["Num", 4], ["Num", 5]],
                ],
            ]
        ],
    }
    assert toast.ast_to_source(f_ast) == f_source
"""


print(ast.dump(ast.parse(code).body[0]))

f_ast = toast.source_to_ast(code)
pprint(f_ast)
pprint(toast.ast_to_source(f_ast))
