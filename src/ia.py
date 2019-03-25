# -*- coding: utf-8 -*-
"""
    Main IA File
    @author : <Arthur Correnson> <Tristan Barriere>
"""

from main import *

### Construction d'arbre

class Node:
    """
    @brief      Class for Node.
    """
    def __init__(self, val):
        self.value = val
        self.children = []

    def get_children(self):
        return self.children

class Leaf:
    """
    @brief      Class for Leaf.
    """
    def __init__(self, val):
        self.value = val

### Utilitaires

def copy(grille):
    """
        Copier une grille.
    """
    new_grille = []
    for l in grille:
        new_grille.append(l[:])
    return new_grille

### Simulation

def simulate(c, joueur, grille, depth=0):
    """
    @brief      Simuler une partie complète à partir d'une grille 
    
    @param      c       Un coup
    @param      joueur  Le joueur
    @param      grille  La grille
    @param      depth   Pronfondeur max
    
    @return     Un arbre representant la partie
    """
    if fin_partie(grille) or depth > 5:
        # cas terminal
        return Leaf(grille)
    else:
        # cas recursif
        # on cree un nouvel arbre
        N = Node(grille)
        # on effectue le premier coup
        if c[0] == 0:
            copied = copy(grille)
            deplacement_capture(c[1], c[2], c[3], c[4], joueur, copied)
        else:
            copied = copy(grille)
            deplacement_simple(c[1], c[2], c[3], c[4], joueur, copied)
        # on calcul recursivement les reponses de l'adversaire
        cpc, cpd = liste_coups_possibles(copied, int(not joueur))
        for (x1, y1, x2, y2) in cpc:
            copied = copy(grille)
            deplacement_capture(x1, y1, x2, y2, int(not joueur), copied)
            N.children.append(simulate((0, x1, y1, x2, y2), int(not joueur), copied, depth+1))
        for (x1, y1, x2, y2) in cpd:
            copied = copy(grille)
            deplacement_capture(x1, y1, x2, y2, int(not joueur), copied)
            N.children.append(simulate((1, x1, y1, x2, y2), int(not joueur), copied, depth+1))

        return N

### Affichage

def pprint(T, i = 0):
    print('step :', i)
    if isinstance(T, Leaf):
        afficher_grille(T.value)
    else:
        afficher_grille(T.value)
        for c in T.get_children():
            pprint(c, i+1)

IA = 0
grille = grille_debut_partie()
N = Node(grille)
cpc, cps = liste_coups_possibles(grille, IA)

N = simulate((0, cpc[0][0], cpc[0][1], cpc[0][2], cpc[0][3]), IA, grille)

pprint(N)

