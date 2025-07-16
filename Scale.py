from Notation import Notation
from Note import Note
import random

##############################################################################################################
#### Clase que contiene una escala y subescalas en función de las notas diferentes que tengan entre ellas ####
##############################################################################################################
class Scale:
    def __init__(self, name, grades, cromatism=-1):
        self.name = name
        # Contiene los grados de la escala como enteros
        self.grades = grades
        # Número de notas diferentes que se permiten para ser considerada subescala
        self.cromatism = cromatism
        self.subscales = []

    ###########################################################################
    #### Comprueba el número de notas diferentes de una escala con tónicas ####
    ###########################################################################
    def check_scale(self, scale, tonic1, tonic2):
        scale1 = self.to_notes(tonic1)
        scale2 = scale.to_notes(tonic2.notation)
        cromatism = len(set(scale1) - set(scale2))
        return cromatism
    
    def add_subscale(self, scale):
        self.subscales.append(scale)

    ########################################################################
    #### Devuelve las notas que tiene esa escala a partir de una tónica ####
    ########################################################################
    def to_notes(self, tonic):
        notes = []
        for g in self.grades:
            note = g + tonic.value
            if note > 11:
                note -= 12
            notes.append(Notation(note))
        return notes
    
    def get_size(self):
        return len(self.grades)
    
    def change_to_subscale(self, notes, tonic):
        for n in notes:
            if n is not None:
                for s in self.subscales:
                    if s.contains(notes, n) and self.check_scale(s, tonic, n) <= 1:
                        for s2 in list(self.subscales):
                            s.add_subscale(s2)
                        s.add_subscale(self)
                        return s, n.notation
        return self, tonic
            

    def contains(self, notes, tonic):
        scale = self.to_notes(tonic.notation)
        for n in notes:
            if n is not None:
                if n.notation not in scale:
                    return False
        return True
    
    ##############################################################################################
    #### Devuelve el grado de una nota en concreto a partir de una tónica y esa nota concreta ####
    ##############################################################################################
    def get_grade_from_tonic(self, tonic, note):
        notes = self.to_notes(tonic)
        for i, n in enumerate(notes):
            if n.value == note:
                return i
    
    ###################################################################################################################################
    #### Devuelve las notas que pertenecen a la escala desde una nota a otra, a partir de una tónica, y una nota de comienzo y fin ####
    ###################################################################################################################################
    def ascend_scale(self, tonic, start, end):
        scale_notation = self.to_notes(tonic)
        if start.notation not in scale_notation or end.notation not in scale_notation:
            return []
        flag = True
        notes = []
        octave = start.octave
        # Si es la última nota de la escala se suma una octava y se convierte a la primera nota
        if start.notation.value == 11:
            notation = Notation(0)
            octave += 1
        else:
            notation = Notation(start.notation.value + 1)
        while flag:
            # Este bucle recorre las notas que no pertenecen a la escala
            while notation not in scale_notation:
                if notation.value == 11:
                    notation = Notation(0)
                    octave += 1
                else:
                    notation = Notation(notation.value + 1)
            # Cuando detecta la nota de fin
            if notation.value == end.notation.value and octave == end.octave:
                flag = False
                break
            # Se incluye la nota
            notes.append(Note(notation, octave))
            if notation.value == 11:
                notation = Notation(0)
                octave += 1
            else:
                notation = Notation(notation.value + 1)
        return notes
    
    ###################################################
    #### Igual que la anterior pero para descender ####
    ###################################################
    def descend_scale(self, tonic, start, end):
        scale_notation = self.to_notes(tonic)
        if start.notation not in scale_notation or end.notation not in scale_notation:
            return []
        flag = True
        notes = []
        octave = start.octave
        # Si es la primera nota de la escala se resta una octava y se inicia por la del final
        if start.notation.value == 0:
            notation = Notation(11)
            octave -= 1
        else:
            notation = Notation(start.notation.value - 1)
        while flag:
            while notation not in scale_notation:
                if notation.value == 0:
                    notation = Notation(11)
                    octave -= 1
                else:
                    notation = Notation(notation.value - 1)
            if notation.value == end.notation.value and octave == end.octave:
                flag = False
                break
            notes.append(Note(notation, octave))
            if notation.value == 0:
                notation = Notation(11)
                octave -= 1
            else:
                notation = Notation(notation.value - 1)
        return notes
    
    def __str__(self):
        return str(self.name + ": ") + str(self.grades)

####################################################################
#### Lee las escalas de un archivo con el formato de scales.txt ####
####################################################################
def read_scales(filename):
    with open(filename, 'r') as f:
        scales = []
        for line in f:
            parts = line.strip().split(maxsplit=1)
            name = parts[0]
            numbers = list(map(int, parts[1].split('|'))) if len(parts) > 1 else []
            scales.append(Scale(name, numbers))
        return scales
    
def part_scales(filename):
    scales = read_scales(filename)
    ind = random.randint(0, len(scales) - 1)
    scale = scales[ind]
    for i, s in enumerate(scales):
        if i != ind:
            scale.add_subscale(s)
    return scale

scales = read_scales("scales.txt")

scale = scales[0]

for n in scale.ascend_scale(Notation.C, Note(Notation.F, 4), Note(Notation.F, 5)):
    print(str(n) + ", ")
