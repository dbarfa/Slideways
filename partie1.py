# Old partie 1 for historic purposes 

import os                     #Le module os est utilise pour effacer le terminal apres chaque affichage de la matrice

def boucle_jeu():             ################ boucle_jeu()
    """
    Fonction principale du jeu. Dans cette fonction on fait l'appel a toutes les autres fonctions 
    et on place notre couleur grace a elle.
    Entrée: None
    Sortie: Un jeu Slideways sur une matrice 4x4 sans deplacement de lignes. 
    """
    tour_joueur = 1                     #Le jeu commence avec le joueur 1
    dernier_coup_joue = [None,None]
    game_over = False 
    plateau = creation_plateau()
    afficher(plateau)
    
    while game_over != True:            #verifie que le jeu n'est pas fini
        if tour_joueur == 1:
            ligne,col = entree_clavier(tour_joueur)
            
            while plateau[ligne][col] == 1:                                     #
                print('cette case est deja de votre couleur')                   #
                ligne,col = entree_clavier(tour_joueur)                         # Ces 2 while verifient que les cases ne sont     
            while ligne == dernier_coup_joue[0] and col == dernier_coup_joue[1]:# pas deja occupeset que le coup joue n'est
                print('ce coup a deja ete joue')                                # pas le meme que le precedent
                ligne,col = entree_clavier(tour_joueur)                         #
            
            plateau[ligne][col] = 1
            dernier_coup_joue = [ligne,col]  ###### 
            afficher(plateau)  
            if win(plateau):                                                    # Si le joueur1 a gagne alors on arrete le jeu 
                print('joueur 1 gagnant')
                game_over = True   
            tour_joueur = 2                                                     
           
        elif tour_joueur == 2:                                                  # Similaire au joueur 1
            ligne,col = entree_clavier(tour_joueur)
            
            while plateau[ligne][col] == 2:
                print('cette case est deja de votre couleur')
                ligne,col = entree_clavier(tour_joueur)
            while ligne == dernier_coup_joue[0] and col == dernier_coup_joue[1]:
                print('ce coup a deja ete joue')
                ligne,col = entree_clavier(tour_joueur)

            plateau[ligne][col] = 2
            dernier_coup_joue = [ligne,col]  ###### 
            afficher(plateau) 
            if win(plateau):
                print('joueur 2 gagnant')
                game_over = True       
            tour_joueur = 1

def creation_plateau():
    """
    Crée une matrice 4x4
    Entrée : None
    
    Sortie : plateau = un plateau 4v4 avec des elements int entre 0 et 2 
                                                                            
    """
    plateau = [[0] * 4 for x in range(4)]           
    return plateau

def entree_clavier(tour_joueur):
    """
    Cette fonction permet d'entreer une valeur au clavier et la traduire ex B3 = plateau[2][1] elle permet 
    aussi de detecter les commandes invalides.
    Entrée : tour_joueur = elle montre le tour du joueur a changer la prochaine couleur. 1 c'est le joueur 1 et 2 le joueur 2
    Sortie: ligne = Traduction du 2eme element de l'imput de string en int Ex = B3, la ligne est le 3 donc Ex[1] 
            col   = Traduction du 1er  element de l'imput de string en int EX = B3, la colonne est la lettre B donc Ex[0]
            Ces 2 valeurs vont etre utilisées dans la matrice plateau pour montrer l'emplacement desirer par le joueur
    """
    valeurs_valides = [
    'A1','A2','A3','A4',
    'B1','B2','B3','B4',
    'C1','C2','C3','C4',
    'D1','D2','D3','D4'
    ]
    col = 0    
    if tour_joueur == 1:
        print('')
        valeur = input('joueur 1 > ')  
    elif tour_joueur == 2:
        print('')
        valeur = input('joueur 2 > ')    
    while valeur not in valeurs_valides:        #verifie si la valeur entrée ne se trouve pas dans les valeurs valides
        print('commande invalide')              #si elle ne se trouve pas dans les valeurs valides alors on redemande 
        if tour_joueur == 1:                    #une valeur jusqua ce qu'elle soit valide
            print('')
            valeur=input('joueur 1 > ')
        elif tour_joueur == 2:
            print('')
            valeur=input('joueur 2 > ')
    else:                                       #Si elle se trouve dans les valeurs valides on commence la traduction
        if valeur[0] == 'A':
            col = 0
        elif valeur[0] == 'B':
            col = 1
        elif valeur[0] == 'C':
            col = 2
        elif valeur[0] == 'D':
            col = 3
        else:
            print('commande invalide ')    
        ligne = int(valeur[1])-1                #On convertis la ligne en int
        
        return ligne,col             

def win(plateau):
    """
    La fonction win verifie si un joueur a gagne la partie. 
    Elle verifie si dans le plateau on trouve un nombre consecutif different de 0 quatre fois a la suite de l'autre
    horizontalement, verticalement ou en diagonale.
    Entrée : plateau = un plateau 4v4 avec des elements int entre 0 et 2 
    
    Sortie : True si un joueur as gagne sinon il ne retourne rien
    """
    if (
        plateau[0][0] == plateau[1][0] == plateau[2][0] == plateau[3][0] != 0 or
        plateau[0][1] == plateau[1][1] == plateau[2][1] == plateau[3][1] != 0 or
        plateau[0][2] == plateau[1][2] == plateau[2][2] == plateau[3][2] != 0 or
        plateau[0][3] == plateau[1][3] == plateau[2][3] == plateau[3][3] != 0 or
        plateau[0][0] == plateau[0][1] == plateau[0][2] == plateau[0][3] != 0 or
        plateau[1][0] == plateau[1][1] == plateau[1][2] == plateau[1][3] != 0 or
        plateau[2][0] == plateau[2][1] == plateau[2][2] == plateau[2][3] != 0 or
        plateau[3][0] == plateau[3][1] == plateau[3][2] == plateau[3][3] != 0 or#
        plateau[3][0] == plateau[2][1] == plateau[1][2] == plateau[0][3] != 0 or
        plateau[3][3] == plateau[2][2] == plateau[1][1] == plateau[0][0] != 0   
        ):        
        return True
    
def afficher(plateau):                                       ############## fonction afficher(plateau)
    """
    La fonction afficher affiche un plateau 4x4 avec une 'table des matieres' pour les lignes et colonnes
    en transformant les nombres entiers en characteres : 0 = _
                                                         1 = X
                                                         2 = O
    Entrée : plateau = un plateau 4v4 avec des elements int entre 0 et 2 
    
    Sortie : Un plateau 4x4 avec un index et les valeurs a l'interieur du plateau sont affiches comme caractere
    la matrice n'a pas ete changee
    """
    count_ligne = 0
    lignes_reverse_list = ['4 ','3 ','2 ','1 ']
    os.system('clear' if os.name == 'posix' else 'cls')    #voir documentation du module os et ternary operators           
    plateau=plateau[::-1]                                  #je fais un reverse pour pouvoir afficher les lignes 
    print()                                                #de bas en haut au lieu de haut en bas.
    for i in range(4):
        index_ligne = lignes_reverse_list[count_ligne]
        count_ligne = count_ligne + 1
        print(index_ligne, end= " ")
        for j in range(4):                                 #parcours les lignes et affiche un caractere au lieu d'un nombre
            if plateau[i][j]==0:
                print('_', end = "  ")
            elif plateau[i][j]==1:
                print('X',end = "  ")
            elif plateau[i][j]==2:
                print('O',end = "  ")
        print()
    print("   A  B  C  D")

if __name__ == '__main__':
    boucle_jeu()
