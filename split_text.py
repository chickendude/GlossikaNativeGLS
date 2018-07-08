import glob, os

import pdftotext

# ** if you want to add a new book, here's the place **
#
# If it's a regular book (with three parts: sentence, translation, and IPA)
# it should work just fine. Languages with other parts like a romanization
# may need to have a separate function written for them.
#

BOOKS = {
	# ENGLISH
	'ENCA': {
		'languages': ['EN', 'CA'],
		'types': ['EN', 'CA', 'IPA'],
		'F1': [37, 253],
		'F2': [37, 266],
		'F3': [37, 283],
	},
	'ENDE': {
		'languages': ['EN', 'DE'],
		'types': ['EN', 'DE', 'IPA'],
		'F1': [37, 270],
		'F2': [37, 297],
		'F3': [37, 330],
	},
	'ENEL': {
		'languages': ['EN', 'EL'],
		'types': ['EN', 'EL', 'ROM', 'IPA'],
		'F1': [29, 309],
		'F2': [29, 346],
		'F3': [29, 379],
	},
	'ENES': {
		'languages': ['EN', 'ES'],
		'types': ['EN', 'ES', 'IPA'],
		'F1': [31, 266],
		'F2': [31, 295],
		'F3': [31, 321],
	},
	'ENESM': {
		'languages': ['EN', 'ESM'],
		'types': ['EN', 'ESM', 'IPA'],
		'F1': [29, 262],
		'F2': [29, 288],
		'F3': [29, 313],
	},
	'ENNL': {
		'languages': ['EN', 'NL'],
		'types': ['EN', 'NL', 'IPA'],
		'F1': [32, 266],
		'F2': [32, 285],
		'F3': [32, 315],
	},
	'ENRU': {
		'languages': ['EN', 'RU'],
		'types': ['EN', 'RU', 'IPA', 'ROM'],
		'F1': [36, 314],
		'F2': [36, 358],
		'F3': [36, 400],
	},
	'ENTGL': {
		'languages': ['EN', 'TGL'],
		'types': ['EN', 'TGL'],
		'F1': [29, 219],
		'F2': [29, 235],
		'F3': [29, 252],
	},
	'ENTH': {
		'languages': ['EN', 'TH'],
		'types': ['EN', 'TH', 'IPA'],
		'F1': [34, 249],
		'F2': [34, 256],
		'F3': [34, 285],
	},
	'ENTR': {
		'languages': ['EN', 'TR'],
		'types': ['EN', 'TR', 'IPA'],
		'F1': [29, 256],
		'F2': [29, 280],
		'F3': [29, 304],
	},
	# 'ENUKR': {
	# 	'languages': ['EN', 'UKR'],
	# 	'types': ['EN', 'UKR', 'IPA'],
	# 	'F1': [29, 262],
	# 	'F2': [29, 293],
	# 	'F3': [29, 318],
	# },
	'ENZSZT': {
		'languages': ['EN', 'ZS', 'ZT'],
		'types': ['EN', '简', 'PIN', 'IPA', '繁', 'PIN', 'IPA'],
		'F1': [50, 442],
		'F2': [50, 501],
		'F3': [50, 546],
	},
	# PORTUGUESE - BRAZIL
	'PBESM': {
		'languages': ['PB', 'ESM'],
		'types': ['PB', 'ESM', 'IPA'],
		'F1': [32, 267],
		'F2': [32, 296],
		'F3': [32, 323],
	},

	# TRIANGULATIONS
	'PBENFR': {
		'languages': ['PB', 'EN', 'FR'],
		'types': ['PB', 'EN', 'IPA', 'FR', 'IPA'],
		'F1': [48, 369],
		'F2': [48, 428],
		'F3': [48, 473],
	},
}

PATH = "texts"
OUTPUT_FOLDER = ''


class Sentence:
	def __init__(self, index=0, sentence='', translation='', ipa='', romanization=''):
		self.index = index
		self.sentence = sentence
		self.translation = translation
		self.ipa = ipa
		self.romanization = romanization

	def __str__(self):
		return self.sentence

	def __repr__(self):
		return "{}. sent: '{}' // ipa '{}'".format(self.index, self.sentence, self.ipa)


# extract special combined Mandarin simplified + traditional book
def extract_chinese_sentences(book, info, language_pair, series, callback=None):
	# set up generator
	if callback:
		next(callback)

	if series == 'F1':
		sentence_num = 0
	elif series == 'F2':
		sentence_num = 1000
	elif series == 'F3':
		sentence_num = 2000
	else:
		sentence_num = 0

	sentences = []
	sentence_types = info['types']
	lines = book.split('\n')
	line_num = 0
	for line in lines:
		line_num += 1

		# send back progress report
		if callback:
			callback.send(line_num / len(lines))

		line = line.strip()

		# check if it's a sentence or just junk
		if language_pair in line or line.isdigit() or 'GMS #' in line:
			continue

		# get the current type and the next one
		type, next_type = get_sentence_type(sentence_types, line)

		# make sure it's a valid sentence
		if type == None:
			continue

		if next_type == None:
			next_type = language_pair

		if type == info['languages'][0]:
			sentence_num += 1
			sentences.append([])

		if type in ('EN', '简', '繁',):
			sentence = Sentence(index=sentence_num)
			sentences[-1].append(sentence)

		# remove type prefix
		_, phrase = line.split(type + " ")

		# next we check if it's a multi-line sentence
		if line_num < len(lines):
			line1 = lines[line_num].strip()
			if next_type not in line1 and not line1.isdigit() and language_pair not in line1:
				phrase += " " + lines[line_num].strip()
				if line_num + 1 < len(lines):
					line2 = lines[line_num + 1].strip()
					if next_type not in line2 and not line2.isdigit() and language_pair not in line2:
						phrase += " " + lines[line_num + 1].strip()
		index = sentence_types.index(type)
		if index == 0 or index == 1 or index == 4:
			sentence.sentence = phrase
		if index == 2 or index == 5:
			if not sentences[-1][0].romanization:
				sentences[-1][0].romanization = phrase
			sentence.romanization = phrase
		if index == 3 or index == 6:
			sentence.ipa = phrase

	create_sentence_packs(sentences, series, info['languages'])

	# close generator
	if callback:
		callback.close()


