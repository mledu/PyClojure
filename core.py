class ComparableExpr(object):
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

class Atom(ComparableExpr):
    def __init__(self, name=None, value=None):
        self.__name = name
        self.__binding = value


    def name(self):
        return self.__name

    def __repr__(self):
        return "ATOM(%s, %s)" % (self.__name, self.__binding)


class ComparableList(ComparableExpr):
    def __init__(self, *args):
        self.__contents = []
        for arg in args:
            self.__contents.append(arg)

    def contents(self):
        return self.__contents

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__.upper(),
                           ','.join([str(el) for el in self.__contents]))


class List(ComparableList):
    pass


class Vector(ComparableList):
    pass


class Scope(dict):
    pass


class UnknownVariable(Exception):
    pass


def find_in_scopechain(scopes, name):
    for scope in reversed(scopes):
        try:
            return scope[name]
        except:
            pass
    raise UnknownVariable("Unknown variable: %s" % name)


def evaluate(x, scopes):
    if type(x) is int:
        return x
    elif type(x) is Atom:
        return find_in_scopechain(scopes, x.name())
    elif type(x) is Vector:
        return apply(Vector, [evaluate(el, scopes) for el in x.contents()])
    elif type(x) is List:
        contents = x.contents()
        if len(contents) == 0:
            return x  # ()
        first = contents[0]
        if type(first) is Atom and first.name() == "def":
            atom, rhs = contents[1:3]
            scopes[-1][atom.name()] = evaluate(rhs, scopes)
            return atom
    return x


def tostring(x):
    if x is None:
        return 'nil'
    elif type(x) is int:
        return str(x)
    elif type(x) is Atom:
        return x.name()
    elif type(x) is List:
        inner = ' '.join([tostring(x) for x in x.contents()])
        return '(%s)' % inner
    elif type(x) is Vector:
        inner = ' '.join([tostring(x) for x in x.contents()])
        return '[%s]' % inner
    else:
        raise TypeError('%s is unknown!' % x)
