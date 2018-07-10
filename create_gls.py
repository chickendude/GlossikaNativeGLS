import os, glob, shutil


def create_gls(languages: tuple, books: tuple, output_folder: str, folder_to_zip: str) -> list:
	"""

	:param languages: list of languages to create gls packages for
	:param output_folder: where to save the file
	:param folder_to_zip: where the mp3/gsp files are located
	:return:
	"""
	print("Zipping...")
	filenames = []
	for language in languages:
		for book in books:
			language_folder = os.path.join(folder_to_zip, language, book)
			mp3_files = os.path.join(language_folder, '*.mp3')
			filename = "{}-{}".format(language, book)
			filename = os.path.join(output_folder, filename)
			shutil.make_archive(filename, 'zip', language_folder)
			print("Zip done")
			os.rename(filename + '.zip', filename + '.gls')
			print("Done: " + filename + ".gls")
			filenames.append(filename + ".gls")
	return filenames


def split():
	create_gls(('EN', 'EL',), ('F1', 'F2', 'F3'), 'output', 'output')


if __name__ == '__main__':
	split()
