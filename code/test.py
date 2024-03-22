"""
Module qui permet de lancer des tests pour verifier que votre implementation est conforme

========================== ATTENTION ==========================
            VOUS NE DEVEZ PAS MODIFIER CE FICHIER
===============================================================
"""
import sys
import pickle as pk
import time

from track import Track
from kart import Kart

ERROR_STRING = "\n========================== ECHEC DU TEST ===========================\n"
SUCCESS_STRING = "\n===================== VOTRE CODE A PASSE LE TEST ======================\n"
MARGIN = 50


class SequencePlayer():
    """
    Classe qui sert a jouer une sequence de mouvements predefinis
    """

    def __init__(self, sequence):
        self.sequence = sequence
        self.time = 0
        self.kart = None

    def wrap_move(self, string):
        start = time.time()
        move = self.move(string)
        end = time.time()
        print(end-start)
        return move

    def move(self, string):

        global final_time
        assert self.time <= final_time + MARGIN, ERROR_STRING + \
            "Le kart n'a pas fini le circuit dans le temps imparti, il faut revoir votre implementation"

        if self.time >= len(self.sequence):
            command = self.sequence[-1]
        else:
            command = self.sequence[self.time]
        self.time += 1
        return command


test_names = [
    'un_checkpoint',
    'plusieurs_checkpoints',
    'grass',
    'boost',
    'lava'
]

assert len(sys.argv) > 1, "Vous devez specifier un nom de test. Par exemple: python test.py un_checkpoint"
test_name = sys.argv[1]

assert test_name in test_names, "Le test " + test_name + " n'est pas defini."

# Chargement du circuit et de la trajectoire du kart
test_string, initial_position, initial_angle, test_sequence, final_time = pk.load(
    open('test/' + test_name + '.pk', 'rb'))

# Instanciation du circuit
controller = SequencePlayer(test_sequence)
kart = Kart(controller)
controller.kart = kart
track = Track(test_string, initial_position, initial_angle)
track.add_kart(kart)

# Simulation de la sequence predefinie sur le circuit
compteur = track.play()

# On regarde si le kart a bien termine avec le bon nombre d'etapes
assert compteur >= final_time - MARGIN, ERROR_STRING + \
    "Le kart a fini le circuit trop rapidement, il faut revoir votre implementation"

print(SUCCESS_STRING)
