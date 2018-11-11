import ast

import astor

#from toast.scratch import *


def _python_to_toast(a):
    return a


def _toast_to_python(a):
    return a


def source_to_ast(function_source):
    return _python_to_toast(ast.parse(function_source))


def ast_to_source(function_ast):
    return astor.to_source(_toast_to_python(function_ast))


def ast_to_object():
    pass


def object_to_ast():
    pass


def object_to_source():
    pass


def source_to_object():
    pass
