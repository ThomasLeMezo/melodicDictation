
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
#(set-default-paper-size "a6landscape" )
\\header {
    tagline = ""
    title = "Interval %i"
  }
\\score{
  {
  \\omit Score.BarLine
  \\override Score.SpacingSpanner.shortest-duration-space = #5.0
  \\mark "%s"
  {%s-\\bendAfter #%s5  s4}
  }
  \\layout {
  \\context {
    \\Staff
      \\remove "Clef_engraver"
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

def export_score(track, dictee_number, interval_name, sens, file_name="track"):
  t_lily = lilypond.from_Track(track)
  t_lily_output = SCORE_TEMPLATE % (dictee_number, interval_name, t_lily[t_lily.find("{", 2)+1:t_lily.find("}")][1:-1], sens)
  t_lily_output = t_lily_output.replace('r4', 's4')
  lilypond.to_pdf(t_lily_output, file_name+".pdf")
  subprocess.call(['pdftoppm', '-png', '-r', '300', '-singlefile', file_name+'.pdf', file_name],
  stdout=subprocess.PIPE)
  os.remove(file_name+'.pdf')

def export_movie(dictee_number=0):
  file_name_movie = 'output/'+'interval%s.mp4'%(dictee_number)
  print("export movie", file_name_movie)

  subprocess.call(['ffmpeg', '-framerate', '0.5' ,'-pattern_type', 'glob', '-i', './interval/score_interval*.png', '-vcodec', 'libx264', '-crf', '25', file_name_movie])

  # Remove files
  #os.remove('./interval/*.png')

tab_interval = ["seconde", "tierce", "quarte", "quinte", "sixte", "septième"]

################################################
#export_movie()
for dictee_number in range(nb_generate):
  # Initial track with the given note
  
  # Add random notes within the constraint of max interval
  for i in range(nb_notes):
    t = Track()
    t + Note(random.randint(note_min, note_max))

    sens = "" if bool(random.getrandbits(1)) else "-"
    interval_name = tab_interval[random.randint(0, len(tab_interval)-1)]
    
    export_score(t, dictee_number, interval_name , sens, "./interval/score_interval_"+str(i).zfill(2))

  export_movie(dictee_number)
  
