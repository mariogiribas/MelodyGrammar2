import Scale
import Note
import Notation
import random

############################################################################################
#### Clase que contiene la melodía en función de una tónica y una escala como tonalidad ####
############################################################################################
class Melody():
    def __init__(self, tone, tonic):
        self.flag = False
        self.tone = tone
        self.tonic = tonic
        self.notes = []
        self.prev_notes = [None, None, None]
        self.octave = 0.01
        self.ascend = 0.5
        self.scale_change = 0.05

    ##########################################################
    #### Genera la melodía devolviendo una lista de notas ####
    ##########################################################
    def generate(self, min, max, from_scratch, submelody):
        # Establece la duración de la melodía de forma aleatoria entre dos valores límite
        octave1 = None
        duration = random.randint(min, max)
        i = 0
        # Pobla las probabilidades iniciales
        self.calculate_probabilities()
        if from_scratch:
            if submelody:
                if self.prev_notes[1] is not None:
                    octave1 = self.prev_notes[1].octave
                elif self.prev_notes[0] is not None:
                    octave1 = self.prev_notes[0].octave
                elif self.prev_notes[2] is not None:
                    octave1 = self.prev_notes[2].octave
            self.prev_notes = [None, None, None]

        # Bucle que seguirá hasta que la melodía tenga la duración establecida
        while len(self.notes) < duration:
            # El flag se utiliza para reiniciar el contador a 0 ya que se inserta entre notas y no siempre al final
            # Se insertará en notes[i] siempre, i se incrementa de 2 en 2
            if self.flag:
                self.flag = False
                i = 0
            inserted = 0
            change_scale = False
            # Para el caso inicial (está dentro del bucle ya que se permite que no sea siempre así el inicial)
            # Generará siempre 3 notas con las probabilidades iniciales
            if self.prev_notes[0] is None and self.prev_notes[1] is None and self.prev_notes[2] is None:
                note = self.tone.to_notes(self.tonic)[self.note_probabilities.get_value()]
                if octave1 is None:
                    self.notes.append(Note.Note(note, self.get_octave(note)))
                else:
                    self.notes.append(Note.Note(note, octave1))
                if len(self.notes) == duration:
                    return self.notes
                self.prev_notes[0] = self.notes[0]
                note = self.tone.to_notes(self.tonic)[self.note_probabilities.get_value()]
                self.notes.append(Note.Note(note, self.get_octave(note)))
                if len(self.notes) == duration:
                    return self.notes
                self.prev_notes[1] = self.notes[1]
                note = self.tone.to_notes(self.tonic)[self.note_probabilities.get_value()]
                self.notes.append(Note.Note(note, self.get_octave(note)))
                if len(self.notes) == duration:
                    return self.notes
                self.prev_notes[2] = self.notes[2]
            # Caso de inserción para insertar la nota en la primera, es decir, sin anteriores
            if i == 0:
                self.prev_notes[0] = None
                self.prev_notes[1] = None
                self.prev_notes[2] = self.notes[i]
            # Caso de inserción para insertar la nota en la segunda, es decir, solo con una anterior
            elif i == 1:
                self.prev_notes[0] = None
                self.prev_notes[1] = self.notes[i - 1]
                self.prev_notes[2] = self.notes[i]
            # Caso de inserción para insertar la nota en la última, es decir, sin posteriores
            # En este caso se reinicia el contador i
            elif i > (len(self.notes) - 1):
                self.prev_notes[0] = self.notes[len(self.notes) - 2]
                self.prev_notes[1] = self.notes[len(self.notes) - 1]
                self.prev_notes[2] = None
                self.flag = True
            # Caso de inserción normal, considerando todas las notas previas y posteriores
            else:
                self.prev_notes[0] = self.notes[i - 2]
                self.prev_notes[1] = self.notes[i - 1]
                self.prev_notes[2] = self.notes[i]
            change_scale = random.random() < self.scale_change
            if change_scale:
                subtone = self.tone.change_to_subscale(self.prev_notes, self.tonic)
                submelody = Melody(subtone[0], subtone[1])
                submelody.set_prev_notes(self.prev_notes)
                subnotes = submelody.generate(1, duration - len(self.notes), True, True)
                for j, sn in enumerate(subnotes):
                    self.notes.insert(i + j, sn)
                    inserted += 1
                self.scale_change = 0.05
            else:
                # Se calculan las probabilidades teniendo en cuenta las notas previas y posteriores (prev_notes[])
                self.calculate_probabilities()
                # Se obtiene la nota a partir de las probabilidades, y su octava, y se inserta
                note = self.tone.to_notes(self.tonic)[self.note_probabilities.get_value()]
                self.notes.insert(i, Note.Note(note, self.get_octave(note)))
                self.scale_change *= 1.25
            i += ((2 + inserted) // 2) * 2
        return self.notes
    
    def set_prev_notes(self, notes):
        self.prev_notes[0] = notes[0]
        self.prev_notes[1] = notes[1]
        self.prev_notes[2] = notes[2]

    ##############################################################################################################################
    #### Calcula las probabilidades de cada grado de la escala teniendo en cuenta la tónica y las notas previas y posteriores ####
    ##############################################################################################################################
    def calculate_probabilities(self):
        self.note_probabilities = Probabilities(self.tone.get_size())
        # Se da prioridad a los grados I, II, III y IV
        self.note_probabilities.update(0, 1.5)
        self.note_probabilities.update(1, 1.25)
        self.note_probabilities.update(2, 1.25)
        self.note_probabilities.update(3, 1.25)
        self.note_probabilities.update(4, 1.25)
        # En caso de que no tenga nota anterior, se da prioridad a los grados I, II y III
        if self.prev_notes[1] is None:
            self.note_probabilities.update(0, 2)
            self.note_probabilities.update(1, 1.5)
            self.note_probabilities.update(2, 1.5)
        # Si no tiene nota preanterior (pero si anterior), se da prioridad a los grados I, II y III
        # y se baja la posibilidad de repetirse la anterior
        elif self.prev_notes[0] is None:
            self.note_probabilities.update(0, 2)
            self.note_probabilities.update(1, 1.5)
            self.note_probabilities.update(2, 1.5)
            self.note_probabilities.update(self.tone.get_grade_from_tonic(self.tonic, self.prev_notes[1].notation.value), 0.5)
        # Si existen todas las anteriores, se baja la posibilidad de repetir la nota preanterior
        else:
            self.note_probabilities.update(self.tone.get_grade_from_tonic(self.tonic, self.prev_notes[0].notation.value), 0.75)
        # Si existen tanto la nota anterior como la posterior, se sube la posibilidad de las notas que están entre medias de esas dos
        if self.prev_notes[1] is not None and self.prev_notes[2] is not None:
            dist = self.prev_notes[1].get_distance(self.prev_notes[2])
            notes = []
            if dist < 0:
                notes = self.tone.descend_scale(self.tonic, self.prev_notes[1], self.prev_notes[2])
            elif dist > 0:
                notes = self.tone.ascend_scale(self.tonic, self.prev_notes[1], self.prev_notes[2])
            for n in notes:
                self.note_probabilities.update(self.tone.get_grade_from_tonic(self.tonic, n.notation.value), 2)

    ###################################################################################################
    #### Calcula la octava de la nota a generar teniendo en cuenta las notas previas y posteriores ####
    ###################################################################################################
    def get_octave(self, note):
        # Se aumenta la posibilidad de que se suba o baje una octava
        self.octave *= 1.05
        # Se prueba esa posibilidad
        octave = random.random() < self.octave
        # Si se cumple, se elige al azar si baja o sube y se reinicia la posibilidad
        if octave:
            self.octave = 0.01
            oct_val = random.choice([-1, 1])
        else:
            oct_val = 0
        # Si no existen notas anteriores ni posteriores se devuelve una octava aleatoria (2, 3, 4 o 5)
        # Si existe la nota posterior pero no la anterior se devuelve la octava de la posterior
        if self.prev_notes[1] is None:
            if self.prev_notes[2] is None:
                if self.prev_notes[0] is None:
                    o = random.choice([4, 5, 6])
                    return o
                if self.prev_notes[0].octave + oct_val <= 7 or self.prev_notes[0].get_ascend(note) + oct_val > 0:
                    return self.prev_notes[0].octave + oct_val
                else:
                    return self.prev_notes[0].octave
            if self.prev_notes[2].octave + oct_val <= 7 or self.prev_notes[2].get_ascend(note) + oct_val > 0:
                return self.prev_notes[2].octave + oct_val
            else:
                return self.prev_notes[2].octave
        # Se elige al azar en función de la varible ascend si asciende o desciende
        # La posibilidad de que ascienda se baja cada vez que asciende, y se sube si desciende
        # Se devuelve la octava de descender o ascender sobre la nota anterior
        elif random.random() < self.ascend:
            self.ascend *= 0.9
            return self.prev_notes[1].get_ascend(note) + oct_val
        else:
            self.ascend *= 1.1
            return self.prev_notes[1].get_descend(note) + oct_val


##################################################################################################################################
#### Esta clase permite guardar las notas de una escala con sus probabilidades guardando los grados como índices en una lista ####
##################################################################################################################################
class Probabilities:
    # Se inicializa con un tamaño
    def __init__(self, n):
        self.values = [1/n] * n
        self.size = n

    # Actualiza un valor sobre un factor y lo normaliza con el resto de valores
    def update(self, index, factor):
        if index is None:
            return
        self.values[index] *= factor
        total = sum(self.values)
        self.values = [p / total for p in self.values]

    def get(self):
        return tuple(self.values)
    
    def set(self, value, index):
        self.values[index] = value
    
    def setAll(self, value):
        self.values = [value] * self.size
    
    # Extrae un valor aleatorio aplicando las probabilidades
    def get_value(self):
        elements = list(range(self.size))
        return random.choices(elements, weights=self.values, k=1)[0]
    def get_values(self, n):
        pass
    def __str__(self):
        ret = ""
        for i, n in enumerate(self.values):  
            ret += str(i) + ": " + str(n) + '\n'
        return ret
