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


def deconstruct3(a, depth=0):
    if depth > 5:
        return 'DEPTH EXCEEDED'

    if isinstance(a, (int, str)):
        return a

    if isinstance(a, list):
        return [deconstruct(e, depth+1) for e in a]

    data = {}
    for attr in dir(a):
        if attr in ['__abstractmethods__',
                    '__weakref__',
                    '__subclasshook__',
                    '__new__',
                    '__le__',
                    '__str__',
                    '__sizeof__',
                    '__setattr__',
                    '__ne__',
                    '__dir__',
                    '__doc__',
                    '__eq__',
                    '__class__',
                    '__delattr__',
                    '__dict__',
                    '__format__',
                    '__ge__',
                    '__getattribute__',
                    '__gt__',
                    '__hash__',
                    '__init__',
                    '__init_subclass__',
                    '__lt__',
                    '__reduce__',
                    '__reduce_ex__',
                    '__repr__',
                    '__add__',
                    '__contains__',
                    '__getitem__',
                    '__getnewargs__',
                    '__iter__',
                    '__len__',
                    '__mul__',
                    '__rmul__',
                    '__call__',
                    '__self__',
                    '__qualname__',
                    '__text_signature__']:
            continue

        data[attr] = deconstruct(getattr(a, attr), depth+1)

    return data
