 # old partie 2

import os
import random

def afficher(plateau,decalage):
    """Affiche le plateau de jeu avec les coups joués par les joueurs et les numéros et lettre pour les lignes et colonnes
    :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
    :param decalage: liste, represente le decalage de chaque ligne
    :return: None
    """
    os.system('clear' if os.name == 'posix' else 'cls')    #supprime les textes du terminal           
    s = '\n\n'
    dic = {
    -3:'{: >12}',
    -2:'{: >15}',
    -1:'{: >18}',
    0:'{: >21}',
    1:'{: >24}',
    2:'{: >27}',
    3:'{: >30}'
    }
    symboles = ['_', 'X', 'O']
    for x in range(3,-1,-1):
        lst_tmp = []
        ligne2 = ''
        #cette partie regroupe les ellements dans une ligne et ajoute les decalages + traduction individuele
        for j in range(0,4):
            lst_tmp.append(plateau[x][j])
        for i in lst_tmp:
            ligne2 += str(symboles[i]) + '  '
        s += str(x+1)+'  ' + dic[decalage[x]].format(ligne2) + '\n\n'
    s += "            A  B  C  D\n\n "
    print(s)

def nouveau_plateau():
    """Crée le plateau de jeu
    :return: liste de liste de dimension 4x4 contenant des 0
    """
    plateau = []
    for _ in range(4):
        plateau.append([0]*4)
    return plateau

def coup(plateau, joueur, dernier_coup,decalage):
    """Demande un coup au joueur jusqu'à ce qu'il soit valide et le joue en modifiant le plateau
    :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
    :param decalage: list d'entiers, représentent le décalage des lignes du plateau
    :param joueur: entier, 1 ou 2
    :param dernier_coup: string de deux caractères, dernier coup joué
    :param decalage: liste, represente le decalage de chaque ligne
    :return c: coup joué qui peut etre utilise comme dernier coup joue
    """
    fini = False
    # demande au joueur d'entrer son coup, vérifie que le coup est correct, et l'effectue
    while not fini:
        if joueur == 1:
            c = input('joueur ' + str(joueur) + ' > ')
        else:
            c = minimax(plateau,decalage,dernier_coup)[0]
            print('joueur ' + str(joueur) + ' > ' + c)
        if len(c) == 2 and c[0] in ['A', 'B', 'C', 'D'] and c[1] in ['1', '2', '3', '4']:


            # si pas dernier coup, déchiffre le coup pour le plateau
            if c[0:2] == dernier_coup: 
                print("ce coup vient d'être joué")
            else:
                i = int(c[1]) - 1
                j = ['A', 'B', 'C', 'D'].index(c[0])
                if plateau[i][j] != joueur:
                    plateau[i][j] = joueur
                    fini = True
                else: 
                    print("cette case est déjà de votre couleur")
                    
        elif len(c) == 2 and c[0] in ['1', '2', '3', '4'] and c[1] in ['-','+']: 
            #teste si le coup entree n'anule pas le decalage precedent
            if c[0:2] == dernier_coup: 
                print("on ne peut pas annuler un decalage au tour suivant, merci de reesayer")
            else:
                #cette partie changent le decalave entree dans l'imput
                if c[1] == '+':
                    if decalage[int(c[0])-1] == 3:
                        print("decalege trop grand merci de reesayer")
                    else:
                        decalage[int(c[0])-1] += 1
                        #change le signe pour le coup precedent
                        if c[1] == '+':
                            c = c.replace('+','-')
                        elif c[1] == '-':
                            c = c.replace('-','+')
                        fini = True
                elif c[1] == '-':
                    if decalage[int(c[0])-1] == -3:
                        print("decalege trop petit merci de reesayer")
                    else:
                        decalage[int(c[0])-1] -= 1
                        if c[1] == '+':
                            c = c.replace('+','-')
                        elif c[1] == '-':
                            c = c.replace('-','+')
                        fini = True
        else:
            print("commande invalide")
    return c[0:2]

