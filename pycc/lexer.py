from funcparserlib.parser import *
import re
from functools import reduce
from operator import add
from collections import Iterable

def flatten(coll):
    for i in coll:
            if isinstance(i, Iterable) and not isinstance(i, str):
                for subc in flatten(i):
                    yield subc
            else:
                yield i

compose = lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs))

join = compose(''.join, flatten)
sre = lambda ms: some(lambda x: re.match(ms, x) is not None)
string = lambda s: reduce(add, map(a, s)) >> ''.join

D = sre(r"[0-9]")
L = sre(r"[a-zA-Z_]")
H = sre(r"[a-fA-F0-9]")
E = sre(r"[Ee]") + maybe(sre("[+-]")) + oneplus(D)
FS = sre(r"f|l|F|L")
IS = many(sre(r"u|l|U|L"))

COMMENT_START = string("/*")
COMMENT_END = string("*/")

AUTO = string("auto")
BREAK = string("break")
CHAR = string("char")
CASE = string("case")
CONST = string("const")
CONTINUE = string("continue")
DEFAULT = string("default")
DO = string("do")
DOUBLE = string("double")
ELSE = string("else")
ENUM = string("enum")
EXTERN = string("extern")
FLOAT = string("float")
FOR = string("for")
GOTO = string("goto")
IF = string("if")
INT = string("int")
LONG = string("long")
REGISTER = string("register")
RETURN = string("return")
SHORT = string("short")
SIGNED = string("signed")
SIZEOF = string("sizeof")
STATIC = string("static")
STRUCT = string("struct")
SWITCH = string("switch")
TYPEDEF = string("typedef")
UNION = string("union")
UNSIGNED = string("unsigned")
VOID = string("void")
VOLATILE = string("volatile")
WHILE = string("while")

IDENTIFIER = L + many(L | D) >> join

CONSTANT  = a("0") + sre("[xX]") + oneplus(H) + maybe(IS) >> join
CONSTANT |= a("0") + oneplus(D) + maybe(IS) >> join
CONSTANT |= oneplus(D) + maybe(IS) >> join
CONSTANT |= maybe(L) + a("'") + oneplus(sre(r"[^\']")) + a("'") >> join
CONSTANT |= oneplus(D) + E + maybe(FS) >> join
CONSTANT |= many(D) + a(".") + oneplus(D) + maybe(E) + maybe(FS) >> join
CONSTANT |= oneplus(D) + a(".") + many(D) + maybe(E) + maybe(FS) >> join

STRING_LITERAL = maybe(L) + a('"') + many(sre(r"[^\"]")) + a('"') >> join

ELLIPSIS = string("...")
RIGHT_ASSIGN = string(">>=")
LEFT_ASSIGN = string("<<=")
ADD_ASSIGN = string("+=")
SUB_ASSIGN = string("-=")
MUL_ASSIGN = string("*=")
DIV_ASSIGN = string("/=")
MOD_ASSIGN = string("%=")
AND_ASSIGN = string("&=")
XOR_ASSIGN = string("^=")
OR_ASSIGN = string("|=")
RIGHT_OP = string(">>")
LEFT_OP = string("<<")
INC_OP = string("++")
DEC_OP = string("--")
PTR_OP = string("->")
AND_OP = string("&&")
OR_OP = string("||")
LE_OP = string("<=")
GE_OP = string(">=")
EQ_OP = string("==")
NE_OP = string("!=")
SEMI = a(";")
OPEN_BLOCK = a("{") | string("<%")
CLOSE_BLOCK = a("}") | string("%>")
COMMA = a(",")
COLON = a(":")
EQ = a("=")
LEFT_PAREN = a("(")
RIGHT_PAREN = a(")")
OPEN_INDEX = a("[") | string("<:")
CLOSE_INDEX = a("]") | string(":>")
DOT = a(".")
AND = a("&")
NOT = a("!")
INVERT = a("~")
SUB = a("-")
ADD = a("+")
MUL = a("*")
DIV = a("/")
MOD = a("%")
LT = a("<")
GT = a(">")
XOR = a("^")
OR = a("|")
QMARK = a("?")