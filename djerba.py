# djerba — a tiny toy language with a unique syntax
# Author: Khaled Ouriemmi (https://github.com/khaledouriemmi)
# Run: python djerba.py test.djerba

import sys, re, math
from dataclasses import dataclass
from typing import List, Tuple, Any, Dict, Optional

# ----------------------
# Lexer
# ----------------------

TOKEN_SPEC = [
    ('NUMBER',   r'\d+(\.\d+)?'),         # 123, 3.14
    ('STRING',   r'"([^"\\]|\\.)*"'),     # "hello"
    ('ARROW',    r'<-'),                  # assignment
    ('PRINT',    r':>'),                  # print
    ('FORLOOP',  r'@>'),                  # for loop
    ('IF',       r'\?'),                  # if
    ('WHILE',    r'~'),                   # while
    ('FUNC',     r'@'),                   # function def
    ('RETURN',   r'!>'),                  # return
    ('TRUE',     r'\btrue\b'),            # boolean true
    ('FALSE',    r'\bfalse\b'),           # boolean false
    ('AND',      r'\band\b'),             # logical and
    ('OR',       r'\bor\b'),              # logical or
    ('NOT',      r'\bnot\b'),             # logical not
    ('IN',       r'\bin\b'),              # for loop in
    ('BREAK',    r'\bbreak\b'),           # break
    ('CONTINUE', r'\bcontinue\b'),        # continue
    ('ELSE',     r'\belse\b'),
    ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'),
    ('DOLLAR',   r'\$'),
    ('OP',       r'[+\-*\/\^%]'),
    ('CMP',      r'(==|!=|<=|>=|<|>)'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('LBRACKET', r'\['),                  # list start
    ('RBRACKET', r'\]'),                  # list end
    ('COMMA',    r','),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t\r]+'),
    ('COMMENT',  r';;[^\n]*'),
]
MASTER_RE = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC))

@dataclass
class Token:
    type: str
    value: str
    pos: int

def lex(source: str) -> List[Token]:
    tokens = []
    for m in MASTER_RE.finditer(source):
        kind = m.lastgroup
        val = m.group()
        if kind in ('SKIP', 'COMMENT'):
            continue
        if kind == 'STRING':
            #
            pass
        tokens.append(Token(kind, val, m.start()))
    tokens.append(Token('EOF', '', len(source)))
    return tokens

# ----------------------
# Parser (recursive descent)
# ----------------------

class ParseError(Exception): pass

@dataclass
class Node: ...
@dataclass
class Program(Node): body: List[Node]
@dataclass
class Print(Node): args: List[Node]
@dataclass
class Assign(Node): name: str; expr: Node
@dataclass
class If(Node): cond: Node; then: List[Node]; els: Optional[List[Node]]
@dataclass
class While(Node): cond: Node; body: List[Node]
@dataclass
class ForLoop(Node): var: str; iterable: Node; body: List[Node]
@dataclass
class FuncDef(Node): name: str; params: List[str]; body: List[Node]
@dataclass
class Return(Node): expr: Node
@dataclass
class Break(Node): pass
@dataclass
class Continue(Node): pass

# Expressions
@dataclass
class Var(Node): name: str
@dataclass
class Num(Node): value: float
@dataclass
class Str(Node): value: str
@dataclass
class Bool(Node): value: bool
@dataclass
class List_(Node): elements: List[Node]  # List_ to avoid shadowing built-in
@dataclass
class Index(Node): obj: Node; idx: Node
@dataclass
class Call(Node): name: str; args: List[Node]
@dataclass
class BinOp(Node): op: str; left: Node; right: Node
@dataclass
class Compare(Node): op: str; left: Node; right: Node
@dataclass
class LogicalOp(Node): op: str; left: Node; right: Optional[Node] = None  # right is None for 'not'

