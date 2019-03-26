# -*- coding: utf-8 -*-
from test import *
import random

#### REPRESENTATION DES DONNEES

def grille_debut_partie():
    """Construit une liste de debut de partie"""
    grille = [
        ['X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X'],
        ['O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O']
    ]
    return grille


def grille_milieu_partie():
    """Construit une liste de milieu de partie"""
    grille = [
        [' ', ' ', ' ', ' '],
        ['X', ' ', ' ', 'X'],
        [' ', ' ', ' ', 'X'],
        ['O', 'O', 'X', 'O']
    ]
    return grille


def grille_fin_partie():
    """Construit une liste de fin de partie"""
    grille = [
        ['X', ' ', ' ', 'X'],
        ['X', ' ', 'X', 'O'],
        ['O', ' ', ' ', 'X'],
        [' ', ' ', ' ', 'X']
    ]
    return grille

# la grille du jeu
grille = grille_debut_partie()
joueur_en_cours = 0


#### SAISIE

def est_dans_grille(x, y, grille):
    """Verifier qu'un couple de coordonnees est dans la grille"""
    if 0 <= x < len(grille[0]) and 0 <= y < len(grille):
        return True
    else:
        return False


def convertir_lettre_index(lettre):
    """Convertir une lettre en l'index correspondant"""

    lettres = "ABCD"
    for i in range(4):
        if lettres[i] == lettre:
            return i

    # erreur de coordonnees (-1 n'est jamais valide)
    # la lettre n'est pas dans A,B,C,D
    return -1


def analyser_action(action):
    """Renvoyer un tuple de coordonnees a partir d'une chaine"""

    if len(action) >= 2 and action[1] in "1234" and action[0] in "ABCD":
        # convertir les coordonnees en entiers
        y = convertir_lettre_index(action[0])
        x = int(action[1]) - 1
        # renvoyer les coordonnees
        return (x, y)
    else:
        # renvoyer une erreur (les coordonnees negatives ne sont jamais valides)
        # - soit car la taille de la saisie est trop petite
        # - soit car la deuxieme composante n'est pas un chiffre
        return (-1, -1)


def saisir_coordonnees(grille):
    """Demander la saisie de coordonnees"""

    message = 'Choississez une position dans la grille. [ Par exemple : A1 ou B3 ... ]'
    print(message)
    x, y = analyser_action(input('> '))

    while not est_dans_grille(x, y, grille):
        print('Veuillez choisir des cordonnees valides...')
        print(message)
        x, y = analyser_action(input('> '))

    return (x, y)

#### deplacement

def pion(joueur):
    if joueur == 0:
        return 'X'
    else:
        return 'O'

def pion_complementaire(joueur):
    if joueur == 0:
        return 'O'
    else:
        return 'X'


def direction(depart_x, depart_y, arrive_x, arrive_y):
    # la distance horizontal est abs(distance_x)
    # la direction horizontal est le signe de distance_x
    distance_x = arrive_x - depart_x
    # la distance vertical est abs(distance_y)
    # la direction vertical est le signe de distance_y
    distance_y = arrive_y - depart_y
    return (distance_x, distance_y)


