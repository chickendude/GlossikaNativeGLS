import os, glob, shutil


def create_gls(languages: tuple, output_folder: str, folder_to_zip: str) -> list:
	"""

	:param languages: list of languages to create gls packages for
	:param output_folder: where to save the file
	:param folder_to_zip: where the mp3/gsp files are located
	:return:
	"""
	print("Zipping...")
	filenames = []
	for language in languages:
		language_folder = os.path.join(folder_to_zip, language)
		mp3_files = os.path.join(language_folder, '*.mp3')
		lang = ''
		book = ''
		for mp3 in glob.glob(mp3_files):
			filename = mp3.split('/')[-1]
			lang = filename.split(' - ')[0]
			book = filename.split(' - ')[1]
			break

		filename = "{}-{}".format(lang, book)
		gsp_files = glob.glob(os.path.join(language_folder, '*.gsp'))
		if len(gsp_files) > 1:
			for gsp_file in gsp_files:
				if language[-2:] not in gsp_file:
					os.remove(gsp_file)
		filename = os.path.join(output_folder, filename)
		shutil.make_archive(filename, 'zip', language_folder)
		print("Zip done")
		os.rename(filename + '.zip', filename + '.gls')
		print("Done: " + filename + ".gls")
		filenames.append(filename + ".gls")
	return filenames


def split():
	create_gls(('EN','ZS'), 'output', 'output')


if __name__ == '__main__':
	split()