class Parser:
    def __init__(self, tokens: List[Token]):
        self.ts = tokens
        self.i = 0

    def peek(self, *types) -> bool:
        return self.ts[self.i].type in types

    def expect(self, ttype: str) -> Token:
        tok = self.ts[self.i]
        if tok.type != ttype:
            raise ParseError(f'Expected {ttype}, got {tok.type} at {tok.pos}')
        self.i += 1
        return tok

    def match(self, ttype: str) -> Optional[Token]:
        if self.peek(ttype):
            return self.expect(ttype)
        return None

    def parse(self) -> Program:
        stmts = []
        while not self.peek('EOF'):
            if self.peek('NEWLINE'):
                self.expect('NEWLINE'); continue
            stmts.append(self.statement())
            self.match('NEWLINE')
        return Program(stmts)

    def block(self) -> List[Node]:
        self.expect('LBRACE')
        body = []
        while not self.peek('RBRACE'):
            if self.peek('NEWLINE'):
                self.expect('NEWLINE'); continue
            body.append(self.statement())
            self.match('NEWLINE')
        self.expect('RBRACE')
        return body

    def statement(self) -> Node:
        if self.peek('PRINT'):
            self.expect('PRINT')
            args = [self.expr()]
            while self.match('COMMA'):
                args.append(self.expr())
            return Print(args)

        if self.peek('DOLLAR'):
            self.expect('DOLLAR')
            name = self.expect('IDENT').value
            self.expect('ARROW')
            return Assign(name, self.expr())

        if self.peek('IF'):
            self.expect('IF')
            cond = self.expr()
            then = self.block()
            els = None
            if self.match('ELSE'):
                els = self.block()
            return If(cond, then, els)

        if self.peek('WHILE'):
            self.expect('WHILE')
            cond = self.expr()
            body = self.block()
            return While(cond, body)

        if self.peek('FORLOOP'):
            self.expect('FORLOOP')
            self.expect('DOLLAR')
            var = self.expect('IDENT').value
            self.expect('IN')
            iterable = self.expr()
            body = self.block()
            return ForLoop(var, iterable, body)

        if self.peek('FUNC'):
            self.expect('FUNC')
            name = self.expect('IDENT').value
            self.expect('LPAREN')
            params = []
            if not self.peek('RPAREN'):
                params.append(self.expect('IDENT').value)
                while self.match('COMMA'):
                    params.append(self.expect('IDENT').value)
            self.expect('RPAREN')
            body = self.block()
            return FuncDef(name, params, body)

        if self.peek('RETURN'):
            self.expect('RETURN')
            return Return(self.expr())

        if self.peek('BREAK'):
            self.expect('BREAK')
            return Break()

        if self.peek('CONTINUE'):
            self.expect('CONTINUE')
            return Continue()

        # Expression statement (e.g., function call)
        return self.expr()

    # Expression grammar: precedence climbing
    def expr(self) -> Node:
        return self.logical_or()

    def logical_or(self) -> Node:
        node = self.logical_and()
        while self.peek('OR'):
            self.expect('OR')
            right = self.logical_and()
            node = LogicalOp('or', node, right)
        return node

    def logical_and(self) -> Node:
        node = self.logical_not()
        while self.peek('AND'):
            self.expect('AND')
            right = self.logical_not()
            node = LogicalOp('and', node, right)
        return node

    def logical_not(self) -> Node:
        if self.peek('NOT'):
            self.expect('NOT')
            return LogicalOp('not', self.logical_not())
        return self.compare()

    def compare(self) -> Node:
        node = self.term()
        while self.peek('CMP'):
            op = self.expect('CMP').value
            right = self.term()
            node = Compare(op, node, right)
        return node

    def term(self) -> Node:
        node = self.factor()
        while self.peek('OP') and self.ts[self.i].value in ('+', '-'):
            op = self.expect('OP').value
            right = self.factor()
            node = BinOp(op, node, right)
        return node

    def factor(self) -> Node:
        node = self.power()
        while self.peek('OP') and self.ts[self.i].value in ('*', '/', '%'):
            op = self.expect('OP').value
            right = self.power()
            node = BinOp(op, node, right)
        return node

    def power(self) -> Node:
        node = self.unary()
        while self.peek('OP') and self.ts[self.i].value == '^':
            self.expect('OP')
            right = self.unary()
            node = BinOp('^', node, right)
        return node

    def unary(self) -> Node:
        if self.peek('OP') and self.ts[self.i].value == '-':
            self.expect('OP')
            return BinOp('*', Num(-1), self.unary())
        return self.primary()

    def primary(self) -> Node:
        if self.peek('NUMBER'):
            val = float(self.expect('NUMBER').value)
            return Num(val)
        if self.peek('STRING'):
            raw = self.expect('STRING').value
            s = bytes(raw[1:-1], 'utf-8').decode('unicode_escape')
            return Str(s)
        if self.peek('TRUE'):
            self.expect('TRUE')
            return Bool(True)
        if self.peek('FALSE'):
            self.expect('FALSE')
            return Bool(False)
        if self.peek('LBRACKET'):
            self.expect('LBRACKET')
            elements = []
            if not self.peek('RBRACKET'):
                elements.append(self.expr())
                while self.match('COMMA'):
                    elements.append(self.expr())
            self.expect('RBRACKET')
            return List_(elements)
        if self.peek('DOLLAR'):
            self.expect('DOLLAR')
            name = self.expect('IDENT').value
            node = Var(name)
            # Handle indexing
            while self.peek('LBRACKET'):
                self.expect('LBRACKET')
                idx = self.expr()
                self.expect('RBRACKET')
                node = Index(node, idx)
            return node
        if self.peek('IDENT'):
            name = self.expect('IDENT').value
            if self.match('LPAREN'):
                args = []
                if not self.peek('RPAREN'):
                    args.append(self.expr())
                    while self.match('COMMA'):
                        args.append(self.expr())
                self.expect('RPAREN')
                return Call(name, args)
            return Var(name)  # allow bare ident inside functions
        if self.match('LPAREN'):
            e = self.expr()
            self.expect('RPAREN')
            return e
        raise ParseError(f'Unexpected token {self.ts[self.i].type} at {self.ts[self.i].pos}')

