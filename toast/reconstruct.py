import ast

import astor


def r_Return(value):
    return ast.Return(value=reconstruct(value))


def r_Name(_id):
    return ast.Name(_id, None)


def r_Assign(targets, value):
    return ast.Assign(targets=[reconstruct(targets[0])], value=reconstruct(value))


def r_Add(left, right):
    return ast.BinOp(left=reconstruct(left), op=ast.Add(), right=reconstruct(right))


def r_Sub(left, right):
    return ast.BinOp(left=reconstruct(left), op=ast.Sub(), right=reconstruct(right))


def r_Mult(left, right):
    return ast.BinOp(left=reconstruct(left), op=ast.Mult(), right=reconstruct(right))


def r_Div(left, right):
    return ast.BinOp(left=reconstruct(left), op=ast.Div(), right=reconstruct(right))


def r_Num(n):
    return ast.Num(n)


def r_Call(func, args, keywords):
    return ast.Call(
        func=reconstruct(func),
        args=[reconstruct(a) for a in args],
        keywords=[reconstruct(k) for k in keywords],
    )


def r_Str(s):
    return ast.Str(s)


def r_Attribute(value, attr):
    return ast.Attribute(value=reconstruct(value), attr=reconstruct(attr))


def r_str(s):
    return s


def r_list(lst):
    return [reconstruct(e) for e in lst]


def r_List(lst):
    return ast.List(elts=[reconstruct(e) for e in lst], ctx=None)


def r_Assert(test, msg):
    return ast.Assert(
        test=test, msg=(None if msg == [] else reconstruct(msg)), ctx=None
    )


def r_Pass():
    return ast.Pass


reconstruct_lookup = {
    "Return": r_Return,
    "Add": r_Add,
    "Mult": r_Mult,
    "Sub": r_Sub,
    "Div": r_Div,
    "Name": r_Name,
    "Assign": r_Assign,
    "Num": r_Num,
    "Call": r_Call,
    "Str": r_Str,
    "Attribute": r_Attribute,
    "str": r_str,
    "list": r_list,
    "List": r_List,
    "Assert": r_Assert,
    "Pass": r_Pass,
}


def reconstruct(f_ast):
    head, *rest = f_ast

    if head in reconstruct_lookup:
        return reconstruct_lookup[head](*rest)

    raise TypeError(f"'{head}' not handled")
