
from mingus.midi import *
from mingus.containers import *

from mingus.midi import *
from mingus.extra import *

import random
import subprocess
import time
import re
import os

################################################
# Score template

SCORE_TEMPLATE = """
#(set-default-paper-size "a6landscape" )
\\header {
    tagline = ""
  }
\\score{
  {
  %s
  }
  \\header {
    piece = "Dictée %i"
  }
}
"""

################################################
# Parameters

note_min = int(Note("A-3"))
note_max = int(Note("A-5"))
interval_max = 6
nb_notes = 10
note_given = "A-4"
fluidsynth_sf2 = '/home/lemezoth/Downloads/Nice-Steinway-v3.8.sf2'
nb_generate = 50

################################################
# Export functions

def export_score(track, dictee_number, file_name="track"):
	t_lily = lilypond.from_Track(track)
	lilypond.to_pdf(SCORE_TEMPLATE % (t_lily, dictee_number), file_name+".pdf")
	subprocess.call(['pdftoppm', '-png', '-r', '300', '-singlefile', file_name+'.pdf', file_name],
	stdout=subprocess.PIPE)
	os.remove(file_name+'.pdf')

def export_wav(track, bpm=50, file_name="output"):
	midi_file_out.write_Track("output.mid", track, bpm=bpm)

	subprocess.call(['fluidsynth', '-F', file_name+'.wav', fluidsynth_sf2, 'output.mid'],
		stdout=subprocess.PIPE,
		universal_newlines=True)
	os.remove('output.mid')

def export_movie(file_name_audio="output", file_name_score="score", file_name_score_default="score_default"):
	file_name_movie = 'output/'+'dictee_%s.mp4'%(dictee_number)
	print("export movie", file_name_movie)

	# Export video with sound
	subprocess.call(['ffmpeg', '-loglevel', 'error' ,'-r', '20', '-loop', '1', '-y', '-i', file_name_score_default+'.png', '-i', file_name_audio+'.wav', '-shortest', '-acodec', 'mp3', '-vcodec', 'libx264', '-crf', '25', 'output.mp4'])
	
	# Export video with solution
	subprocess.call(['ffmpeg', '-loglevel', 'error' ,'-r', '20', '-loop', '1', '-y', '-i', file_name_score+'.png', '-t', '5', '-vcodec', 'libx264', '-crf', '25', 'output_solution.mp4'])

	## Concat video files
	list_file="""file 'output.mp4'
	file 'output_solution.mp4'
	"""
	with open('list_file.txt', 'w') as f:
		f.write(list_file)
	
	subprocess.call(['ffmpeg', '-loglevel', 'error', '-y','-f', 'concat', '-safe', '0', '-i', 'list_file.txt', '-c', 'copy', file_name_movie])

	# Remove files
	os.remove('output_solution.mp4')
	os.remove('output.mp4')

	os.remove(file_name_score+'.png')
	os.remove(file_name_score_default+'.png')
	os.remove(file_name_audio+'.wav')
	os.remove('list_file.txt')

################################################

for dictee_number in range(nb_generate):
	# Initial track with the given note
	t = Track()
	t + note_given
	t.bars[0].place_rest(2)

	# Export initial score
	export_score(t, dictee_number, "score_default")

	# Add random notes within the constraint of max interval
	for i in range(nb_notes):
		previous_note = int(t.bars[-1][0][2][0]) if (i==0) else int(t.bars[-1][-1][2][0])
		interval_random = random.randint(max(-interval_max, note_min-previous_note), min(interval_max, note_max-previous_note))
		result_note = previous_note + interval_random
		t + Note(result_note)

	# Export score & audio
	export_score(t, dictee_number, "score")
	export_wav(t)
	
	# Create the movie
	export_movie()
	
