# GlossikaNative GLS packager
A set of Python scripts to create GLS packages for use with the Natibo app. The text splitter uses pdftotext
which is only available on Linux, sorry Windoze users! Audio splitter should work on Linux/Windoze.

## Scripts and their functions

# split_text.py
This splits the PDFs into individual sentences and saves all sentences in a tab separated file with the sentence number
and various sentence parts (sentence, ipa, romanization, etc.). It relies on [pdftotext](https://github.com/jalan/pdftotext)
and isn't available on Windoze, unfortunately. You can try the online version of
these scripts if you're on Windoze.

# split_gms.py
This splits the audio from the GMS files into individual files using the silence as a seperator.

# split_audio.py
This splits the audio from the GMS files using timings taken from Audacity + a one-line header pointing to the filename
of the audio file. `split_gms.py` should be used to have automatic conversion. This is just here in case it's important for someone in the future again.

# create_gls.py
This packages everything together into a zip file and renames it as a .gls file that can be sent to [Natibo](https://github.com/chickendude/Natibo).

# cleanup.py
Some things to help clean up the timing files that Audacity spits out.

# Usage
You will need to create a `texts`, `files` and `output` directory. Put all your PDFs `texts`, GMS-B files (for example) into `files`. Run `split_text.py` followed by `split_gms.py`.
The result will be in the `output` directory.

There are various ways of doing this.

Here is an example:

```
git clone https://github.com/chickendude/GlossikaNativeGLS
cd GlossikaNativeGLS

mkdir texts files output
cp ~/GlossikaCourses/Spanish/ENES-F123-EBK/*.pdf texts
cp ~/GlossikaCourses/Spanish/ENES-F1-GMS/GMS-B/*.mp3 files

python3 ./split_text.py 
Checking 'texts/GLOSSIKA-ENES-F2-EBK.pdf'
Checking 'texts/GLOSSIKA-ENES-F1-EBK.pdf'
Checking 'texts/GLOSSIKA-ENES-F3-EBK.pdf'

python3 ./split_gms.py   
Analyzing 'files/ENES-F1-GMS-B-0001.mp3'
```

# License
All code (written by me) is released into the Public Domain.