def fin_matrice(plateau,decalage):
    """Demande un coup au joueur jusqu'à ce qu'il soit valide et le joue en modifiant le plateau
    :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
    :param decalage: list d'entiers, représentent le décalage des lignes du plateau
    :param joueur: entier, 1 ou 2
    :param dernier_coup: string de deux caractères, dernier coup joué
    :param decalage: liste, represente le decalage de chaque ligne
    :return: coup joué lors du tour precedent
    """
    #deepcopy manuel du plateau
    matrice = [x[:] for x in plateau]
    for i in range(4):
        #ajoutent le decalage pour creer une matrice 4x10
        if decalage[i] == 0:
            for _ in range(3):
                matrice[i].insert(0,0)
                matrice[i].append(0)
        if decalage[i] == -1:
            for _ in range(2):
                matrice[i].insert(0,0)
            for _ in range(4):
                matrice[i].append(0)
        if decalage[i] == -2:
            for _ in range(1):
                matrice[i].insert(0,0)
            for _ in range(5):
                matrice[i].append(0)
        if decalage[i] == -3:
            for _ in range(6):
                matrice[i].append(0)
        if decalage[i] == 1:
            for _ in range(4):
                matrice[i].insert(0,0)
            for _ in range(2):
                matrice[i].append(0)
        if decalage[i] == 2:
            for _ in range(5):
                matrice[i].insert(0,0)
            for _ in range(1):
                matrice[i].append(0)  
        if decalage[i] == 3:
            for _ in range(6):
                matrice[i].insert(0,0) 
    return matrice 

def fin(plateau,decalage):
    """Détermine si quelqu'un a gagné
    :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
    :param decalage: liste, represente le decalage de chaque ligne
    :param joueur: int, represente joueur qui a gagne
    :return: int, 0 si pas de gagnant, sinon le numéro du joueur gagnant ou 3 si egalite
    """
    g=[0]
    matrice = fin_matrice(plateau,decalage)
    #horiz
    #r = row
    #c = column
    for r in range(7):
        for c in range(4):
            if matrice[c][r] == matrice[c][r+1] == matrice[c][r+2] == matrice[c][r+3] != 0:
                g.append(matrice[c][r])
    #vert
    for r in range(10):
        for c in range(1):
            if matrice[c][r] == matrice[c+1][r] == matrice[c+2][r] == matrice[c+3][r] != 0:
                g.append(matrice[c][r])
    #diag
    for r in range(7):
        for c in range(1):
            if matrice[c][r] == matrice[c+1][r+1] == matrice[c+2][r+2] == matrice[c+3][r+3] != 0:
                g.append(matrice[c][r])
    for r in range(6,-1,-1):
        for c in range(1):
            if matrice[c][r] == matrice[c+1][r-1] == matrice[c+2][r-2] == matrice[c+3][r-3] !=0 :
                g.append(matrice[c][r])
    #si g contient 2 elements on n a qu un seul gagnant, si g == 3 egalite else jeu continue
    if len(g) == 2:
        return g[1]
    elif len(g) == 3:
        return 3
    return 0

def trad(ligne,colonne):
    """Traduis les commandes recues de int en string
    :param ligne: int, premier element de la liste
    :param colonne: int, deuxieme element de la liste
    :return (c,l): tuple, 2 string dans un tuple qui representent des coordonees
    
    """
    lignes = {0:'1', 1:'2' , 2:'3', 3:'4'}
    colonnes = {0:'A', 1:'B', 2:'C', 3:'D'}
    l = 0
    c = 0
    #traduis les lignes et les collones en meme temps grace a zip
    for lig,col in zip(lignes,colonnes):
        if lig == ligne:
            l = lignes[lig]
        if col == colonne:
            c = colonnes[col]
    return (c,l)

def coups_possible(plateau,decalage,dernier_coup,joueur):
    """Calcule les coups possible en fonction du plateau et du decalage.
    :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
    :param decalage: liste, represente le decalage de chaque ligne
    :param joueur: int, represente joueur qui a gagne
    :param dernier_coup: string de deux caractères, dernier coup joué
    :param joueur: entier, 1 ou 2
    :return coups_abcd_dec: liste, cette liste recoit les coups possible deca et plateau
    """
    if dernier_coup[0] == 'A':
        col = 0
    elif dernier_coup[0] == 'B':
        col = 1
    elif dernier_coup[0] == 'C':
        col = 2
    elif dernier_coup[0] == 'D':
        col = 3    
    if dernier_coup[1] not in '+-':
        ligne = int(dernier_coup[1])-1                
        dernier_coup=[ligne,col]     
    coups_abcd_dec=[]
    decalage_possible = ['4-','3-','2-','1-','1+','2+','3+','4+']
    #decalage
    for i in decalage_possible:
        if i != dernier_coup and i[1] == '+':
            if decalage[int(i[0])-1] != 3:
                coups_abcd_dec.append(i)
        if i != dernier_coup and i[1] == '-':
            if decalage[int(i[0])-1] != -3:
                coups_abcd_dec.append(i)
    #plateau
    for i in range(4):
        for j in range(4):
            c = [i,j]
            if c != dernier_coup and plateau[i][j] != joueur:
                res = trad(i,j)
                coups_abcd_dec.append(res[0]+res[1])
    return coups_abcd_dec

