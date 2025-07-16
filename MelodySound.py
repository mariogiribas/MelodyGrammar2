import Melody
import Notation
import Scale
import numpy as np
import sounddevice as sd

# Función que convierte Note en frecuencia (Hz)
def note_to_freq(note):
    # A4 es el punto de referencia (440 Hz)
    semitones_from_a4 = (note.octave - 4) * 12 + (note.notation.value - Notation.Notation.A.value)
    return 440 * (2 ** (semitones_from_a4 / 12))

# Generar onda senoidal para una nota
def generate_tone(freq, duration=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * freq * t)

# Reproducir una secuencia de notas
def play_melody(notes, note_duration=0.5):
    melody = np.concatenate([
        generate_tone(note_to_freq(note), duration=note_duration)
        for note in notes
    ])
    sd.play(melody, samplerate=44100)
    sd.wait()

m = Melody.Melody(Scale.part_scales("scales.txt"), Notation.Notation.C)
notes = m.generate(15, 35, True, False)
for n in notes:
    print(n, end=" ")
print()
play_melody(notes)