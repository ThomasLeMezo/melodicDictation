
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

# \\override Staff.StaffSymbol.line-count = #2%

SCORE_TEMPLATE = """
#(set-default-paper-size "a6landscape")
\\header {
    tagline = ""
  }
\\score{
  {
  \\new Staff {}
  \\new Staff {%s}
  }
  \\header {
    piece = "Lecture %i"
  }
  \\layout {
    \\context {
      \\Score
        proportionalNotationDuration = #(ly:make-moment 1/8)
      }
    \\context {
      \\Staff
        \\remove "Time_signature_engraver"
        \\remove "Clef_engraver"
        \\remove "Bar_engraver"
    }
  }
}
"""

################################################
# Parameters

note_min = int(Note("A-3"))
note_max = int(Note("A-5"))
interval_max = 12
nb_notes = 14
note_given = "D-4"
nb_generate = 1

################################################
# Export functions

def export_score(track, dictee_number, file_name="track"):
  t_lily = lilypond.from_Track(track)
  t_lily_output = SCORE_TEMPLATE % (t_lily, dictee_number)
  t_lily_output = t_lily_output.replace('r4', 's4')
  lilypond.to_pdf(t_lily_output, file_name+".pdf")
  subprocess.call(['pdftoppm', '-png', '-r', '300', '-singlefile', file_name+'.pdf', file_name],
  stdout=subprocess.PIPE)
  os.remove(file_name+'.pdf')

def export_movie(dictee_number=0):
  file_name_movie = 'output/'+'lecture%s.mp4'%(dictee_number)
  print("export movie", file_name_movie)

  subprocess.call(['ffmpeg', '-framerate', '1' ,'-pattern_type', 'glob', '-i', './lecture/score_interval*.png', '-vcodec', 'libx264', '-crf', '25', file_name_movie])

  # Remove files
  #os.remove('./lecture/*.png')

def add_rest(t):
  if(len(t.bars)==0 or t.bars[-1].is_full()):
    t.add_bar(Bar())
  t.bars[-1].place_rest(4)

################################################
#export_movie()
for dictee_number in range(nb_generate):
  # Initial track with the given note
  
  tab_notes = []
  tab_notes.append(random.randint(note_min, note_max))
  # Add random notes within the constraint of max interval
  for i in range(nb_notes):
    interval_random = random.randint(max(-interval_max, note_min-tab_notes[-1]), min(interval_max, note_max-tab_notes[-1]))
    tab_notes.append(tab_notes[-1] + interval_random)

  for i in range(len(tab_notes)-1):
    t = Track()
    add_rest(t)
    # for j in range(i):
    #   add_rest(t)

    for j in range(0, i+2):
      t + Note(tab_notes[j])

    for j in range(len(tab_notes)-(i+1)):
      add_rest(t)
    
    export_score(t, dictee_number, "./lecture/score_interval_"+str(i).zfill(2))

  export_movie(dictee_number)
  
