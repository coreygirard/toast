import ast
from pprint import pprint

import astor

import toast


def test_source2ast():
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


def test_something():
    code = """def f(a, b):
    return a + b
    """

    parsed_ast = ast.parse(code)

    o = parsed_ast.body[0].body
    de_o = toast.deconstruct.deconstruct(o)
    pprint(de_o)
    o2 = toast.reconstruct.reconstruct(de_o)
    #print(o)

    o2[0].lineno = 2
    o2[0].col_offset = 4

    o2[0].value.lineno = 2
    o2[0].value.col_offset = 11

    o2[0].value.left.lineno = 2
    o2[0].value.left.col_offset = 11

    o2[0].value.right.lineno = 2
    o2[0].value.right.col_offset = 15


    pprint(o[0].value.right.col_offset)
    pprint(o2[0].value.right.col_offset)

    parsed_ast.body[0].body = o2
    print(astor.to_source(parsed_ast))

    #compare(o, o2)
