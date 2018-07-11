# GlossikaNative GLS packager
A set of Python scripts to create GLS packages for use with the Natibo app. The text splitter uses pdftotext
which is only available on Linux, sorry Windoze users! Audio splitter should work on Linux/Windoze.

# split_text.py
This splits the PDFs into individual sentences and saves all sentences in a tab separated file with the sentence number
and various sentence parts (sentence, ipa, romanization, etc.). It relies on [pdftotext](https://github.com/jalan/pdftotext)
and isn't available on Windoze, unfortunately. You can try the online version of
these scripts if you're on Windoze.

# split_audio.py
This splits the audio from the GMS files using timings taken from Audacity + a one-line header pointing to the filename
of the audio file.

# create_gls.py
This packages everything together into a zip file and renames it as a .gls file that can be sent to [Natibo](https://github.com/chickendude/Natibo).

# cleanup.py
Some things to help clean up the timing files that Audacity spits out.

# License
All code (written by me) is released into the Public Domain.
