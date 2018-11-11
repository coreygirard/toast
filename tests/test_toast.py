import ast
from pprint import pprint

import astor

import toast


def test_source_to_ast_and_back():
    f_source = "def f():\n    return 0\n"

    # convert to ast
    f_ast = toast.source_to_ast(f_source)
    assert f_ast == {"name": "f", "args": [], "body": [["Return", ["Num", 0]]]}

    # modify ast
    f_ast["body"][0][1][1] = 1

    # convert back to source
    f_source2 = toast.ast_to_source(f_ast)
    assert f_source2 == "def f():\n    return 1\n"


def test_basic():
    f_source = "\n".join(["def f():", "    return 4", ""])
    f_ast = toast.source_to_ast(f_source)
    assert f_ast == {"name": "f", "args": [], "body": [["Return", ["Num", 4]]]}


def test_nested_arithmetic():
    f_source = "\n".join(["def f():", "    return 1 + (2 - (3 * (4 / 5)))", ""])
    f_ast = toast.source_to_ast(f_source)
    assert f_ast == {
        "name": "f",
        "args": [],
        "body": [
            [
                "Return",
                [
                    "Add",
                    ["Num", 1],
                    [
                        "Sub",
                        ["Num", 2],
                        ["Mult", ["Num", 3], ["Div", ["Num", 4], ["Num", 5]]],
                    ],
                ],
            ]
        ],
    }

    f_source = "\n".join(["def f():", "    return (1 + (2 - 3)) * (4 / 5)", ""])
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


def test_function_call():
    f_source = "\n".join(["def f():", "    return some_function(1, 2, 3)", ""])
    f_ast = toast.source_to_ast(f_source)
    assert f_ast == {
        "name": "f",
        "args": [],
        "body": [
            [
                "Return",
                [
                    "Call",
                    ["Name", "some_function"],
                    [["Num", 1], ["Num", 2], ["Num", 3]],
                ],
            ]
        ],
    }
    assert toast.ast_to_source(f_ast) == f_source


'''
def test_cycle():
    f_source = "def f():\n    return 0\n"

    f_ast = toast.source_to_ast(f_source)

    assert f_ast == {"name": "f", "args": [], "body": [["Return", ["Num", 0]]]}

    f_object = toast.ast_to_object(f_ast)


def test_deconstruct_recurse():
    # deconstructing variable references
    assert toast.deconstruct_recurse(ast.Name("a", None)) == ["Name", "a"]

    # deconstructing return statements
    f = ast.Return(value=ast.Name("a", None))
    expected = ["Return", ["Name", "a"]]
    assert toast.deconstruct_recurse(f) == expected

    # deconstructing assignment statements
    f = ast.Assign(targets=[ast.Name("a", None)], value=ast.Name("b", None))
    expected = ["Assign", [["Name", "a"]], ["Name", "b"]]
    assert toast.deconstruct_recurse(f) == expected


def test_reconstruct_recurse():
    # reconstructing variable references
    o = toast.reconstruct_recurse(["Name", "a"])
    assert type(o) == type(ast.Name("a", None))
    assert o.id == "a"

    # reconstructing return statements
    o = toast.reconstruct_recurse(["Return", ["Name", "a"]])
    assert type(o) == type(ast.Return(value=ast.Name("a", None)))
    assert o.value.id == "a"

    # reconstructing assignment statements
    o = toast.reconstruct_recurse(["Assign", [["Name", "a"]], ["Name", "b"]])
    assert type(o) == type(
        ast.Assign(targets=[ast.Name("a", None)], value=ast.Name("b", None))
    )


def test_reconstruct_recurse__nested():
    a = ["Add", ["Name", "a"], ["Add", ["Name", "b"], ["Name", "c"]]]
    o = toast.reconstruct_recurse(a)

    a = [
        "Assign",
        [["Name", "d"]],
        ["Add", ["Name", "a"], ["Add", ["Name", "b"], ["Name", "c"]]],
    ]
    o = toast.reconstruct_recurse(a)


def test_round_trip():
    code = "\n".join(["def f(a):", "    return a", ""])
    j = toast.deconstruct_function(code)
    assert j == {"name": "f", "args": ["a"], "body": [["Return", ["Name", "a"]]]}
    assert toast.reconstruct_function(j) == code

    code = "\n".join(["def f(a, b):", "    return a + b", ""])
    j = toast.deconstruct_function(code)
    assert j == {
        "name": "f",
        "args": ["a", "b"],
        "body": [["Return", ["Add", ["Name", "a"], ["Name", "b"]]]],
    }
    assert toast.reconstruct_function(j) == code

    code = "\n".join(["def f(a, b, c):", "    d = a + (b + c)", "    return d", ""])
    j = toast.deconstruct_function(code)
    assert j == {
        "name": "f",
        "args": ["a", "b", "c"],
        "body": [
            [
                "Assign",
                [["Name", "d"]],
                ["Add", ["Name", "a"], ["Add", ["Name", "b"], ["Name", "c"]]],
            ],
            ["Return", ["Name", "d"]],
        ],
    }
    toast.reconstruct_function(j)
    assert toast.reconstruct_function(j) == code


def tst_s():
    code = "\n".join(["def f(a):", "    return a", ""])
    j = toast.deconstruct_function(code)
    assert j == {"name": "f", "args": ["a"], "body": [["Return", ["Name", "a"]]]}
    assert toast.reconstruct_function(j) == code

    code = """def f(a, b, c):
    d = a + (b + c)
    return d
    """
    j = toast.deconstruct_function(code)

    assert j == {
        "name": "f",
        "args": ["a", "b", "c"],
        "body": [
            [
                "Assign",
                [["Name", "d"]],
                ["Add", ["Name", "a"], ["Add", ["Name", "b"], ["Name", "c"]]],
            ],
            ["Return", ["Name", "d"]],
        ],
    }
    pprint(toast.reconstruct_function(j))

'''
