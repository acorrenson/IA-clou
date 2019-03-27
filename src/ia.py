# -*- coding: utf-8 -*-
"""
    Main IA File
    @author : <Arthur Correnson> <Tristan Barriere>
"""

from main import *
import time
from multiprocessing import Process
from multiprocessing import Pool


### Utilitaires

def copy(grille):
    """
        Copier une grille.
    """
    new_grille = []
    for l in grille:
        new_grille.append(l[:])
    return new_grille


### MINMAX

MDEP = 6
IA = 0
EN = 1

def value(grille, depth, joueur):
    """
    @brief      Calcul du score de la grille en fonction du joueur en cours
    
    @param      grille  The grille
    @param      depth   The depth
    @param      joueur  The joueur
    
    @return     Le Score
    """
    if not fin_partie(grille):
        j0, j1 = compter_nombre_pions(grille)
        return (j0-j1)
    else:
        if joueur == EN:
            # si le joueur en cours est l'adversaire de l'IA
            # et que la partie est finie, alors l'IA gagne
            return 1000 - depth
        else:
            # si le joueur en cours est l'IA
            # et que la partie est finie, alors l'adversaire gagne
            return -1000 + depth


def Min(grille, depth=0):
    """
    @brief      L'adversaire virtuel de l'IA joue en minimisant les chances
                pour l'IA de gagner
    
    @param      grille  The grille
    @param      depth   The depth
                        
    @return     Le score de la partie
    """

    if depth >= MDEP or fin_partie(grille):
        return value(grille, depth, EN)
    else:
        cap, dep = liste_coups_possibles(grille, EN)
        
        min_val = 1234

        for (x1, x2, y1, y2) in cap:
            copied = copy(grille)
            deplacement_capture(x1, y1, x2, y2, EN, copied)
            m = Max(copied, depth+1)
            if m < min_val:
                min_val = m

        for (x1, x2, y1, y2) in dep:
            copied = copy(grille)
            deplacement_simple(x1, y1, x2, y2, EN, copied)
            m = Max(copied, depth+1)
            if  m < min_val:
                min_val = m

        return min_val


def Max(grille, depth=0):
    """
    @brief      L'IA joue en maximisant ses chances
    
    @param      grille  The grille
    @param      depth   The depth
    
    @return     Score de la partie
    """

    if depth >= MDEP or fin_partie(grille):
        return value(grille, depth, IA)
    else:
        cap, dep = liste_coups_possibles(grille, IA)
        
        max_val = -12345

        for (x1, x2, y1, y2) in cap:
            copied = copy(grille)
            deplacement_capture(x1, y1, x2, y2, IA, copied)
            m = Min(copied, depth+1)
            if m > max_val:
                max_val = m

        for (x1, x2, y1, y2) in dep:
            copied = copy(grille)
            deplacement_simple(x1, y1, x2, y2, IA, copied)
            m = Min(copied, depth+1)
            if  m > max_val:
                max_val = m

        return max_val


def minmax_ab(grille, joueur, A, B, depth=0):
    if fin_partie(grille) or depth >= MDEP:
        return value(grille, depth, joueur)
    else:
        Beta = B
        Alpha = A
        cpc, cpd = liste_coups_possibles(grille, IA)
        if joueur == IA:
            for c in cpc:
                cp = copy(grille)
                x1, y1, x2, y2 = c
                deplacement_capture(x1, y1, x2, y2, IA, cp)
                Alpha = max(Alpha, minmax_ab(cp, EN, Alpha, Beta, depth+1))
                if Alpha >= Beta:
                    return Beta
            for c in cpd:
                cp = copy(grille)
                x1, y1, x2, y2 = c
                deplacement_capture(x1, y1, x2, y2, IA, cp)
                Alpha = max(Alpha, minmax_ab(cp, EN, Alpha, Beta, depth+1))
                if Alpha >= Beta:
                    return Beta
            return Alpha
        else:
            for c in cpc:
                cp = copy(grille)
                x1, y1, x2, y2 = c
                deplacement_simple(x1, y1, x2, y2, IA, cp)
                Beta = min(Alpha, minmax_ab(cp, EN, Alpha, Beta, depth+1))
                if Alpha >= Beta:
                    return Alpha
            for c in cpd:
                cp = copy(grille)
                x1, y1, x2, y2 = c
                deplacement_simple(x1, y1, x2, y2, IA, cp)
                Beta = min(Alpha, minmax_ab(cp, EN, Alpha, Beta, depth+1))
                if Alpha >= Beta:
                    return Alpha
            return Beta


def run():
    grille = grille_debut_partie()
    cpc, cps = liste_coups_possibles(grille, IA)
    meilleur_coup = None
    meilleur_score = 0
    debut = time.time()

    for c in cpc:
        cp = copy(grille)
        x1, y1, x2, y2 = c
        deplacement_capture(x1, y1, x2, y2, IA, cp)

        score =  Min(cp)
        if score > meilleur_score:
            meilleur_score = score
            meilleur_coup = c

    for c in cps:
        cp = copy(grille)
        x1, y1, x2, y2 = c
        deplacement_simple(x1, y1, x2, y2, IA, cp)
        score = Min(cp)
        if score > meilleur_score:
            meilleur_score = score
            meilleur_coup = c
    
    print(meilleur_coup)

    print('Time :')
    print(time.time() - debut)


def job(t):
    coup, grille = t
    cp = copy(grille)
    x1, y1, x2, y2 = coup
    deplacement_capture(x1, y1, x2, y2, IA, cp)
    score = Min(cp)
    return score


def test():
    grille = grille_debut_partie()
    cpc, cps = liste_coups_possibles(grille, IA)
    meilleur_coup = None
    meilleur_score = 0
    debut = time.time()
    
    p = Pool(processes=50)
    
    print(p.map(job, zip(cpc, [grille for i in range(len(cpc))])))
    print(p.map(job, zip(cpc, [grille for i in range(len(cps))])))
    


grille = [
    ['O', 'X', ' ', 'O'],
    ['X', 'X', 'X', 'X'],
    [' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' '],
]


def tour_ia_boost(grille, joueur):
    
    cpc, cps = liste_coups_possibles(grille, IA)
    meilleur_coup = None
    meilleur_score = 0

    for c in cpc:
        cp = copy(grille)
        x1, y1, x2, y2 = c
        deplacement_capture(x1, y1, x2, y2, IA, cp)
        score =  minmax_ab(cp, EN, -1234, 1234)
        if score > meilleur_score:
            meilleur_score = score
            meilleur_coup = c

    for c in cps:
        cp = copy(grille)
        x1, y1, x2, y2 = c
        deplacement_simple(x1, y1, x2, y2, IA, cp)
        score =  minmax_ab(cp, EN, -1234, 1234)
        if score > meilleur_score:
            meilleur_score = score
            meilleur_coup = c

    if meilleur_coup is None:
        if cpc != []:
            meilleur_coup = cpc[0]
        else:
            meilleur_coup = cps[0]

    print(meilleur_coup, meilleur_score)
    
    x1, y1, x2, y2 = meilleur_coup
    if deplacement_capture(x1, y1, x2, y2, IA, grille):
        print('blop')
    else:
        deplacement_simple(x1, y1, x2, y2, IA, grille)

mode_jeu = 1

while not fin_partie(grille):
    if mode_jeu == 1:
        tour_ia_boost(grille, IA)
    else:
        tour_de_jeu(grille, IA)
    tour_de_jeu(grille, EN)