def est_capture(depart_x, depart_y, arrive_x, arrive_y, joueur, grille):
    depart_ok = pion(joueur) == grille[depart_y][depart_x]
    arrive_ok = pion_complementaire(joueur) == grille[arrive_y][arrive_x]

    distance_x, distance_y = direction(depart_x, depart_y, arrive_x, arrive_y)
    
    distance_ok = (abs(distance_x) == 2 or abs(distance_y) == 2)
    direction_ok = (distance_x == 0 or distance_y == 0)

    saut_ok = False
    if abs(distance_x) == 2 and grille[depart_y][depart_x+distance_x//2] == pion(joueur):
        saut_ok = True
    elif abs(distance_y) == 2 and grille[depart_y+distance_y//2][depart_x] == pion(joueur):
        saut_ok = True

    capture_ok = distance_ok and direction_ok and depart_ok and arrive_ok and saut_ok

    return capture_ok


def effectuer_capture(depart_x, depart_y, arrive_x, arrive_y, joueur, grille):
    # la case de depart est maintenant vide
    grille[depart_y][depart_x] = ' '
    # le joueur prend la place en "arrive_x, arrive_y"
    # capturant ainsi un pion adverse
    grille[arrive_y][arrive_x] = pion(joueur)


def effectuer_deplacement_simple(depart_x, depart_y, arrive_x, arrive_y, joueur, grille):
    grille[depart_y][depart_x] = ' '
    grille[arrive_y][arrive_x] = pion(joueur)


def est_deplacement_simple(depart_x, depart_y, arrive_x, arrive_y, joueur, grille):
    depart_ok = pion(joueur) == grille[depart_y][depart_x]
    arrive_ok = grille[arrive_y][arrive_x] == ' '

    distance_x = abs(depart_x - arrive_x)
    distance_y = abs(depart_y - arrive_y)

    distance_ok = (distance_x == 1 or distance_y == 1)
    orthogonal_ok = (distance_x == 0 or distance_y == 0)

    deplacement_ok = depart_ok and arrive_ok and distance_ok and orthogonal_ok

    return deplacement_ok


def deplacement_capture(depart_x, depart_y, arrive_x, arrive_y, joueur, grille):
    if est_capture(depart_x, depart_y, arrive_x, arrive_y, joueur, grille):
        # la capture est possible, donc on l'effectue
        effectuer_capture(depart_x, depart_y, arrive_x, arrive_y, joueur, grille)
        # on a bien effectue la capture
        return True
    # la capture est impossible
    return False


def deplacement_simple(depart_x, depart_y, arrive_x, arrive_y, joueur, grille):
    if est_deplacement_simple(depart_x, depart_y, arrive_x, arrive_y, joueur, grille):
        # le deplacement est possible, donc on l'effectue
        effectuer_deplacement_simple(depart_x, depart_y, arrive_x, arrive_y, joueur, grille)
        # on a bien effectue le deplacement
        return True
    # le deplacement est impossible
    return False

#### fin de partie

def est_bloque(grille, x, y):
    # nombre de voisins ennemis@
    voisins_ennemis = 0
    # pion de l'adversaire
    pion_courrant = grille[y][x]
    pion_adv = 'X'
    if pion_courrant == 'X':
        pion_adv = 'O'

    if y-1 < 0 or (y-1 >= 0 and grille[y-1][x] == pion_adv):
        # je suis bloque par le haut
        voisins_ennemis += 1
    if y+1 > 3 or (y+1 < 4 and grille[y+1][x] == pion_adv):
        # je suis bloque par le bas
        voisins_ennemis += 1
    if x-1 < 0 or (x-1 >= 0 and grille[y][x-1] == pion_adv):
        # je suis bloque par la gauche
        voisins_ennemis += 1
    if x+1 > 3 or (x+1 < 4 and grille[y][x+1] == pion_adv):
        # je suis bloque par la droite
        voisins_ennemis += 1

    # je suis bloque par les 4 cotes
    return voisins_ennemis == 4


def compter_nombre_pions(grille):
    nombre_joueur0 = 0
    nombre_joueur1 = 0
    for lignes in grille:
        for pions in lignes:
            if pions == pion(0):
                nombre_joueur0 += 1
            elif pions == pion(1):
                nombre_joueur1 += 1
    return (nombre_joueur0, nombre_joueur1)


def compter_pions_bloques(grille):
    nbr_bloque_joueur0 = 0
    nbr_bloque_joueur1 = 0

    for i in range(4):
        for j in range(4):
            if grille[j][i] == pion(0) and est_bloque(grille, i, j):
                nbr_bloque_joueur0 += 1
            elif grille[j][i] == pion(1) and est_bloque(grille, i, j):
                nbr_bloque_joueur1 += 1

    return (nbr_bloque_joueur0 ,nbr_bloque_joueur1)


def fin_partie(grille):
    nbr_pions0, nbr_pions1 = compter_nombre_pions(grille)
    nbr_bloque0, nbr_bloque1 = compter_pions_bloques(grille)

    if nbr_pions0 < 2 or nbr_bloque0 == nbr_pions0:
        # print("joueur " + pion(1) + " gagne")
        return True
    elif nbr_pions1 < 2 or nbr_bloque1 == nbr_pions1:
        # print("joueur " + pion(0) + " gagne")
        return True

    return False

#### tour de jeu

def saisir_deplacement():
    print('Quel est votye type de deplacement ?')
    print('[0] deplacement simple, [1] capture')
    dep = input('> ')
    while dep not in ("0", "1"):
        print('Choississez un type de deplacement parmis 0 ou 1 !')
        print('[0] deplacement simple, [1] capture')
        dep = input('> ')

    return int(dep)

def choisir_position(grille):
    print('Choississez une position de depart : ')
    x1, y1 = saisir_coordonnees(grille)
    print('Choississez une position d\'arrivee : ')
    x2, y2 = saisir_coordonnees(grille)
    return (x1, y1, x2, y2)


def tour_de_jeu(grille, joueur):
    afficher_grille(grille)
    print("c'est le tour du joueur " + pion(joueur))
    deplacement = saisir_deplacement()
    x1, y1, x2, y2 = choisir_position(grille)

    if deplacement == 1:
        if not deplacement_capture(x1, y1, x2, y2, joueur, grille):
            print('Veuillez choisir une capture valide')
            tour_de_jeu(grille, joueur)
    else:
        if not deplacement_simple(x1, y1, x2, y2, joueur, grille):
            print('Veuillez choisir un deplacement valide')
            tour_de_jeu(grille, joueur)


#### AFFICHAGE

def afficher_grille(grille):
    """Afficher la grille dans la console"""
    
    table = "ABCD"
    
    print("  | 1  2  3  4")
    print("-"*14)
    
    for i in range(len(grille)):
        texte = table[i] + " | "
        for colonnes in grille[i]:
            texte += colonnes + "  "
        print(texte)

    print("")

#### MENU

def choisir_grille():
    print('Choississez une grille :')
    print('[1] debut, [2] milieu, [3] fin')
    type_grille = int(input('> '))

    while type_grille not in (1, 2, 3):
        print('tapez 1, 2 ou 3')
        type_grille = int(input('> '))

    if type_grille == 1:
        grille = grille_debut_partie()
    elif type_grille == 2:
        grille = grille_milieu_partie()
    else:
        grille = grille_fin_partie()

    return grille


def choisir_mode():
    print('Choississez un mode de jeu :')
    print('[0] joueur contre joueur, [1] joueur contre IA')
    saisie = input('> ')
    while saisie not in "01":
        print('Veuillez choisir une valeur parmis 0 ou 1')
        saisie = input('> ')
    return int(saisie)

#### IA

def peut_capturer(x, y, joueur, grille):
    ok = False
    if est_dans_grille(x, y+2, grille):
        ok = est_capture(x, y, x, y+2, joueur, grille)
    elif est_dans_grille(x+2, y, grille):
        ok = est_capture(x, y, x+2, y, joueur, grille)
    elif est_dans_grille(x-2, y, grille):
        ok = est_capture(x, x, x-2, y, joueur, grille)
    elif est_dans_grille(x, y-2, grille):
        ok = est_capture(x, y, x, y-2, joueur, grille)

    return ok

def peut_deplacer(x, y, joueur, grille):
    ok = False
    if est_dans_grille(x, y+2, grille):
        ok = est_deplacement_simple(x, y, x, y+2, joueur, grille)
    elif est_dans_grille(x+2, y, grille):
        ok = est_deplacement_simple(x, y, x+2, y, joueur, grille)
    elif est_dans_grille(x-2, y, grille):
        ok = est_deplacement_simple(x, x, x-2, y, joueur, grille)
    elif est_dans_grille(x, y-2, grille):
        ok = est_deplacement_simple(x, y, x, y-2, joueur, grille)

    return ok


def liste_captures(x, y, joueur, grille):
    liste = []
    if est_dans_grille(x, y+2, grille):
        if est_capture(x, y, x, y+2, joueur, grille):
            liste.append((x, y, x, y+2))
    if est_dans_grille(x+2, y, grille):
        if est_capture(x, y, x+2, y, joueur, grille):
            liste.append((x, y, x+2, y))
    if est_dans_grille(x-2, y, grille):
        if est_capture(x, y, x-2, y, joueur, grille):
            liste.append((x, y, x-2, y))
    if est_dans_grille(x, y-2, grille):
        if est_capture(x, y, x, y-2, joueur, grille):
            liste.append((x, y, x, y-2))
    return liste


def liste_deplacements(x, y, joueur, grille):
    liste = []
    if est_dans_grille(x, y+1, grille):
        if est_deplacement_simple(x, y, x, y+1, joueur, grille):
            liste.append((x, y, x, y+1))
    if est_dans_grille(x+1, y, grille):
        if est_deplacement_simple(x, y, x+1, y, joueur, grille):
            liste.append((x, y, x+1, y))
    if est_dans_grille(x-1, y, grille):
        if est_deplacement_simple(x, y, x-1, y, joueur, grille):
            liste.append((x, y, x-1, y))
    if est_dans_grille(x, y-1, grille):
        if est_deplacement_simple(x, y, x, y-1, joueur, grille):
            liste.append((x, y, x, y-1))
    return liste

def liste_coups_possibles(grille, joueur):
    captures = []
    deplacements = []
    for ligne in range(len(grille)):
        for colonne in range(len(grille[0])):
            if grille[ligne][colonne] == pion(joueur):
                captures += liste_captures(colonne, ligne, joueur, grille)
                deplacements += liste_deplacements(colonne, ligne, joueur, grille)
    return (captures, deplacements)

def tour_ia(grille, joueur):
    coups_possibles = liste_coups_possibles(grille, joueur)
    captures, deplacements = coups_possibles

    if len(captures) > 0:
        choix = random.randint(0, len(captures)-1)
        x1, y1, x2, y2 = captures[choix]
        deplacement_capture(x1, y1, x2, y2, joueur, grille)
    else:
        choix = random.randint(0, len(deplacements)-1)
        x1, y1, x2, y2 = captures[choix]
        deplacement_simple(x1, y1, x2, y2, joueur, grille)


#### Programme principal

# cette ligne permet de separer le code principal des fonction.
# Lorsqu'on va importer les fonctions de main.py
# dans test.py, le programme principal ne sera pas lance 
if __name__ == '__main__':
    # effectuer les tests
    # run_tests()
    grille = choisir_grille()
    afficher_grille(grille)

    print(liste_coups_possibles(grille, 0))

    mode_jeu = choisir_mode()

    while not fin_partie(grille):
        tour_de_jeu(grille, 0)
        if mode_jeu == 1:
            tour_ia(grille, 1)
        else:
            tour_de_jeu(grille, 1)
