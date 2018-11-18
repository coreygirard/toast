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


def test_cycle():
    f_source = "def f():\n    return 0\n"

    f_ast = toast.source_to_ast(f_source)

    assert f_ast == {"name": "f", "args": [], "body": [["Return", ["Num", 0]]]}

    f_object = toast.ast_to_object(f_ast)


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
                    [],
                ],
            ]
        ],
    }

    assert toast.ast_to_source(f_ast) == f_source


def test_function_args():
    f_source = "\n".join(["def f(a, b, c):", "    pass", ""])
    f_ast = toast.source_to_ast(f_source)
    assert f_ast["args"] == ["a", "b", "c"]
