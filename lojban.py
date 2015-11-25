dictionary = [
	('basti fa', 'with'),
	('ro', 'for'),
	("vidnyja'o", 'print'),
	('nenri', 'in'),
	('lujvo', 'word'),
	('jbovlaste', 'dictionary'),
	('basygau', 'replace'),
	('(te tcidu fe)', 'read'),
	('datnyvei','file'),
	('vlamei', 'text'),
	('kargau', 'open'),
	('la .lojban.', 'lojban'),
	('no', '0'),
	('pa', '1'),
	('as', ''),
	('with', 'basti fa'),
	('for', 'ro'),
	('print', "vidnyja'o"),
	('in', 'nenri'),
	('word', 'lujvo'),
	('dictionary', 'jbovlaste'),
	('replace', 'basygau'),
	('read', '(te tcidu fe)'),
	('file', 'datnyvei'),
	('text', 'vlamei'),
	('open', 'kargau'),
	('lojban', '(la .lojban.)'),
	('0', 'no'),
	('1', 'pa')
]

with open('lojban.py', 'r') as file:
	text = file.read()

for word in dictionary:
	text = text.replace(word[0], word[1])

print(text)

