from pydub import AudioSegment
import os, glob


# ------------------ classes ------------------

class Segment:
	def __init__(self, start, end, id):
		self.start = start
		self.end = end
		self.id = id


class LoadedFile:
	def __init__(self, filename='', sentence_start=1, langs=[], lang1='', lang2='', book=''):
		self.filename = filename
		self.sentence_start = sentence_start
		self.langs = langs
		self.lang1 = lang1
		self.lang2 = lang2
		self.book = book


# ------------------ globals ------------------

ACCEPTED_LANGUAGES_F1 = (
	'ENCA',
	'ENES',
	'ENZS',
	'PBESM',
	# TRIANGULATIONS
	'PBENFR',
)

ACCEPTED_LANGUAGES_F2 = (
	'ENES',
	'ENZS',
	'PBESM',
)

ACCEPTED_LANGUAGES_F3 = (
	'ENES',
	'ENZS',
	'PBESM',
)

LANGUAGES = {
	'ENCA': ('EN', 'CA'),
	'ENES': ('EN', 'ES'),
	'ENZS': ('EN', 'ZS'),
	'PBESM': ('PB', 'ESM'),
	'PBENFR': ('PB', 'EN', 'FR'),
}

PATH = "files"
EXPORT_PATH = "output"
GTL_PATH = 'sentence_markings'

OUTPUT_FOLDER = ''

LOADED_FILE = LoadedFile()


# ------------------ main code ------------------

def load_segments(path):
	segments = []
	with open(path, 'r') as f:
		filename = f.readline().strip() + ".mp3"
		for line in f.readlines():
			start, end, id = line.split("\t")
			segments.append(Segment(float(start), float(end), int(id) - 1))
	# update file information
	filename_parts = filename.split('-')
	lang = filename_parts[0]
	LOADED_FILE.filename = filename.rstrip('.mp3')
	LOADED_FILE.sentence_start = int(filename.strip('.mp3')[-4:])
	LOADED_FILE.langs = LANGUAGES[lang]
	LOADED_FILE.lang1 = LANGUAGES[lang][0]
	LOADED_FILE.lang2 = LANGUAGES[lang][1]
	LOADED_FILE.book = filename_parts[1]
	return segments, filename


def extract_sentences(filepath, segments):
	track = AudioSegment.from_mp3(filepath)
	for sentence in segments:
		# extract times and id
		start = int(sentence.start * 1000)
		end = int(sentence.end * 1000)
		id = sentence.id
		offset = LOADED_FILE.sentence_start

		# check which type it is
		langs = LOADED_FILE.langs
		language = langs[id % len(langs)]
		# language = LOADED_FILE.lang1 if id % 2 == 0 else LOADED_FILE.lang2

		export_name = "{} - {} - {num:04d}.mp3".format(language, LOADED_FILE.book, num=int(id / len(langs)) + offset)
		directory = os.path.join(EXPORT_PATH, OUTPUT_FOLDER, language)
		if not os.path.exists(directory):
			os.makedirs(directory)
		export_path = os.path.join(directory, export_name)
		print("Extracting '{}'".format(export_path))
		segment = track[start:end]
		segment.export(export_path, codec='mp3')


def split_audio(gtl_path, gms_path, language, book, base_folder, unique_folder, callback=None):
	global OUTPUT_FOLDER, EXPORT_PATH
	OUTPUT_FOLDER = unique_folder
	EXPORT_PATH = base_folder

	if callback:
		next(callback)

	location = os.path.join(gtl_path, language, book, '*.gtl')
	list_files = glob.glob(location)
	for list_file in list_files:
		# send progress back
		if callback:
			callback.send(list_files.index(list_file) / len(list_files))

		segments, filename = load_segments(list_file)

		filepath = os.path.join(gms_path, filename)

		print("Found file: " + filepath)
		extract_sentences(filepath, segments)

	if callback:
		callback.send(1)
		callback.close()


def split():
	split_audio(GTL_PATH, PATH, 'PBENFR', 'F3', EXPORT_PATH, '')


if __name__ == '__main__':
	split()
