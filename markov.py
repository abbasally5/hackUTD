import random
import nltk
import os
#from nltk import NgramModel

class Markov(object):

	def __init__(self, directory):
		self.cache = {}
		self.dir = directory
		self.open_file = None
		#self.file_words = self.file_to_words()
		self.words = []
		self.word_size = 0
		self.characters = {}
		#self.database()
		self.punctuation = [".", "!", "?"]
		self.saved_path = os.getcwd()

	def goToSavedPath(self):
		print 'in goToSavedPath'
		if (not (os.getcwd() is self.saved_path)):
			self.changeDir()

	def changeDir(self):
		try:
			os.chdir(self.saved_path)
		except Exception as e:
			print e

	def getCharacters(self):
		currentChar = ""
		print os.getcwd()
		self.goToSavedPath()
		os.chdir('scripts')
		os.chdir(self.dir)
		for i in os.listdir(os.getcwd()):
			self.open_file = open(i, 'r+')
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
					#if line[len(line)-1] in self.punctuation:
						#line = line[0:len(line)-1]
					self.characters[currentChar].append(line)

	def printCharacters(self):
		for c in self.characters:
			print c + ": "
			for sent in self.characters[c]:
				print sent


	def file_to_words(self):
		print os.getcwd()
		os.chdir('scripts')
		os.chdir(self.dir)
		for i in os.listdir(os.getcwd()):
			print i
			self.open_file = open(i)
			self.open_file.seek(0)
			data = self.open_file.read()
			data = data.split()
			for d in data:
				words.append(d)
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

	def generate_markov_text(self, size=15):
		#size = random.randint(0, self.word_size/10)

		# picking a good seed
		seed = 0
		while True:
			seed = random.randint(0, self.word_size-3)
			word = self.words[seed]
			if word[len(word)-1] in self.punctuation:
				seed += 1
				break

		seed_word, next_word = self.words[seed], self.words[seed+1]
		w1, w2 = seed_word, next_word
		gen_words = []
		for i in xrange(size):
			gen_words.append(w1)
			#print size - i
			if w1[len(w1)-1] in self.punctuation and (size - i) < 5:
				return ' '.join(gen_words)
			w1, w2 = w2, random.choice(self.cache[(w1,w2)])
		gen_words.append(w2)
		return ' '.join(gen_words)

	def availableChars(self):
		for c in self.characters:
			print c

	def getWordsForChar(self, char):
		self.words = ' '.join(sent for sent in self.characters[char]).split()
		#print self.words
		self.word_size = len(self.words)
		#print self.word_size
		self.database()

'''
# testing
folder = 'Spice_and_Wolf'
#file = open('spice1.txt')
test = Markov(folder)
test.getCharacters()
test.availableChars()
test.getWordsForChar('Holo')
print ' '
a = test.generate_markov_text() 
print a
'''