# ----------------------
# Interpreter
# ----------------------

class ReturnSignal(Exception):
    def __init__(self, value): self.value = value

class BreakSignal(Exception):
    pass

class ContinueSignal(Exception):
    pass

class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.vars: Dict[str, Any] = {}
        self.funcs: Dict[str, FuncDef] = {}

    def get(self, name: str):
        if name in self.vars: return self.vars[name]
        if self.parent: return self.parent.get(name)
        raise NameError(f'Undefined variable {name}')

    def set(self, name: str, value: Any):
        # assign into nearest existing scope, else current
        if name in self.vars:
            self.vars[name] = value; return
        if self.parent and name in self.parent.vars:
            self.parent.set(name, value); return
        self.vars[name] = value

    def define_func(self, f: FuncDef):
        self.funcs[f.name] = f

    def get_func(self, name: str):
        if name in self.funcs: return self.funcs[name]
        if self.parent: return self.parent.get_func(name)
        raise NameError(f'Undefined function {name}()')

def eval_program(ast: Program):
    env = Environment()
    # built-in constants
    env.vars['PI'] = math.pi
    env.vars['E'] = math.e
    
    # built-in math functions
    env.vars['sin'] = lambda x: math.sin(x)
    env.vars['cos'] = lambda x: math.cos(x)
    env.vars['tan'] = lambda x: math.tan(x)
    env.vars['sqrt'] = lambda x: math.sqrt(x)
    env.vars['abs'] = lambda x: abs(x)
    env.vars['floor'] = lambda x: math.floor(x)
    env.vars['ceil'] = lambda x: math.ceil(x)
    env.vars['round'] = lambda x: round(x)
    env.vars['min'] = lambda *args: min(args)
    env.vars['max'] = lambda *args: max(args)
    env.vars['pow'] = lambda x, y: x ** y
    
    # built-in string functions
    def _len(obj):
        return len(obj)
    def _upper(s):
        return s.upper()
    def _lower(s):
        return s.lower()
    def _substr(s, start, end=None):
        if end is None:
            return s[int(start):]
        return s[int(start):int(end)]
    
    env.vars['len'] = _len
    env.vars['upper'] = _upper
    env.vars['lower'] = _lower
    env.vars['substr'] = _substr
    
    # built-in list functions
    def _push(lst, item):
        lst.append(item)
        return lst
    def _pop(lst):
        return lst.pop() if lst else None
    def _append(lst, item):
        lst.append(item)
        return lst
    
    env.vars['push'] = _push
    env.vars['pop'] = _pop
    env.vars['append'] = _append
    
    # built-in utility functions
    def _input(prompt=""):
        return input(prompt)
    def _type(obj):
        if isinstance(obj, bool):
            return "bool"
        elif isinstance(obj, int) or isinstance(obj, float):
            return "number"
        elif isinstance(obj, str):
            return "string"
        elif isinstance(obj, list):
            return "list"
        else:
            return "unknown"
    def _range(*args):
        if len(args) == 1:
            return list(range(int(args[0])))
        elif len(args) == 2:
            return list(range(int(args[0]), int(args[1])))
        elif len(args) == 3:
            return list(range(int(args[0]), int(args[1]), int(args[2])))
        return []
    
    env.vars['input'] = _input
    env.vars['type'] = _type
    env.vars['range'] = _range
    env.vars['print'] = lambda *vals: print(*vals)
    
    run_block(ast.body, env)

def run_block(stmts: List[Node], env: Environment):
    for s in stmts:
        eval_stmt(s, env)

