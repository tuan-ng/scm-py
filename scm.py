import math
import operator as op
from functools import reduce


def tokenize(s):
    token = ''
    tokens = []
    def is_paren(c): return c in '()'

    for c in s:
        if c.isspace():
            if token:
                tokens.append(token)
                token = ''
        elif is_paren(c):
            if token:
                tokens.append(token)
                token = ''
            tokens.append(c)
        else:
            token += c

    if token:
        tokens.append(token)
    return tokens


def parse(tokens):
    def atom(token):
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return token

    def _parse(exp, tokens):
        if not tokens:
            return (exp, tokens)

        c = tokens.pop(0)
        if c is '(':
            (_exp, tokens) = _parse([], tokens)
            exp.append(_exp)
            return _parse(exp, tokens)
        elif c is ')':
            return (exp, tokens)
        else:
            exp.append(atom(c))
            return _parse(exp, tokens)
    return _parse([], tokens)[0][0]


class Env(dict):
    def __init__(self, pars=(), args=(),  parent=None):
        self.update(zip(pars, args))
        self.parent = parent

    def find(self, var):
        return self if (var in self) else self.parent.find(var)


class Proc(object):
    def __init__(self, pars=(), body=(), env=None):
        self.pars, self.body, self.env = pars, body, env

    def __call__(self, *args):
        return interpret(self.body, Env(self.pars, args, self.env))


global_env = Env()
global_env.update({
    'pi': math.pi,
    'e': math.e,
    '+': Proc(),
    '-': Proc(),
    '*': Proc(),
    '>': Proc(),
    '>=': Proc(),
    '<': Proc(),
    '<=': Proc(),
    '=': Proc()})


def repl(prompt='scm.py> '):
    while True:
        val = interpret(parse(tokenize(input(prompt))))
        if val is not None:
            print(lispstr(val))


def lispstr(exp):
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)


def interpret(e, env=global_env):
    def _interpret(exp):
        return [interpret(exp, env) for exp in exp]

    def _reduce(op, rest, snd, fst):
        return reduce(op, rest, reduce(op, [snd], fst))

    if isinstance(e, str):
        return env.find(e)[e]
    elif not isinstance(e, list):
        return e
    elif e[0] == '+':
        args = _interpret(e[1:])
        return reduce(op.add, args, 0)
    elif e[0] == '-':
        first, *rest = _interpret(e[1:])
        return reduce(op.sub, rest, -first if not rest else first)
    elif e[0] == '*':
        args = _interpret(e[1:])
        return reduce(op.mul, args, 1)
    elif e[0] == '/':
        first, *rest = _interpret(e[1:])
        return reduce(op.truediv, rest, 1/first if not rest else first)
    elif e[0] == '<=':
        first, second, *rest = _interpret(e[1:])
        return _reduce(op.le, rest, second, first)
    elif e[0] == '>=':
        first, second, *rest = _interpret(e[1:])
        return _reduce(op.ge, rest, second, first)
    elif e[0] == '<':
        first, second, *rest = _interpret(e[1:])
        return _reduce(op.lt, rest, second, first)
    elif e[0] == '>':
        first, second, *rest = _interpret(e[1:])
        return _reduce(op.gt, rest, second, first)
    elif e[0] == '=':
        first, second, *rest = _interpret(e[1:])
        return _reduce(op.eq, rest, second, first)
    elif e[0] == 'quote':
        (_, exp) = e
        return exp
    elif e[0] == 'if':
        (_, test, cons, alt) = e
        exp = (cons if interpret(test, env) is not False else alt)
        return interpret(exp, env)
    elif e[0] == 'define':
        (_, var, exp) = e
        env.update({var: interpret(exp, env)})
    elif e[0] == 'set!':
        (_, var, exp) = e
        env.find(var)[var] = interpret(exp, env)
    elif e[0] == 'lambda':
        (_, pars, body) = e
        return Proc(pars, body, env)
    else:
        proc, *args = _interpret(e)
        return proc(*args)


repl()
