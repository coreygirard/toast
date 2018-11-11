import ast
from pprint import pprint

import astor

import deconstruct
import reconstruct


code = """
def f(a, b):
    c = a + b + 0
    d = 'a' + 'b'
    return c
"""
code = """
def f(a, b):
    c = a + b + 0
    return c
"""


def source2ast(s):
    parsed_ast = ast.parse(s)
    o = parsed_ast.body[0].body
    return deconstruct.deconstruct(o)


"""
parsed_ast = ast.parse(code)

o = parsed_ast.body[0].body
de_o = deconstruct(o)
#pprint(de_o)
o2 = reconstruct(de_o)
#print(o)

parsed_ast.body[0].body = o2
print(astor.to_source(parsed_ast))

pprint(o[0].value.left.left.id)
pprint(o2[0].value.left.left.id)
"""
