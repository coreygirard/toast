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


def r_Call(func, args):
    return ast.Call(func=reconstruct(func), args=reconstruct(args))


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
}


def reconstruct(f_ast):
    if isinstance(f_ast, list):
        return [reconstruct(e) for e in f_ast]

    print(f_ast)

    head, *rest = f_ast

    if head in reconstruct_lookup:
        return reconstruct_lookup[head](*rest)

    raise TypeError(f"'{head}' not handled")
