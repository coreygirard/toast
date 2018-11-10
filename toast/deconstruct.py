def deconstruct_list(a):
    return list(map(deconstruct, a))


def deconstruct_int(a):
    return a


def deconstruct_str(a):
    return a


def deconstruct_dict(a):
    return a


def deconstruct_BinOp(a):
    typ = type(a.op).__name__
    data = {'left': deconstruct(a.left),
            'right': deconstruct(a.right)}
    return {typ: data}


def deconstruct_Tuple(a):
    return {'Tuple': {'elts': deconstruct(a.elts)}}


def deconstruct_Name(a):
    return ('variable', a.id)


def deconstruct_Num(a):
    return ('literal', a.n)


def deconstruct_Str(a):
    return ('literal', a.s)


def deconstruct_Assign(a):
    return {'Assign': {'targets': deconstruct(a.targets),
                       'value': deconstruct(a.value)}}


def deconstruct_Return(a):
    return {'Return': {'value': deconstruct(a.value)}}


deconstruct_lookup = {'list': deconstruct_list,
                      'int': deconstruct_int,
                      'str': deconstruct_str,
                      'dict': deconstruct_dict,
                      'Tuple': deconstruct_Tuple,
                      'Name': deconstruct_Name,
                      'Num': deconstruct_Num,
                      'Str': deconstruct_Str,
                      'Assign': deconstruct_Assign,
                      'Return': deconstruct_Return,
                      'BinOp': deconstruct_BinOp}


def deconstruct(a):
    typ = type(a).__name__
    if typ in deconstruct_lookup:
        return deconstruct_lookup[typ](a)

    raise TypeError(f'unhandled type: {typ}')
