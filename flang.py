from funcparserlib.parser import *
from funcparserlib.lexer import make_tokenizer
from functools import partial

token_specs = [
	("NL", (r"[\r\n]+",)),
	("WS", (r"[ \t]+",)),
	("NAME", (r"[A-Za-z_\$@][A-Za-z0-9_]+",)),
	("STRING", (r'("[^"]*")|'+r"('[^']')",)),
	("LCB", (r"\{",)),
	("RCB", (r"\}",)),
	("LB", (r"\(",)),
	("RB", (r"\)",)),
	("NUM", (r"[0-9]+(\.[0-9]+)?",)),
	("OP", (r"(\-\>)|(\:\>)|(\:\=\>)|(\=\>)|(\>\>)|\|",))
]

lex = make_tokenizer(token_specs)

tvk = lambda type, value: some(lambda t: t.type == type and t.value == value)
tk = lambda type: some(lambda t: t.type == type)
op = lambda value: tvk("OP", value)


value = forward_decl()
block = skip(tk("LCB")) + maybe(value + many(skip(tk("NL")) + value)) + skip(tk("RCB"))
bracket = skip(tk("LB")) + value + skip(tk("RB"))
literal = tk("STRING") | tk("NUM")

r_assign = value + skip(op("=>")) + tk("NAME")
r_map = value + skip(op(":>")) + value
r_filter = value + skip(op(":=>")) + value
r_if = value + skip(op("->")) + value + maybe(skip(op("|")) + value)
r_apply = value + skip(op(">>")) + value

value.define(literal|r_apply | r_map | r_filter | r_assign | r_if | bracket | block)

print(value.parse(list(lex("""3.4:>f"""))))