def minimax(plateau, decalage, dernier_coup, profondeur=2, maxi=True):
    """Fonction recursive, minimax est un algorithme d'inteligence artificiele qui nous permet de jouer avec l'ordinateur
    :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
    :param decalage: liste, represente le decalage de chaque ligne
    :param dernier_coup: string de deux caractères, dernier coup joué
    :param profondeur: int, profondeur represente la profondeur du test de minimax
    :param maxi: bool, si maxi = true then AI else joueur
    :return (choice_final,score_final): un tuple qui represente le coup a jouer et le score de ce coup
    """
    win=fin(plateau,decalage)
    #profondeur 0 ou gagnant alors on stop, condition utilisee seulement pour recursivite
    if win == 1:
        return (None,-1)
    elif win == 2:
        return (None,1) 
    elif profondeur == 0:
        return (None,0)
    if maxi == True:
        #j2
        meilleurscore = -1000
        meilleurcoup = []
        coups_poss = coups_possible(plateau,decalage,dernier_coup,2)
        for i in range(len(coups_poss)):
            #deepcopy manuel
            plateau2 = [x[:] for x in plateau]
            decalage2 = decalage[:]
            dernier_coup2 = dernier_coup[:]
            coup = coups_poss[i]
            #joue le coup sur le plateau fictif
            coup_AI(plateau2,decalage2,2,coup)
            #score calcule recursivement
            score = minimax(plateau2,decalage2,dernier_coup2,profondeur-1,False)
            #teste le score et mets le meilleur coup dans une variable
            if meilleurscore < score[1]:
                meilleurscore = score[1]
                meilleurcoup = [(coup,score[1])]
            elif meilleurscore == score[1]:
                meilleurcoup.append((coup,score[1]))
    elif maxi == False:
        #j1
        meilleurscore = 1000
        meilleurcoup = []
        coups_poss = coups_possible(plateau,decalage,dernier_coup,1)
        for i in range(len(coups_poss)):
            plateau2 = [x[:] for x in plateau]
            decalage2 = decalage[:]
            dernier_coup2=dernier_coup[:]
            coup = coups_poss[i]
            coup_AI(plateau2,decalage2,1,coup)
            score=minimax(plateau2,decalage2,dernier_coup2,profondeur-1,True)
            if  meilleurscore > score[1]:
                meilleurscore = score[1]
                meilleurcoup = [(coup,score[1])]
            elif meilleurscore == score[1]:
                meilleurcoup.append((coup,score[1]))
    res=random.choice(meilleurcoup)
    choice_final = res[0]
    score_final = res[1]
    return (choice_final,score_final)

def coup_AI(plateau, decalage, joueur, coup):
    """Coup AI est une fonction qui teste les coups fictifs de minimax
    :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
    :param decalage: liste, represente le decalage de chaque ligne
    :param joueur: int, represente joueur qui a gagne
    :param coup: str, represente le coup a jouer
    :return None:
    """
    b = ['4-','3-','2-','1-','1+','2+','3+','4+']
    if coup in b:
        if coup[1] == '+':
            decalage[int(coup[0])-1]+=1     
        else:
            decalage[int(coup[0])-1]-=1
    else:
        if coup[0] == 'A':
            col = 0
        elif coup[0] == 'B':
            col = 1
        elif coup[0] == 'C':
            col = 2
        elif coup[0] == 'D':
            col = 3   
        ligne = int(coup[1])-1                
        plateau[ligne][col] = joueur
    return None
    
def boucle_jeu():
    """Lance une partie entre joueur et les laisse chacun jouer un coup jusqu'à ce qu'il y ait un gagnant
    :return: None
    
    """
    decalage = [0,0,0,0]
    plateau = nouveau_plateau()
    joueur = 1  # 1 ou 2
    gagnant = 0
    dernier_coup = None
    # continue jusqu'à ce qu'on ait un gagnant
    while gagnant == 0:
        afficher(plateau,decalage)        
        dernier_coup = coup(plateau, joueur, dernier_coup,decalage)
        gagnant = fin(plateau,decalage)        
        joueur = (joueur%2) + 1
    afficher(plateau,decalage)        
    if gagnant == 1 or gagnant == 2:
        print('joueur', gagnant, 'gagnant')
    elif gagnant == 3:
        print('egalite')

if __name__ == "__main__":
    boucle_jeu()  
