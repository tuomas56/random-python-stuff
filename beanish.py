from collections import namedtuple
from operator import itemgetter

corpus = """ᔪᕒᖚᐧ ᘛᔭᐤ # frame 2663, "Where are you from?"
ᔪᖆᓄᐧ ᔪ, ᒣᖉ ᖊᐣᖽ ᖽᘛᕋᑦᐤ # frame 2664, "What happened to your leg?"
ᓭᘈ ᘊᒣᓭᐧᖊᔕ ᖆᘊᓭᒣᖊᐣᖗᐨ # frame 2668, "Get/Fetch/Bring (me/us) cream for-healing."
ᕒᖚᐧ ᘊᘖᑫᘖᒣᐣᖚ ᘛ ᓭᑦᐧ ᕒᖚᑫᕋ,ᐨ # frame 2671, "Where (...)."
ᘊᒣᓭᐧᖊᔕ ᖆᘊᓭᒣᖊᐣᖗᐨ # frame 2676, "Cream for-healing."
ᖚᑫᘖ ᓭᐧᖚ # frame 2697, "(...) you-wildling."
ᓭᘖᔭᓄᐨ # frame 2706, "Water."
ᖉᑦ,ᐦ ᓭᘖᔭᓄᐦ # frame 2708, "Yes! Water."
ᔪᖉᔭᑫ ᕒᖚᐧ ᘊᓭᐧᑲᐤ ᑦᘈᖽᐣ ᔭ ᖆᖽᒣ ᓭᘖᑦ ᖊᘊᐤ ᕋᖗ ᖆᕬᖉᔭ ᘖᐣᖗᔭ, ᘊᓭᘖᔭᓄᐤ # frame 2728, "(...) your land? (...)? (...) waters?"
ᖽᔕᐣᘖ ᖚᐣᘖᖗᑫ ᖆᐣᖽ ᘊᒣᑦᖽᖆᐨ # frame 2734, "We will go to the castle."
ᒣᓭᐧᖊᔕᐨ # frame 2797, "Cream."
ᑕᘊᐣᒣ ᘊᓭᑦᑕᖉᐨ ᑕᘊᐣᒣ ᘊᓭᘖᔭᓄᐨ ᓭᘖᔭᓄᐦ # frame 2802, "These lands. These seas. Water!"
ᖆᘈᘖ ᖽᔕᐣᘖ ᖚᒣᑕᑫᓭ ᖆᐣᖽ ᘊᒣᑦᖽᖆᐨ # frame 2806, "JohnDoe/Comrade, we shall go to the castle (now)."
ᖉᑦ,ᐨ # frame 2806, "Ok."
ᖆᓄᘈᖉᐣᐨ # frame 2821, "(name of the Beanie city)"
ᖉ, ᖆᐣᖚᔭ,ᐨ # frame 2823, "Good morning."
ᘊᒣᑦᖽᖆᐨ # frame 2827, "(Our/The) Castle."
ᖽᔕᐣᘖ ᖚᐣᘖᖗᑫ ᖆᐣᖽ ᘊᓭᘖᑦᓄᐨ # frame 2836, "We should go to the leader."
ᘈᘊᘖᐨ # frame 2841, "Hello."
ᖉ, ᖆᐣᖚᔭ,ᐨ # frame 2841, "Good morning."
ᖆᘈᘖᐦ ᖉ, ᖆᐣᖚᔭᐦ # frame 2842, "JohnDoe/Comrade! Good morning!"
ᘈᘊᘖᐨ # frame 2863, "Hello."
ᘈᘊᘖᐨ # frame 2864, "Hello."
ᕒᖚᐧ ᓭᔭᑦᘖ ᘛᖆᖚᘈᐤ # frame 2865, "Where are they from?"
ᖆᐣᑕᑦᖚᑫ ᓭᐧᘖ ᕒᖚᐧ ᘊᓭᐧᑲᐨ # frame 2866, "They are from the wildlands."
ᖉᔭᒣᘊᐣᘖᑫᖗ ᖽᘛᕋᑦᐨ # frame 2866, "One of them was attacked."
ᘛᐣ ᖆᔭᖊᖽ ᖊ,ᘖ ᘖᖆᒣᘛᐨ # frame 2880, "You can leave now."
ᔪᑕᐨ # frame 2880, "Ok."
ᘊᖊᑦᓄ ᘊᓭᐧᑲ # frame 2906, "Wildlands/Balearic Sea"
ᘊᖊᑦᓄ ?ᓄᐣᔭ # frame 2906, "Ionian Sea"
ᑫᘊᘊ # frame 2906, "Gibraltar"
ᘊᓭᑦᑕᖉ # frame 2906, "(...)"
ᘖᓄᘈᖉᐣ # frame 2906, "(...)"
ᓭᘊᘊ # frame 2906, '(...)'"""

Sentence = namedtuple('Sentence','frame text translation')

sentences = []

for line in corpus.split("\n"):
	line = line.split("#")
	line = [x.strip() for x in line]
	line[1] = [x.strip() for x in line[1].split(",")]
	sentences.append(Sentence(frame=int(line[1][0][6:]), text=line[0], translation=line[1][1][1:-1]))

totaltext = ' '.join(sentence.text for sentence in sentences)

freqs = sorted(list(set((x, totaltext.count(x)/len(totaltext)) for x in totaltext)), key=itemgetter(1), reverse=True)[1:]

print(len(freqs), "unique characters.")

print("Char | Freq\n============")
for (char, freq) in freqs:
	print(char," "*4,str(round(freq*100,2))+("0" if len(str(round(freq*100,2))) == 3 else "")+"%")

for frame, text, translation in sentences:
	print(frame, text, translation)
