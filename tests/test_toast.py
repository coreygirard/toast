import ast
from pprint import pprint

import astor

import toast


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
def t_source2ast():
    code = """def f(a, b):
    return a + b
    """

    expected = [
        {
            "Return": {
                "value": {
                    "Add": {"left": ("variable", "a"), "right": ("variable", "b")}
                }
            }
        }
    ]

    result = toast.source2ast(code)
    assert result == expected

    code = """def f(a, b, c):
    d = a*b + c
    return 2**d
    """

    expected = [
        {
            "Assign": {
                "targets": [("variable", "d")],
                "value": {
                    "Add": {
                        "left": {
                            "Mult": {
                                "left": ("variable", "a"),
                                "right": ("variable", "b"),
                            }
                        },
                        "right": ("variable", "c"),
                    }
                },
            }
        },
        {
            "Return": {
                "value": {"Pow": {"left": ("literal", 2), "right": ("variable", "d")}}
            }
        },
    ]

    result = toast.source2ast(code)
    assert result == expected


def compare(a, b, depth=0):
    if depth > 4:
        return

    if isinstance(a, int):
        return

    if isinstance(a, list):
        for i, j in zip(a, b):
            compare(i, j)

    assert type(a).__name__ == type(b).__name__
    assert sorted(dir(a)) == sorted(dir(b))

    for attr in dir(a):
        if attr.startswith('_'):
            continue

        i = getattr(a, attr)
        j = getattr(b, attr)

        print(attr)


        compare(i, j, depth+1)


def test_esomething():
    code = """def f(a, b):
    return a + b
    """

    parsed_ast = ast.parse(code)

    o = parsed_ast.body[0].body
    de_o = toast.deconstruct.deconstruct(o)
    pprint(de_o)
    o2 = toast.reconstruct.reconstruct(de_o)
    #print(o)

    ast.fix_missing_locations(o2[0])

    """
    o2[0].lineno = 2
    o2[0].col_offset = 4

    o2[0].value.lineno = 2
    o2[0].value.col_offset = 11

    o2[0].value.left.lineno = 2
    o2[0].value.left.col_offset = 11

    o2[0].value.right.lineno = 2
    o2[0].value.right.col_offset = 15
    """


    pprint(o[0].value.right.col_offset)
    pprint(o2[0].value.right.col_offset)

    parsed_ast.body[0].body = o2
    print(astor.to_source(parsed_ast))

    #compare(o, o2)


def test_something():
    code = """def f(a, b):
    return a + b
    """

    parsed_ast = ast.parse(code)
    o = parsed_ast.body[0].body
    o = toast.deconstruct.deconstruct(o)
    print('\n--------\n')
    pprint(o)
    print('\n--------\n')
'''
