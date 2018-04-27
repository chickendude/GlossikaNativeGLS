import os, glob, shutil


def create_gls(language, output_folder, folder_to_zip):
	print("Zipping...")
	mp3_files = os.path.join(folder_to_zip, '*.mp3')
	lang1 = ''
	lang2 = ''
	book = ''
	for mp3 in glob.glob(mp3_files):
		filename = mp3.split('/')[-1]
		lang = filename.split(' - ')[0]
		if language.find(lang) == 0:
			lang1 = lang
		else:
			lang2 = lang
		if not lang1 == '' and not lang2 == '':
			book = filename.split(' - ')[1]
			break

	filename = "{}-{}-{}".format(lang1, lang2, book)
	gsp_files = glob.glob(os.path.join(folder_to_zip, '*.gsp'))
	if len(gsp_files) > 1:
		for gsp_file in gsp_files:
			if language[-2:] not in gsp_file:
				os.remove(gsp_file)
	filename = os.path.join(output_folder, filename)
	shutil.make_archive(filename, 'zip', folder_to_zip)
	print("Zip done")
	os.rename(filename + '.zip', filename + '.gls')
	print("Done: " + filename + ".gls")
	return filename + '.gls'


def split():
	create_gls('ENZS', '')


if __name__ == '__main__':
	split()