def eval_stmt(node: Node, env: Environment):
    if isinstance(node, Print):
        vals = [eval_expr(a, env) for a in node.args]
        print(*vals)
        return
    if isinstance(node, Assign):
        env.set(node.name, eval_expr(node.expr, env)); return
    if isinstance(node, If):
        if truthy(eval_expr(node.cond, env)):
            run_block(node.then, Environment(env))
        elif node.els is not None:
            run_block(node.els, Environment(env))
        return
    if isinstance(node, While):
        while truthy(eval_expr(node.cond, env)):
            try:
                run_block(node.body, Environment(env))
            except ContinueSignal:
                continue
            except BreakSignal:
                break
            except ReturnSignal:  
                pass
        return
    if isinstance(node, ForLoop):
        iterable = eval_expr(node.iterable, env)
        if not hasattr(iterable, '__iter__'):
            raise TypeError(f'Cannot iterate over {type(iterable)}')
        for item in iterable:
            child = Environment(env)
            child.vars[node.var] = item
            try:
                run_block(node.body, child)
            except ContinueSignal:
                continue
            except BreakSignal:
                break
        return
    if isinstance(node, FuncDef):
        env.define_func(node); return
    if isinstance(node, Return):
        val = eval_expr(node.expr, env)
        raise ReturnSignal(val)
    if isinstance(node, Break):
        raise BreakSignal()
    if isinstance(node, Continue):
        raise ContinueSignal()
    # Expression-only statement
    eval_expr(node, env)

def truthy(v): return bool(v)

def eval_expr(node: Node, env: Environment):
    if isinstance(node, Num): return node.value
    if isinstance(node, Str): return node.value
    if isinstance(node, Bool): return node.value
    if isinstance(node, List_): return [eval_expr(e, env) for e in node.elements]
    if isinstance(node, Var):
        # allow bare identifiers as local vars or params
        try:
            return env.get(node.name)
        except NameError:
            raise
    if isinstance(node, BinOp):
        l = eval_expr(node.left, env); r = eval_expr(node.right, env)
        if node.op == '+': return l + r
        if node.op == '-': return l - r
        if node.op == '*': return l * r
        if node.op == '/': return l / r
        if node.op == '%': return l % r
        if node.op == '^': return l ** r
        raise RuntimeError(f'Unknown op {node.op}')
    if isinstance(node, Compare):
        l = eval_expr(node.left, env); r = eval_expr(node.right, env)
        if node.op == '==': return l == r
        if node.op == '!=': return l != r
        if node.op == '<':  return l <  r
        if node.op == '>':  return l >  r
        if node.op == '<=': return l <= r
        if node.op == '>=': return l >= r
        raise RuntimeError(f'Unknown cmp {node.op}')
    if isinstance(node, LogicalOp):
        if node.op == 'not':
            return not truthy(eval_expr(node.left, env))
        l = eval_expr(node.left, env)
        if node.op == 'and':
            return truthy(l) and truthy(eval_expr(node.right, env))
        if node.op == 'or':
            return truthy(l) or truthy(eval_expr(node.right, env))
        raise RuntimeError(f'Unknown logical op {node.op}')
    if isinstance(node, Index):
        obj = eval_expr(node.obj, env)
        idx = eval_expr(node.idx, env)
        if isinstance(obj, (list, str)):
            return obj[int(idx)]
        raise TypeError(f'Cannot index {type(obj)}')
    if isinstance(node, Call):
        # user-defined
        try:
            f = env.get_func(node.name)
            if len(node.args) != len(f.params):
                raise TypeError(f'{f.name} expects {len(f.params)} args, got {len(node.args)}')
            child = Environment(env)
            for name, arg in zip(f.params, node.args):
                child.vars[name] = eval_expr(arg, env)
            try:
                run_block(f.body, child)
                return None
            except ReturnSignal as rs:
                return rs.value
        except NameError:
            # try a built-in callable in vars
            fn = env.vars.get(node.name)
            if callable(fn):
                args = [eval_expr(a, env) for a in node.args]
                return fn(*args)
            raise
    raise RuntimeError(f'Unhandled expr node: {node}')

# ----------------------
# CLI
# ----------------------

def main():
    if len(sys.argv) != 2:
        print("Usage: python djerba.py <file.djerba>")
        sys.exit(1)
    path = sys.argv[1]
    src = open(path, 'r', encoding='utf-8').read()
    tokens = lex(src)
    parser = Parser(tokens)
    ast = parser.parse()
    eval_program(ast)

if __name__ == '__main__':
    main()
