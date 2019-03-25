# -*- coding: utf-8 -*-
from main import *

def test_est_dans_grille():
    grille = grille_debut_partie()
    assert est_dans_grille(0, 0, grille), \
        "Les cordonnees 0 0 appartiennent bien a la grille"
    assert est_dans_grille(-1, 0, grille) == False, \
        "Les cordonnees -1 0 n'appartiennent pas a la grille"
    assert est_dans_grille(2, 2, grille), \
        "Les cordonnees 2 2 appartiennent a la grille"
    assert est_dans_grille(0, 7, grille) == False, \
        "Les cordonnees 0 7 appartiennent pas a la grille"
    assert est_dans_grille(0, -1, grille) == False, \
        "Les cordonnees 0 -1 n'appartiennent pas a la grille"


def test_convertir_lettre_index():
    assert convertir_lettre_index('A') == 0, \
        "La lettre A correspond a l'index 0"
    assert convertir_lettre_index('B') == 1, \
        "La lettre A correspond a l'index 0"
    assert convertir_lettre_index('C') == 2, \
        "La lettre A correspond a l'index 0"
    assert convertir_lettre_index('D') == 3, \
        "La lettre A correspond a l'index 0"
    assert convertir_lettre_index('E') == -1, \
        "La lettre E est invalide"


def test_analyser_action():
    assert analyser_action('A14') == (0, 0), \
        "La saisie A14 est valide mais le 4 n'est pas pris en compte"
    assert analyser_action('A@') == (-1, -1), \
        "La saisie A@ n'est pas valide car @ n'est pas un chiffre"
    assert analyser_action('A1') == (0, 0), \
        "La saisie A1 correspond aux index (0, 0)"
    assert analyser_action('F2') == (-1, -1), \
        "La saisie F2 n'est pas valide [F est en dehors de la grille]"
    assert analyser_action('B2') == (1, 1), \
        "La saisie B2 correspond aux index (1, 1)"


def test_est_capture():
    grille = grille_debut_partie()
    joueur = 0
    assert est_capture(0, 0, 0, 2, 0, grille), \
        "Joueur 0 peut capturer A1 -> C1 en debut de partie"
    assert est_capture(0, 0, 0, 1, 0, grille) == False, \
        "Joueur 0 ne peut pas capturer A1 -> B1 en debut de partie"
    assert est_capture(0, 3, 0, 1, 1, grille), \
        "Joueur 1 peut capturer D1 -> B1 en debut de partie"
    assert est_capture(0, 2, 0, 0, 0, grille) == False, \
        "Joueur 1 ne peut pas capturer D1 -> A1 en debut de partie"


def test_deplacement_capture():
    grille_ref = grille_debut_partie()
    grille = grille_debut_partie()

    # test joueur 0 capture joueur 1
    assert deplacement_capture(0, 0, 0, 2, 0, grille), \
        "La capture du Joueur 0 de A1 en C1 doit etre effectuee"
    assert grille[0][0] == ' ' and grille[2][0] == pion(0), \
        "La capture est bien effectuee"
    
    # test joueur 0 essaye de capturer sans sauter
    grille = grille_debut_partie()
    assert deplacement_capture(0, 0, 0, 1, 0, grille) == False, \
        "La capture du Joueur 0 de A1 en B1 ne doit pas etre effectuee"
    assert grille == grille_ref, \
        "La capture n'est pas effectuee"
    
    # test joueur 1 capture joueur 0
    grille = grille_debut_partie()
    assert deplacement_capture(0, 3, 0, 1, 1, grille), \
        "La capture du Joueur D1 en B1 doit etre effectuee"
    assert grille[3][0] == ' ' and grille[1][0] == pion(1), \
        "La capture est bien effectuee"
    

    # test joueur 0 essaye de capturer sans sauter
    grille = grille_debut_partie()
    assert deplacement_capture(0, 2, 0, 0, 0, grille) == False, \
        "La capture du Joueur 1 de D1 en A1 ne doit pas etre effectuee"
    assert grille == grille_ref, \
        "La capture n'est pas effectuee"

    # test joueur 0 essaye de capturer en diagonale
    grille = grille_debut_partie()
    assert deplacement_capture(0, 2, 0, 3, 0, grille) == False, \
        "Les captures en diagonales ne sont pas permises"
    assert grille == grille_ref, \
        "La capture n'est pas effectuee"

    grille_ref = grille_milieu_partie()
    
    grille = grille_milieu_partie()
    assert deplacement_capture(2, 3, 0, 3, 0, grille) == False, \
        "Le joueur 0 tente de capturer sans saute au dessus d'un allier"
    assert grille == grille_ref, \
        "La capture n'est pas effectuee"


