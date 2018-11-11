import ast
from toast import deconstruct
from toast import reconstruct
from toast.scratch import *


def source2ast(s):
    parsed_ast = ast.parse(s)
    o = parsed_ast.body[0].body
    return deconstruct.deconstruct(o)
