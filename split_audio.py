from pydub import AudioSegment
import os, glob


# import cleanup

# ------------------ classes ------------------

class Segment:
	def __init__(self, start, end, id):
		self.start = start
		self.end = end
		self.id = id


class LoadedFile:
	def __init__(self, filename='', sentence_start=1, lang1='', lang2='', book=''):
		self.filename = filename
		self.sentence_start = sentence_start
		self.lang1 = lang1
		self.lang2 = lang2
		self.book = book


# ------------------ globals ------------------

ACCEPTED_LANGUAGES_F1 = (
	'ENES',
	'ENZS',
)
ACCEPTED_LANGUAGES_F2 = (

)

ACCEPTED_LANGUAGES_F3 = (

)

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
	LOADED_FILE.filename = filename.rstrip('.mp3')
	LOADED_FILE.sentence_start = int(filename.strip('.mp3')[-4:])
	LOADED_FILE.lang1 = filename[:2]
	LOADED_FILE.lang2 = filename[2:4]
	LOADED_FILE.book = filename[5:7]
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
		language = LOADED_FILE.lang1 if id % 2 == 0 else LOADED_FILE.lang2

		export_name = "{} - {} - {num:04d}.mp3".format(language, LOADED_FILE.book, num=int(id / 2) + offset)
		directory = os.path.join(EXPORT_PATH, OUTPUT_FOLDER)
		if not os.path.exists(directory):
			os.makedirs(directory)
		export_path = os.path.join(EXPORT_PATH, OUTPUT_FOLDER, export_name)
		print("Extracting '{}'".format(export_path))
		segment = track[start:end]
		segment.export(export_path, codec='mp3')


def split_audio(gtl_path, gms_path, language, base_folder, unique_folder, callback=None):
	global OUTPUT_FOLDER, EXPORT_PATH
	OUTPUT_FOLDER = unique_folder
	EXPORT_PATH = base_folder

	if callback:
		next(callback)

	location = os.path.join(gtl_path, language, '*.gtl')
	list_files = glob.glob(location)
	for list_file in list_files:
		# send progress back
		callback.send(list_files.index(list_file) / len(list_files))

		segments, filename = load_segments(list_file)

		filepath = os.path.join(gms_path, filename)

		print("Found file: " + filepath)
		extract_sentences(filepath, segments)

	if callback:
		callback.send(1)
		callback.close()

def split():
	split_audio(GTL_PATH, PATH, 'ENZS', EXPORT_PATH, '')


if __name__ == '__main__':
	split()