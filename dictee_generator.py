
from mingus.midi import *
from mingus.containers import *

from mingus.midi import *
from mingus.extra import *

import random
import subprocess
import time

SCORE_TEMPLATE = """\\header {
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

########################

note_min = int(Note("A-3"))
note_max = int(Note("A-5"))
interval_max = 12
nb_notes = 15
note_donnee = "A-4"

#######################

i = Instrument()
i.name = "Test"

t = Track(i)

t + note_donnee
t.bars[0].place_rest(2)
print(int(t.bars[-1][0][2][0]))

for i in range(nb_notes):
	previous_note = int(t.bars[-1][0][2][0]) if (i==0) else int(t.bars[-1][-1][2][0])
	interval_random = random.randint(max(-interval_max, note_min-previous_note), min(interval_max, note_max-previous_note))
	result_note = previous_note + interval_random
	t + Note(result_note)

print(t)
midi_file_out.write_Track("test.mid", t, bpm=50)

t_lily = lilypond.from_Track(t)
number = 1

lilypond.to_pdf(SCORE_TEMPLATE % (t_lily, number), "test_track.pdf")


subprocess.call(['fluidsynth', '-F', 'output.wav', '/home/lemezoth/Downloads/Nice-Steinway-v3.8.sf2', 'test.mid'],
	stdout=subprocess.PIPE,
	universal_newlines=True)

subprocess.call(['rm', 'test.mid'],
	stdout=subprocess.PIPE,
	universal_newlines=True)
