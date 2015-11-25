def words(source):
	return list(filter(lambda x: x != '', source.replace(';',' ; ').replace(',',' , ').replace('.', ' . ').replace(':', ' : ').split(' ')))

def group_clause(words, seps=(',')):
	ast = []
	if words.count(',') % 2 == 1:
		words = [','] + words
	while len(words):
		if words[0] in seps:
			t, *words = words
			ls = []
			while words[0] != t and len(words):
				w, *words = words
				ls.append(w)
			_, *words = words
			ast.append(('CLAUSE', group_clause(ls)))
		else:
			w, *words = words
			ast.append(w)
	return ast

NOUN_TEMPLATE = ['nom','voc','acc','gen','dat','abl']

NOUNS = {
	'M': { 'S': ['us','e','um','i','o','o'],
		   'P': ['i','i','os','orum','is','is']},
	'F': { 'S': ['a','a','am','ae','ae','a'],
		   'P': ['ae','ae','as','arum','is','is']},
	'N': { 'S': ['um','um','um','i','o','o'],
		   'P': ['i','i','os','orum','is','is']}
}

VERBS = {
	'PR': { 'S': ['o','as','at'], 
			'P': ['amus','atis','ant']},
	'PE': { 'S': ['i','is','it'], 
			'P': ['imus','itis','erunt']},
	'IM': { 'S': ['bam','bas','bat'], 
			'P': ['bamus','batis','bant']},
	'FU': { 'S': ['bo','bis','bit'], 
			'P': ['bimus','bitis','bunt']}
}

def has_ending(word, ending):
	return len(word) >= len(ending) and word[-len(ending):] == ending

def tag_endings(words):
	ast = []
	for word in words:
		if word[0] == 'CLAUSE':
			ast.append(('CLAUSE', tag_endings(word[1])))
			continue
		endings = []
		for gender in NOUNS.keys():
			for plurality in NOUNS[gender].keys():
				for i, ending in enumerate(NOUNS[gender][plurality]):
					if has_ending(word, ending):
						endings.append(('NOUN', gender, plurality, NOUN_TEMPLATE[i], word[:-len(ending)], ending))
		for tense in VERBS.keys():
			for plurality in VERBS[tense].keys():
				for i, ending in enumerate(VERBS[tense][plurality]):
					if has_ending(word, ending):
						endings.append(('VERB', tense, plurality, i + 1, word[:-len(ending)], ending))
		ast.append(('WORD',endings))
	return ast

def pprint(words,pad=""):
	for word in words:
		if word[0] == 'CLAUSE':
			pprint(word[1], pad=pad+" "*4)
		else:
			if len(word[1]):
				print(pad + word[1][0][4] + word[1][0][5])
			for pos in word[1]:
				print(pad,"  ",*pos[1:])

print(tag_endings(group_clause(words("""puella dormiat"""))))