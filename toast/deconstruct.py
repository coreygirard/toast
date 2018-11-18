import ast

import astor


def d_Return(line):
    return ["Return", deconstruct(line.value)]


def d_BinOp(line):
    return [type(line.op).__name__, deconstruct(line.left), deconstruct(line.right)]


def d_Name(line):
    return ["Name", line.id]


def d_Num(line):
    return ["Num", line.n]


def d_Str(line):
    return ["Str", line.s]


def d_Assign(line):
    return ["Assign", deconstruct(line.targets), deconstruct(line.value)]


def d_Call(line):
    return [
        "Call",
        deconstruct(line.func),
        deconstruct(line.args),
        deconstruct(line.keywords),
    ]


def d_Attribute(line):
    return ["Attribute", deconstruct(line.value), deconstruct(line.attr)]


def d_str(line):
    return ["str", str(line)]


def d_Assert(line):
    return [
        "Assert",
        deconstruct(line.test),
        [] if line.msg is None else deconstruct(line.msg),
    ]


def d_Compare(line):
    return [
        type(line.ops[0]).__name__,
        deconstruct(line.left),
        deconstruct(line.comparators),
    ]


def d_Subscript(line):
    return ["Subscript", deconstruct(line.value), deconstruct(line.slice)]


def d_Expr(line):
    return ["Expr", deconstruct(line.value)]


def d_Index(line):
    return ["Index", deconstruct(line.value)]


def d_Dict(line):
    return ["Dict", deconstruct(line.keys), deconstruct(line.values)]


def d_List(line):
    return ["List", deconstruct(line.elts)]


def d_Pass(line):
    return ["Pass"]


deconstruct_lookup = {
    "Return": d_Return,
    "BinOp": d_BinOp,
    "Name": d_Name,
    "Assign": d_Assign,
    "Num": d_Num,
    "Call": d_Call,
    "Attribute": d_Attribute,
    "Str": d_Str,
    "str": d_str,
    "Assert": d_Assert,
    "Compare": d_Compare,
    "Subscript": d_Subscript,
    "Expr": d_Expr,
    "Index": d_Index,
    "Dict": d_Dict,
    "List": d_List,
    "Pass": d_Pass,
}


def deconstruct(line):
    if isinstance(line, list):
        return [deconstruct(e) for e in line]

    typ = type(line).__name__
    if typ in deconstruct_lookup:
        return deconstruct_lookup[typ](line)

    raise TypeError(f"'{typ}' not handled")
