import ast
import inspect

import astor

from toast import deconstruct, reconstruct


def _python_to_toast(module_ast):
    f_ast = module_ast.body[0]
    return {
        "name": f_ast.name,
        "args": [a.arg for a in f_ast.args.args],
        "body": [deconstruct.deconstruct(line) for line in f_ast.body],
    }


def _toast_to_python(a):
    # TODO: remove reliance on parsing starter function

    code = """def f(a):
        return a + (b + c)
    """
    f_ast = ast.parse(code)

    f_ast.body[0].name = a["name"]
    f_ast.body[0].args.args = [ast.arg(a, None) for a in a["args"]]
    f_ast.body[0].body = [reconstruct.reconstruct(e) for e in a["body"]]

    for i, line in enumerate(f_ast.body[0].body):
        line.lineno = i
        ast.fix_missing_locations(line)

    return f_ast


def source_to_ast(function_source):
    return _python_to_toast(ast.parse(function_source))


def ast_to_source(function_ast):
    return astor.to_source(_toast_to_python(function_ast))


def ast_to_object(function_ast):
    return compile(_toast_to_python(function_ast), "", "exec")


def source_to_object(function_source):
    return ast_to_object(source_to_ast(function_source))


"""
def object_to_ast():
    pass


def object_to_source(function_object):
    pass
"""
