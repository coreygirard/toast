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


def d_Assign(line):
    return ["Assign", deconstruct(line.targets), deconstruct(line.value)]


def d_Call(line):
    return ["Call", deconstruct(line.func), deconstruct(line.args)]


deconstruct_lookup = {
    "Return": d_Return,
    "BinOp": d_BinOp,
    "Name": d_Name,
    "Assign": d_Assign,
    "Num": d_Num,
    "Call": d_Call,
}


def deconstruct(line):
    if isinstance(line, list):
        return [deconstruct(e) for e in line]

    typ = type(line).__name__
    if typ in deconstruct_lookup:
        return deconstruct_lookup[typ](line)

    raise TypeError(f"'{typ}' not handled")