def create_sentence_packs(sentences, series, languages):
	start = sentences[0][0].index
	end = sentences[-1][0].index
	for language in languages:
		filename = "{}-{}-{}.gsp".format(language, str(start).zfill(4), end)
		directory = os.path.join(EXPORT_FOLDER, OUTPUT_FOLDER, language, series)
		if not os.path.exists(directory):
			os.makedirs(directory)
		index = languages.index(language)
		filename = os.path.join(directory, filename)
		with open(filename, 'w') as f:
			f.write("index\tsentence\tIPA\tromanization\n".format())
			for sentence_set in sentences:
				sentence = sentence_set[index]
				if sentence.romanization:
					f.write("{}\t{}\t{}\t{}\n".format(sentence.index, sentence.sentence.strip(), sentence.ipa.strip(),
													  sentence.romanization.strip()))
				else:
					f.write("{}\t{}\t{}\n".format(sentence.index, sentence.sentence.strip(), sentence.ipa.strip()))


def get_sentence_type(types, line):
	for type in types:
		if line.strip().startswith(type + " "):
			i = types.index(type)
			if i + 1 == len(types):
				return type, None
			else:
				return type, types[i + 1]
	return None, None


# extract regular triangulation books, languages without any romanization, just sentence and IPA
def extract_sentences(book, info, language_pair, series, callback=None):
	# set up generator
	if callback:
		next(callback)

	if series == 'F1':
		sentence_num = 0
	elif series == 'F2':
		sentence_num = 1000
	elif series == 'F3':
		sentence_num = 2000
	else:
		sentence_num = 0

	sentences = []
	sentence_types = info['types']
	lines = book.split('\n')
	line_num = 0
	for line in lines:
		line_num += 1

		# send back progress report
		if callback:
			callback.send(line_num / len(lines))

		line = line.strip()

		# check if it's a sentence or just junk
		if language_pair in line or line.isdigit() or 'GMS #' in line:
			continue

		# get the current type and the next one
		type, next_type = get_sentence_type(sentence_types, line)

		# make sure it's a valid sentence
		if type == None:
			continue

		if next_type == None:
			next_type = language_pair

		if type == info['languages'][0]:
			sentence_num += 1
			sentences.append([])

		# if it's the first type, it's a new sentence
		if type in info['languages']:
			sentence = Sentence(index=sentence_num)
			sentences[-1].append(sentence)

		_, phrase = line.split(type + " ")

		# next we check if it's a multi-line sentence
		if line_num < len(lines) and next_type not in lines[line_num] and not lines[line_num].strip().isdigit():
			phrase += " " + lines[line_num].strip()
			if line_num + 1 < len(lines) and next_type not in lines[line_num + 1] and not lines[
				line_num + 1].strip().isdigit():
				phrase += " " + lines[line_num + 1].strip()
		try:
			index = sentence_types.index(type)
		except IndexError:
			print("INDEX ERROR: " + type + "/" + sentence.index)
		if index == 0 or index == 1:
			sentence.sentence = phrase
		if type == 'IPA':
			sentence.ipa = phrase
		if type == 'ROM':
			sentence.romanization = phrase

	create_sentence_packs(sentences, series, info['languages'])

	# close generator
	if callback:
		callback.send(1)
		callback.close()


EXPORT_FOLDER = ""


def split_text(path, file_list, base_folder='', unique_folder='', callback=None):
	global OUTPUT_FOLDER, EXPORT_FOLDER
	OUTPUT_FOLDER = unique_folder
	EXPORT_FOLDER = base_folder
	for filename in file_list:
		print("Checking '{}'".format(filename))

		try:
			_, language_pair, series, _ = filename.split('-')
		except ValueError:
			print("'{}' isn't a valid PDF name.".format(filename))
			continue

		filename = os.path.join(path, filename)
		with open(filename, "rb") as f:
			pdf = pdftotext.PDF(f)

		if language_pair not in pdf[10]:
			print("PDF name doesn't seem to match the PDF contents.")
			continue

		# get book-specific information
		book_info = BOOKS[language_pair]
		start, end = book_info[series]

		# extract all sentences into a single string
		book = ""
		for i in range(start, end):
			book += pdf[i]

		# extract all sentences
		if language_pair == 'ENZSZT':
			extract_chinese_sentences(book, book_info, language_pair, series, callback)
		else:
			extract_sentences(book, book_info, language_pair, series, callback)


def split():
	location = os.path.join(PATH, '*.pdf')
	split_text('', glob.glob(location), 'output', '')


if __name__ == '__main__':
	split()
