from enum import Enum

#########################################################
#### Enumeración que contiene las notas como enteros ####
#########################################################
class Notation(Enum):
    C = 0
    C_sharp = 1
    D = 2
    D_sharp = 3
    E = 4
    F = 5
    F_sharp = 6
    G = 7
    G_sharp = 8
    A = 9
    A_sharp = 10
    B = 11

    def __str__(self):
        return self.name
