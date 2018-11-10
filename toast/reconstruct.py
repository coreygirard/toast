import ast


def reconstruct_list(a):
    return list(map(reconstruct, a))


def reconstruct_literal(o):
    if isinstance(o, int):
        return ast.Num(o)


def reconstruct_variable(o):
    return ast.Name(o, '')


def reconstruct_tuple(o):
    assert len(o) == 2
    typ, val = o
    if typ == 'literal':
        return reconstruct_literal(val)
    elif typ == 'variable':
        return reconstruct_variable(val)


def reconstruct_dict(o):
    k = list(o.keys())[0]
    if k in reconstruct_lookup:
        return reconstruct_lookup[k](o)

    raise TypeError(f'unhandled type: {k}')


def reconstruct_Tuple(o):
    return ast.Tuple(*[reconstruct(e) for e in o['Tuple']['elts']], None)


def reconstruct_Add(o):
    return ast.BinOp(left=reconstruct(o['Add']['left']),
                     op=ast.Add,
                     right=reconstruct(o['Add']['right']))


def reconstruct_Assign(o):
    return ast.Assign(targets=reconstruct(o['Assign']['targets']),
                      value=reconstruct(o['Assign']['value']))


def reconstruct_Return(o):
    return ast.Return(value=reconstruct(o['Return']['value']))


reconstruct_lookup = {'list': reconstruct_list,
                      'tuple': reconstruct_tuple,
                      'dict': reconstruct_dict,
                      'Assign': reconstruct_Assign,
                      'Return': reconstruct_Return,
                      'Add': reconstruct_Add}


def reconstruct(a):
    typ = type(a).__name__
    if typ in reconstruct_lookup:
        return reconstruct_lookup[typ](a)

    raise TypeError(f'unhandled type: {typ}')
