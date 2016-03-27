import random
import nltk

class Markov(object):

	def __init__(self, open_file):
		self.cache = {}
		self.open_file = open_file
		self.words = self.file_to_words()
		self.word_size = len(self.words)
		self.characters = {}
		self.database()
		self.punctuation = [".", "!", "?"]

	def getCharacters(self):
		currentChar = ""
		self.open_file.seek(0)
		for line in self.open_file:
			#line.strip()
			if ":" in line:
				name = line[0:len(line)-2]
				currentChar = name
			elif line != "\n":
				#print currentChar + ": " + line
				if currentChar not in self.characters:
					self.characters[currentChar] = []
				line = line.strip()
				if line[len(line)-1] in self.punctuation:
					line = line[0:len(line)-1]
				self.characters[currentChar].append(line.strip())

	def printCharacters(self):
		for c in self.characters:
			print c + ": "
			for sent in self.characters[c]:
				print sent


	def file_to_words(self):
		self.open_file.seek(0)
		data = self.open_file.read()
		words = data.split()
		return words

	def triples(self):
		if len(self.words) < 3:
			return

		for i in range(len(self.words) - 2):
			yield (self.words[i], self.words[i+1], self.words[i+2])

	def database(self):
		for w1, w2, w3 in self.triples():
			key = (w1, w2)
			if (key in self.cache):
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]

	def generate_markov_text(self, size=25):
		seed = random.randint(0, self.word_size-3)
		seed_word, next_word = self.words[seed], self.words[seed+1]
		w1, w2 = seed_word, next_word
		gen_words = []
		for i in xrange(size):
			gen_words.append(w1)
			w1, w2 = w2, random.choice(self.cache[(w1,w2)])
		gen_words.append(w2)
		return ' '.join(gen_words)

	def markov_test(self, size=25):
		pass


file = open('spice1.txt')
test = Markov(file)
test.getCharacters()
test.printCharacters()
a = test.generate_markov_text() 
print a


