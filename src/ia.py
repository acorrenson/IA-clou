# -*- coding: utf-8 -*-
"""
    Main IA File
    @author : <Arthur Correnson> <Tristan Barriere>
"""

from main import *
import time
from multiprocessing import Process
from multiprocessing import Pool
import os

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

MDEP = 4
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
        p = compter_nombre_pions(grille)
        return p[joueur]*1000/8 - p[int(not joueur)]*1000/8
    else:
        if joueur == gagnant(grille):
            return 1000 - depth
        else:
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


def minmax_ab(grille, joueur, A, B, depth=0, mdep=MDEP):
    if fin_partie(grille) or depth >= mdep:
        return value(grille, depth, joueur)
    else:
        if joueur == IA:
            cpc, cpd = liste_coups_possibles(grille, EN)
            for c in cpc:
                cp = copy(grille)
                x1, y1, x2, y2 = c
                assert deplacement_capture(x1, y1, x2, y2, EN, cp)
                B = min(B, minmax_ab(cp, EN, A, B, depth+1, mdep))
                if A >= B:
                    return A
            for c in cpd:
                cp = copy(grille)
                x1, y1, x2, y2 = c
                assert deplacement_simple(x1, y1, x2, y2, EN, cp)
                B = min(B, minmax_ab(cp, EN, A, B, depth+1, mdep))
                if A >= B:
                    return A
            return B
        else:
            cpc, cpd = liste_coups_possibles(grille, IA)
            for c in cpc:
                cp = copy(grille)
                x1, y1, x2, y2 = c
                assert deplacement_capture(x1, y1, x2, y2, IA, cp)
                A = max(A, minmax_ab(cp, IA, A, B, depth+1, mdep))
                if A >= B:
                    return B
            for c in cpd:
                cp = copy(grille)
                x1, y1, x2, y2 = c
                assert deplacement_simple(x1, y1, x2, y2, IA, cp)
                A = max(A, minmax_ab(cp, IA, A, B, depth+1, mdep))
                if A >= B:
                    return B
            return A


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


def job(coup, grille):
    cp = copy(grille)
    x1, y1, x2, y2 = coup
    if not deplacement_capture(x1, y1, x2, y2, IA, cp):
        deplacement_simple(x1, y1, x2, y2, IA, cp)
    score = minmax_ab(cp, IA, -1000, 1000)
    return score


def run_parallel(grille, joueur=IA):
    cpc, cps = liste_coups_possibles(grille, joueur)
    meilleur_coup = None
    meilleur_score = -1000

    debut = time.time()
    
    p = Pool(processes=50)
    
    a = p.starmap(job, zip(cpc, [grille for i in range(len(cpc))]))
    b = p.starmap(job, zip(cps, [grille for i in range(len(cps))]))

    # print('Found the best play : ', get_max(cpc, cps, a, b))
    # print('In ', time.time() - debut, 's with depth', MDEP)
    p.close()
    return get_max(cpc, cps, a, b)


def get_max(cpc, cpd, scpc, scpd):
    if cpc == []:
        return cpd[scpd.index(max(scpd))]
    if cpd == []:
        return cpc[scpc.index(max(scpc))]

    m1 = max(scpc)
    m2 = max(scpd)

    m = max(m1, m2)

    if m == m1:
        return cpc[scpc.index(m)]
    else:
        return cpd[scpd.index(m)]



def tour_ia_minmaxab(grille, joueur, depth=MDEP):
    x1, y1, x2, y2 = run_parallel(grille, joueur)
    
    if not deplacement_capture(x1, y1, x2, y2, joueur, grille):
        deplacement_simple(x1, y1, x2, y2, joueur, grille)

grille = [
    ['O', 'X', ' ', 'O'],
    [' ', 'X', 'X', 'X'],
    [' ', ' ', 'X', ' '],
    [' ', ' ', 'O', ' '],
]

def IAvsIA(n):
    for P in range(0, n):
        grille = grille_debut_partie()
        mode_jeu = 0
        jeu = True
        joueur = EN

        while not fin_partie(grille):
            # os.system('clear')
            # afficher_grille(grille)
            if joueur == IA:
                tour_ia_minmaxab(grille, IA)
                joueur = EN
            else:
                tour_ia(grille, EN)
                joueur = IA

        print('VIctoire :', pion(gagnant(grille)))


def PlvsIA():
    grille = grille_milieu_partie()
    joueur = IA

    while not fin_partie(grille):
        if joueur == IA:
            afficher_grille(grille)
            tour_ia_minmaxab(grille, IA)
            joueur = EN
        else:
            os.system('clear')
            tour_de_jeu(grille, EN)
            joueur = IA

    print('VIctoire :', pion(gagnant(grille)))


def server(n):
    Victoires = 0
    global MDEP
    print("Tests for IA Naive VS IA MinMax ab : ")
    for P in range(0, n):
        grille = grille_debut_partie()
        mode_jeu = 0
        jeu = True
        joueur = EN

        while not fin_partie(grille):
            # os.system('clear')
            # afficher_grille(grille)
            if joueur == IA:
                tour_ia_minmaxab(grille, IA)
                joueur = EN
            else:
                tour_ia(grille, EN)
                joueur = IA

        if pion(gagnant(grille)) == 'X':
            Victoires+=1;

    print("Nombres de Victoires de X en profondeur {m} {v}/{n}".format(m=MDEP, v=Victoires, n=n))

server(10)