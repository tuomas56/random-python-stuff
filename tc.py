import graph
from functools import partial
import sys

ASPECTS = {
	"aer": tuple(),
	"terra": tuple(),
	"ignis": tuple(),
	"aqua": tuple(),
	"ordo": tuple(),
	"perdito": tuple(),
	"alienis": ("vacuos","tenebrae"),
	"arbor": ("aer","herba"),
	"auram": ("praecantatio","aer"),
	"bestia": ("motus","victus"),
	"cognitio": ("spiritus","ignis"),
	"corpus": ("mortuus","bestia"),
	"exanimis": ("motus","mortuus"),
	"fabricum": ("humanus","instrumentum"),
	"fames": ("victus","vacuos"),
	"gelum": ("ignis","perdito"),
	"herba": ("victus","terra"),
	"humanus": ("bestia","cognitio"),
	"instrumentum": ("humanus","ordo"),
	"iter": ("motus","terra"),
	"limus": ("victus","aqua"),
	"lucrum": ("humanus","fames"),
	"lux": ("aer","ignis"),
	"machina": ("motus","instrumentum"),
	"messis": ("herba","humanus"),
	"metallum": ("terra","vitreus"),
	"meto": ("messis","instrumentum"),
	"mortuus": ("victus","perdito"),
	"motus": ("aer","ordo"),
	"pannus": ("instrumentum","bestia"),
	"perfodio": ("humanus","terra"),
	"permutatio": ("ordo","perdito"),
	"potentia": ("ordo","ignis"),
	"praecantatio": ("potentia","vacuos"),
	"sano": ("ordo","victus"),
	"sensus": ("aer","spiritus"),
	"spiritus": ("victus","mortuus"),
	"telum": ("instrumentum","perdito"),
	"tempestas": ("aer","aqua"),
	"tenebrae": ("vacuos","lux"),
	"tutamen": ("instrumentum","terra"),
	"vacuos": ("aer","perdito"),
	"venenum": ("aqua","perdito"),
	"victus": ("aqua","terra"),
	"vinculum": ("motus","perdito"),
	"vitium": ("praecantatio","perdito"),
	"vitreus": ("terra","ordo"),
	"volatus": ("aer","motus"),
	"desidia": ("vinculum","spiritus")
}

def string_distance(seq1, seq2):
    """
    Originally From: http://mwh.geek.nz/2009/04/26/python-damerau-levenshtein-distance/

    Calculate the Damerau-Levenshtein distance between sequences.

    This distance is the number of additions, deletions, substitutions,
    and transpositions needed to transform the first sequence into the
    second. Although generally used with strings, any sequences of
    comparable objects will work.

    Transpositions are exchanges of *consecutive* characters; all other
    operations are self-explanatory.

    This implementation is O(N*M) time and O(M) space, for N and M the
    lengths of the two sequences.
    """
    # Conceptually, this is based on a len(seq1) + 1 * len(seq2) + 1 matrix.
    # However, only the current and two previous rows are needed at once,
    # so we only store those.
    oneago = None
    thisrow = list(range(1, len(seq2) + 1)) + [0]
    for x in range(len(seq1)):
        # Python lists wrap around for negative indices, so put the
        # leftmost column at the *end* of the list. This matches with
        # the zero-indexed strings and saves extra calculation.
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in range(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
            # This block deals with transpositions
            if (x > 0 and y > 0 and seq1[x] == seq2[y - 1]
                and seq1[x-1] == seq2[y] and seq1[x] != seq2[y]):
                thisrow[y] = min(thisrow[y], twoago[y - 2] + 1)
    return thisrow[len(seq2) - 1]


def nearest_string(word,dictionary):
	return min(dictionary, key=partial(string_distance,word))

def build_graph():
	g = {}
	for aspect, connections in ASPECTS.items():
		if not len(connections):
			g[aspect] = {}
		else:
			if aspect not in g:
				g[aspect] = {}
			for connection in connections:
				if connection not in g:
					g[connection] = {}
				g[aspect].update({connection: 1})
				g[connection].update({aspect: 1})
	return g

def build_path(g,start,end):
	p = graph.dijkstra(g,start)
	node = p[1][end]
	path = [end]
	while node != start:
		path.insert(0,node)
		node = p[1][node]
	path.insert(0,start)
	return path


def spell_check(x):
	nearest = nearest_string(x,ASPECTS.keys())
	if nearest != x:
		if get(question,"Did you mean %s? " % nearest):
			return nearest
		else:
			return x
	else:
		return x

def question(x):
	if x in ('y','yes'):
		return True
	elif x in ('n','no'):
		return False
	else:
		raise ValueError()

def in_list(l):
	def wrapper(x):
		if x in l:
			return x
		else:
			raise ValueError()
	return wrapper

def compose(f,g):
	return lambda x: f(g(x))

def get(conv=lambda x:x,prompt="",error="Invalid input."):
	while True:
		try:
			return conv(input(prompt))
		except EOFError:
			print("Can't read, exiting.")
			sys.exit()
		except:
			print(error)

def main():
	g = build_graph()
	start = get(compose(in_list(list(ASPECTS.keys())),spell_check),"Please enter the start aspect: ","That aspect does not exist.")
	end = get(compose(in_list(list(ASPECTS.keys())),spell_check),"Please enter the end aspect: ","That aspect does not exist.")

	path = build_path(g,start,end)

	print("The shortest path from %s to %s is: %s" % (start,end,' -> '.join(path)))

if __name__ == "__main__":
	main()