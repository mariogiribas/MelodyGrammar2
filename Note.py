import Notation

#################################################################################
#### Clase que contiene una nota (la propia nota y la octava en la que está) ####
#################################################################################
class Note():
    def __init__(self, notation, octave):
        self.notation = notation
        self.octave = octave

    # Obtiene la distancia entre dos notas
    def get_distance(self, note):
        dif = (note.octave - self.octave) * 11
        dif -= (self.notation.value - note.notation.value)
        return dif
    
    # Obtiene la octava más cercana ascendiendo de la nota indicada
    def get_ascend(self, note):
        if self.notation.value <= note.value:
            return self.octave
        return self.octave + 1
    
    # Obtiene la octava más cercana descendiendo de la nota indicada
    def get_descend(self, note):
        if self.notation.value >= note.value:
            return self.octave
        return self.octave - 1

    def __str__(self):
        return str(self.notation) + str(self.octave)
    
note1 = Note(Notation.Notation.C, 2)
note2 = Note(Notation.Notation.D, 2)

print(note1.get_distance(note2))