def test_deplacement_simple():
    grille = grille_milieu_partie()
    assert deplacement_simple(3, 1, 3, 3, 0, grille) == False, \
        "Le deplacement du Joueur 0 de B4 en D4 n'est pas un deplacement simple"
    assert deplacement_simple(0, 1, 0, 2, 0, grille), \
        "Le deplacement simple du joueur 0 de A1 en B1 doit etre effectue"
    assert deplacement_simple(0, 1, 3, 1, 0, grille) == False, \
        "Le deplacement simple de 2 cases est interdit"
    assert deplacement_simple(0, 3, 0, 2, 0, grille) == False, \
        "Le joueur 0 ne peut pas deplacer un pion du joueur 1"


def test_est_bloque():
    grille = [
        ['X', ' ', ' ', 'X'],
        ['X', 'O', 'X', 'O'],
        ['O', 'X', 'O', 'X'],
        [' ', 'O', ' ', 'X']
    ]
    assert est_bloque(grille, 3, 1), \
        "Le pion O en B4 est bloque par la bordure droite"
    assert est_bloque(grille, 1, 2), \
        "Le pion X en C2 est bloque par 4 pions O"
    assert est_bloque(grille, 0, 0) == False, \
        "Le pion X en A1 n'est bloque"
    assert est_bloque(grille, 0, 2) == False, \
        "Le pion O en C1 n'est bloque"


def test_compter_nombre_pions():
    grille1 = [
        ['X', ' ', ' ', 'X'],
        ['X', ' ', 'X', 'O'],
        [' ', ' ', ' ', 'X'],
        [' ', ' ', ' ', 'X']
    ]
    grille2 = [
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ']
    ]
    assert compter_nombre_pions(grille1) == (6, 1), \
        "Le joueur X a 6 pions, Le joueur O en a 1"
    assert compter_nombre_pions(grille2) == (0, 0), \
        "Il n'y a aucuns pions sur le plateau"


def test_fin_partie():
    grille1 = [
        ['X', ' ', ' ', 'X'],
        ['X', ' ', 'X', 'O'],
        [' ', ' ', ' ', 'X'],
        [' ', ' ', ' ', 'X']
    ]
    grille2 = grille_debut_partie()
    grille3 = grille_milieu_partie()
    grille4 = [
        ['X', 'X', ' ', 'X'],
        ['X', 'O', 'X', 'O'],
        ['O', 'X', ' ', 'X'],
        ['X', ' ', ' ', 'X']
    ]
    assert fin_partie(grille1), \
        "Joueur O n'a plus qu'un pion la partie s'arrete"
    assert fin_partie(grille4), \
        "Joueur O a 3 pions bloques, la partie s'arrete"
    assert fin_partie(grille2) == False, \
        "La grille de depart ne marque pas la fin de la partie"
    assert fin_partie(grille3) == False, \
        "Cette grille est une grille de milieu de partie"


#### TEST AFFICHAGE ET SAISIE
def run_tests():
    print('TEST AFFICHAGE ET SAISIE :')
    test_est_dans_grille()
    test_analyser_action()
    test_convertir_lettre_index()
    print('FIN TEST AFFICHAGE ET SAISIE !')

    print('TEST ACTION:')
    test_est_capture()
    test_deplacement_capture()
    test_deplacement_simple()
    print('FIN TEST ACTION !')

    print('TEST FIN PARTIE')
    test_est_bloque()
    test_compter_nombre_pions()
    test_fin_partie()
    print('FIN DES TESTs !')
