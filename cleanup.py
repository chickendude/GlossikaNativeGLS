import glob
import os

PATH = 'sentence_markings'
LANG_PAIR = 'ENZS'
BOOK = 'F3'

def cleanup():
	os.chdir(PATH)
	os.chdir(LANG_PAIR)
	os.chdir(BOOK)
	for filename in glob.glob('*.txt'):
		print("Checking '{}'".format(filename))
		contents = ''
		with open(filename, 'r') as list_file:
			new_filename = filename.replace('txt', 'gtl')
			lang_pair = LANG_PAIR.lower()
			if lang_pair not in new_filename:
				new_filename = lang_pair + "_" + new_filename
				os.rename(filename, new_filename)
			line = list_file.readline()
			languages, sentence_start = new_filename.strip('.gtl').split('_')
			fluency_num = int(sentence_start[0]) + 1
			if not 'GMS-B' in line:
				list_file.seek(0)
			contents = '{}-F{}-GMS-B-{}\n{}'.format(languages.upper(), fluency_num, sentence_start,
													list_file.read().replace(',', '.'))
		if contents:
			with open(new_filename, 'w') as list_file:
				list_file.write(contents)


if __name__ == '__main__':
	cleanup()
