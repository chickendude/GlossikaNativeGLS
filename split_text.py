# Use pdftotext to convert text file
# $ pdftotext [BOOKNAME].pdf -enc UTF-8 -raw -nopgbrk

import glob, os

import pdftotext

# ** if you want to add a new book, here's the place **
#
# If it's a regular book (with three parts: sentence, translation, and IPA)
# it should work just fine. Languages with other parts like a romanization
# may need to have a separate function written for them.
#

ACCEPTED_PDFS = (
	'GLOSSIKA-ENCA-F1-EBK.pdf',
	'GLOSSIKA-ENES-F1-EBK.pdf',
	'GLOSSIKA-ENES-F2-EBK.pdf',
	'GLOSSIKA-ENES-F3-EBK.pdf',
	'GLOSSIKA-ENZSZT-F1-EBK.pdf',
	'GLOSSIKA-ENZSZT-F2-EBK.pdf',
	'GLOSSIKA-ENZSZT-F3-EBK.pdf',
)

BOOKS = {
	'ENZSZT': {
		'types': ['EN', '简', 'PIN', 'IPA', '繁', 'PIN', 'IPA'],
		'F1': [50, 442],
		'F2': [50, 501],
		'F3': [50, 546],
	},
	'ENCA': {
		'types': ['EN', 'CA', 'IPA'],
		'F1': [37, 253],
		'F2': [0, 0],
		'F3': [0, 0],
	},
	'ENES': {
		'types': ['EN', 'ES', 'IPA'],
		'F1': [31, 266],
		'F2': [31, 295],
		'F3': [31, 321],
	},
}

PATH = "texts"
OUTPUT_FOLDER = ''

class Sentence:
	def __init__(self, index=0, sentence='', translation='', ipa=''):
		self.index = index
		self.sentence = sentence
		self.translation = translation
		self.ipa = ipa

	def __str__(self):
		return self.sentence


class SentenceRomanized:
	def __init__(self, index=0, sentence='', translation='', romanization='', ipa=''):
		self.index = index
		self.sentence = sentence
		self.translation = translation
		self.romanization = romanization
		self.ipa = ipa

	def __str__(self):
		return self.sentence


# extract special combined Mandarin simplified + traditional book
def extract_chinese_sentences(book, info, language_pair, series, callback=None):
	# set up generator
	if callback:
		next(callback)

	if series == 'F1':
		sentence_num = 1
	elif series == 'F2':
		sentence_num = 1001
	elif series == 'F3':
		sentence_num = 2001
	else:
		sentence_num = 1

	sentences_zs = []
	sentences_zt = []
	sentence_types = info['types']
	lines = book.split('\n')
	line_num = 0
	for line in lines:
		line_num += 1

		# send back progress report
		callback.send(line_num / len(lines))

		line = line.strip()

		# check if it's a sentence or just junk
		if language_pair in line or line.isdigit():
			continue

		# get the current type and the next one
		type, next_type = get_sentence_type(sentence_types, line)

		# make sure it's a valid sentence
		if type == None:
			continue

		if next_type == None:
			next_type = language_pair

		# if it's the first type, it's a new sentence
		if type == sentence_types[0]:
			# simplified sentence
			sentence_zs = SentenceRomanized(index=sentence_num)
			sentences_zs.append(sentence_zs)
			# traditional sentence
			sentence_zt = SentenceRomanized(index=sentence_num)
			sentences_zt.append(sentence_zt)
			sentence_num += 1

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
		if index == 0:
			sentence_zs.sentence = phrase
			sentence_zt.sentence = phrase
		if index == 1:
			sentence_zs.translation = phrase
		if index == 2:
			if sentence_zs.romanization == '':
				sentence_zs.romanization = phrase
			else:
				sentence_zt.romanization = phrase
		if index == 3:
			if sentence_zs.ipa == '':
				sentence_zs.ipa = phrase
			else:
				sentence_zt.ipa = phrase
		if index == 4:
			sentence_zt.translation = phrase

	create_romanized_sentence_pack(sentences_zs, 'EN-ZS')
	create_romanized_sentence_pack(sentences_zt, 'EN-ZT')

	#close generator
	if callback:
		callback.close()


