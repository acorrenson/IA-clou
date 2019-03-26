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
    def __init__(self, val, coup=None):
        self.value = val
        self.children = []
        self.coup = coup
        self.score

    def get_children(self):
        return self.children

class Leaf:
    """
    @brief      Class for Leaf.
    """
    def __init__(self, val, coup=None):
        self.value = val
        self.coup = coup

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

### MINMAX

MDEP = 6
IA = 0
EN = 1

def value(grille, depth, joueur):
    if not fin_partie(grille):
        return 0
    else:
        if joueur == EN:
            return 1000 - depth
        else:
            return -1000 + depth


def Max(coup, grille, depth=0):
    grille = copy(grille)
    if depth >= MDEP or fin_partie(grille):
        return value(grille, depth, EN)
    else:
        type_coup, x1, y1, x2, y2 = coup
        if type_coup == 0:
            if not deplacement_capture(x1, y1, x2, y2, IA, grille):
                raise Exception('err')
        else:
            if not deplacement_simple(x1, y1, x2, y2, IA, grille):
                raise Exception('err')

        coups_possibles = liste_coups_possibles(grille, EN)
        captures, deplacements = coups_possibles

        if coups_possibles == ([], []):
            return value(grille, depth, EN)

        max_val = 0

        for (x1, y1, x2, y2) in captures:
            copied = copy(grille)
            m = Min((0, x1, y1, x2, y2), copied, depth+1)
            if m > max_val:
                max_val = m
        
        for (x1, y1, x2, y2) in deplacements:
            copied = copy(grille)
            m = Min((1, x1, y1, x2, y2), copied, depth+1)
            if m > max_val:
                max_val = m

        return max_val


def Min(coup, grille, depth=0):
    grille = copy(grille)
    if depth >= MDEP or fin_partie(grille):
        return value(grille, depth, IA)
    else:
        type_coup, x1, y1, x2, y2 = coup
        if type_coup == 0:
            if not deplacement_capture(x1, y1, x2, y2, EN, grille):
                raise Exception('err')
        else:
            if not deplacement_simple(x1, y1, x2, y2, EN, grille):
                raise Exception('err')
        
        coups_possibles = liste_coups_possibles(grille, IA)
        captures, deplacements = coups_possibles

        if coups_possibles == ([], []):
            return value(grille, depth, IA)
        
        min_val = 1000

        for (x1, y1, x2, y2) in captures:
            copied = copy(grille)
            m = Max((0, x1, y1, x2, y2), copied, depth+1)
            if m < min_val:
                min_val = m
        
        for (x1, y1, x2, y2) in deplacements:
            copied = copy(grille)
            m = Max((1, x1, y1, x2, y2), copied, depth+1)
            if m < min_val:
                min_val = m

        return min_val

### Affichage

def pprint(T, i = 0):
    print('step :', i)
    if isinstance(T, Leaf):
        afficher_grille(T.value)
    else:
        afficher_grille(T.value)
        for c in T.get_children():
            pprint(c, i+1)

grille = [
    ['O', ' ', 'X', 'O'],
    ['X', 'X', 'X', 'X'],
    [' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' '],
]

cpc, cps = liste_coups_possibles(grille, IA)

for c in cpc: 
    x1, y1, x2, y2 = c
    print(Max((0, x1, y1, x2, y2), grille))

for c in cps:
    x1, y1, x2, y2 = c
    print(Max((1, x1, y1, x2, y2), grille))

