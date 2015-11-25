Keywords = """
if
elif
else
while
for
def
"""

Keywords = Keywords.split()

OneCharacterSymbols = """
=
( )
< >
/ * + -
~ | ^ &
, .
"""

OneCharacterSymbols = OneCharacterSymbols.split()

TwoCharacterSymbols = """
==
<=
>=
!=
**
+=
-=
*=
/=
or
is
"""

TwoCharacterSymbols = TwoCharacterSymbols.split()

ThreeCharacterSymbols = """
**=
//=
not
and
"""

ThreeCharacterSymbols = ThreeCharacterSymbols.split()

import string

IDENTIFIER_STARTCHARS = string.letters
IDENTIFIER_CHARS = string.letters + string.digits + "_"

NUMBER_STARTCHARS = string.digits
NUMBER_CHARS = string.digits + "."

STRING_STARTCHARS = "'" + '"'
WHITESPACE_CHARS = " \t\n"

STRING = "String"
IDENTIFIER = "Identifier"
NUMBER = "Number"
WHITESPACE = "Whitespace"
COMMENT = "Comment"
EOF = "Eof"

class Token:
	def __init__(self,startChar):
		self.cargo = startChar.cargo

		self.sourceText = startChar.sourceText
		self.lineIndex = startChar.lineIndex
		self.colIndex = startChar.colIndex

		self.type = None

	def show(self,showLineNumbers=False,**kwargs):
		align = kwargs.get("align",True)
		if align:
			tokenTypeLen = 12
			space = " "
		else:
			tokenTypeLen = 0
			space = ""

		if showLineNumbers:
			s = str(self.lineIndex).rjust(6) + str(self.colIndex).rjust(4) + "   "
		else:
			s = ""

		if self.type == self.cargo:
			s = s + "Symbol".ljust(tokenTypeLen,".") + ":" + space + self.type
		elif self.type == WHITESPACE:
			s = s + "Whitespace".ljust(tokenTypeLen,".") + ":" + space + repr(self.cargo)
		else:
			s = s + self.type.ljust(tokenTypeLen,".") + ":" + space + self.cargo
		return s
	guts = property(show)