def create_sentence_pack(sentences, language_pair):
	start = sentences[0].index
	end = sentences[-1].index
	filename = "{}-{}-{}.gsp".format(language_pair, str(start).zfill(4), end)
	directory = os.path.join(EXPORT_FOLDER, OUTPUT_FOLDER)
	if not os.path.exists(directory):
		os.makedirs(directory)
	filename = os.path.join(directory, filename)
	with open(filename, 'w') as f:
		f.write("index\tsentence\ttranslation\tIPA\tromanization\n".format())
		for sentence in sentences:
			f.write("{}\t{}\t{}\t{}\n".format(sentence.index, sentence.sentence, sentence.translation, sentence.ipa))


def create_romanized_sentence_pack(sentences, type):
	start = sentences[0].index
	end = sentences[-1].index
	filename = "{}-{}-{}.gsp".format(type, str(start).zfill(4), end)
	directory = os.path.join(EXPORT_FOLDER, OUTPUT_FOLDER)
	if not os.path.exists(directory):
		os.makedirs(directory)
	filename = os.path.join(EXPORT_FOLDER, OUTPUT_FOLDER, filename)
	with open(filename, 'w') as f:
		f.write("index\tsentence\ttranslation\tIPA\tromanization\n".format())
		for sentence in sentences:
			f.write("{}\t{}\t{}\t{}\t{}\n".format(sentence.index, sentence.sentence, sentence.translation, sentence.ipa,
												  sentence.romanization))


def get_sentence_type(types, line):
	for type in types:
		if type + " " in line:
			i = types.index(type)
			if i + 1 == len(types):
				return type, None
			else:
				return type, types[i + 1]
	return None, None


# extract regular books, languages without any romanization, just sentence, translation, and IPA
def extract_sentences(book, info, language_pair, series, callback=None):
	# set up generator
	if callback:
		next(callback)

	if series == 'F1':
		sentence_num = 1
	elif series == 'F2':
		sentence_num = 1001
	elif series == 'F3':
		sentence_num = 2001
	else:
		sentence_num = 1

	sentences = []
	sentence_types = info['types']
	lines = book.split('\n')
	line_num = 0
	for line in lines:
		line_num += 1

		# send back progress report
		callback.send(line_num / len(lines))

		line = line.strip()

		# check if it's a sentence or just junk
		if language_pair in line or line.isdigit():
			continue

		# get the current type and the next one
		type, next_type = get_sentence_type(sentence_types, line)

		# make sure it's a valid sentence
		if type == None:
			continue

		if next_type == None:
			next_type = language_pair

		# if it's the first type, it's a new sentence
		if type == sentence_types[0]:
			sentence = Sentence(index=sentence_num)
			sentences.append(sentence)
			sentence_num += 1

		_, phrase = line.split(type + " ")

		# next we check if it's a multi-line sentence
		if line_num < len(lines) and next_type not in lines[line_num] and not lines[line_num].strip().isdigit():
			phrase += " " + lines[line_num].strip()
			if line_num + 1 < len(lines) and next_type not in lines[line_num + 1] and not lines[
				line_num + 1].strip().isdigit():
				phrase += " " + lines[line_num + 1].strip()
		index = sentence_types.index(type)
		if index == 0:
			sentence.sentence = phrase
		if index == 1:
			sentence.translation = phrase
		if index == 2:
			sentence.ipa = phrase

	create_sentence_pack(sentences, "{}-{}".format(info['types'][0], info['types'][1]))

	#close generator
	if callback:
		callback.send(1)
		callback.close()


EXPORT_FOLDER = ""
def split_text(path, file_list, base_folder, unique_folder, callback=None):
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
		if len(book_info['types']) == 3:
			extract_sentences(book, book_info, language_pair, series, callback)
		else:
			extract_chinese_sentences(book, book_info, language_pair, series, callback)


def split():
	location = os.path.join(PATH, '*.pdf', 'output', '')
	split_text('', glob.glob(location))


if __name__ == '__main__':
	split()
