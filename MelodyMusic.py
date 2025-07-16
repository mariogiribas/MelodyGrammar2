import Melody
import Notation
import Scale
import fluidsynth
import time

# Inicializa el generador de melodía
m = Melody.Melody(Scale.part_scales("scales.txt"), Notation.Notation.C)
notes = m.generate(15, 35, True, False)

# Inicializa Fluidsynth
fs = fluidsynth.Synth()
fs.start(driver="pulseaudio")  # Usa "alsa" en Linux o "coreaudio" en macOS
sfid = fs.sfload("FluidR3_GM.sf2")  # Asegúrate de que esta ruta es correcta
fs.program_select(0, sfid, 0, 0)  # Canal 0, banco 0, preset 0 (acústico piano)

# Convierte tu nota a nota MIDI y reproduce
for note in notes:
    midi_note = note.notation.value + 12 * (note.octave + 1)
    fs.noteon(0, midi_note, 100)  # 100 es la velocidad (volumen)
    time.sleep(0.5)
    fs.noteoff(0, midi_note)

fs.delete()