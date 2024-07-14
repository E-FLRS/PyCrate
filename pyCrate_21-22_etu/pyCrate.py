import time
import datetime

from fourni import simulateur
from outils import \
    creer_image, \
    creer_caisse, creer_case_vide, creer_cible, creer_mur, creer_personnage, \
    coordonnee_x, coordonnee_y, est_egal_a

# Constante à utiliser

VALEUR_COUP: int = 50


# Fonctions à développer

def jeu_en_cours(caisses: list, cibles: list) -> bool:
    """
    Fonction testant si le jeu est encore en cours et retournant un booléen comme réponse sur l'état de la partie.
    :param caisses: La liste des caisses du niveau en cours
    :param cibles: La liste des cibles du niveau en cours
    :return: True si la partie est finie, False sinon
    """
    jeu_fini: bool = False
    nb_element = 0

    for nb in range(0, len(caisses)):
        if caisses[nb] in cibles:
            nb_element += 1

    if nb_element == len(cibles):
        jeu_fini = True

    return jeu_fini


def charger_niveau(joueur: list, caisses: list, cibles: list, murs: list, path: str):
    """
    Fonction permettant de charger depuis un fichier.txt et de remplir les différentes listes permettant le
    fonctionnement du jeu (joueur, caisses, murs, cibles)
    :param joueur: liste des personnages
    :param caisses: liste des caisses
    :param cibles: liste des cibles
    :param murs: liste des murs
    :param path: chemin du fichier.txt
    :return:
    """
    with open(path, "r") as niveau:
        niveau = niveau.readlines()
    index_y: int = 0
    index_x: int = 0

    # index_x : gauche droite
    # index_y : haut bas

    for bn in range(0, len(niveau)):
        for nb in range(0, len(niveau[0])):
            index_x = nb
            if niveau[index_y][index_x] == "#":
                murs.append(creer_mur(index_x, index_y))
            elif niveau[index_y][index_x] == "@":
                joueur.append(creer_personnage(index_x, index_y))
            elif niveau[index_y][index_x] == "$":
                caisses.append(creer_caisse(index_x, index_y))
            elif niveau[index_y][index_x] == ".":
                cibles.append(creer_cible(index_x, index_y))
        index_y += 1


def definir_mouvement(direction: str, can, joueur: list, murs: list, caisses: list, liste_image: list):
    """
    Fonction permettant de définir les cases de destinations (il y en a 2 si le joueur pousse une caisse) selon la
    direction choisie.
    :param direction: Direction dans laquelle le joueur se déplace (droite, gauche, haut, bas)
    :param can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
    :param joueur: liste des joueurs
    :param murs: liste des murs
    :param caisses: liste des caisses
    :param liste_image: liste des images (murs, caisses etc...) détaillée dans l'énoncé
    :return:
    """
    deplace_joueur_x: int = coordonnee_x(joueur[0])
    deplace_joueur_y: int = coordonnee_y(joueur[0])
    deplace_caisse_x: int = coordonnee_x(joueur[0])
    deplace_caisse_y: int = coordonnee_y(joueur[0])

    if direction == "droite":
        deplace_joueur_x += 1
        deplace_caisse_x += 2
    elif direction == "gauche":
        deplace_joueur_x -= 1
        deplace_caisse_x -= 2
    elif direction == "haut":
        deplace_joueur_y -= 1
        deplace_caisse_y -= 2
    elif direction == "bas":
        deplace_joueur_y += 1
        deplace_caisse_y += 2

    effectuer_mouvement(caisses, murs, joueur, can, deplace_caisse_x, deplace_caisse_y, deplace_joueur_x,
                        deplace_joueur_y, liste_image)


def effectuer_mouvement(caisses: list, murs: list, joueur: list, can,
                        deplace_caisse_x: int, deplace_caisse_y: int, deplace_joueur_x: int, deplace_joueur_y: int,
                        liste_image: list):
    """
    Fonction permettant d'effectuer le déplacement ou de ne pas l'effectuer si celui-ci n'est pas possible.
    Voir énoncé "Quelques règles".
    Cette methode est appelée par mouvement.
    :param caisses: liste des caisses
    :param murs: liste des murs
    :param joueur: liste des joueurs
    :param can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
    :param deplace_caisse_x: coordonnée à laquelle la caisse va être déplacée en x (si le joueur pousse une caisse)
    :param deplace_caisse_y: coordonnée à laquelle la caisse va être déplacée en y (si le joueur pousse une caisse)
    :param deplace_joueur_x: coordonnée en x à laquelle le joueur va être après le mouvement
    :param deplace_joueur_y: coordonnée en y à laquelle le joueur va être après le mouvement
    :param liste_image: liste des images (murs, caisses etc...) détaillée dans l'énoncé
    :return:
    """
    position_personnage = creer_personnage(deplace_joueur_x, deplace_joueur_y)
    position_caisses = creer_caisse(deplace_caisse_x, deplace_caisse_y)

    if not position_caisses in murs:
        if not position_caisses in caisses:
            if position_personnage in caisses:
                caisses.remove(position_personnage)
                caisses.append(position_caisses)

    if not position_personnage in murs:
        if not position_personnage in caisses:
            creer_image(can, coordonnee_x(joueur[0]), coordonnee_y(joueur[0]), liste_image[6])
            del joueur[0]
            joueur.append(position_personnage)


def chargement_score(scores_file_path: str, dict_scores: dict):
    """
    Fonction chargeant les scores depuis un fichier.txt et les stockent dans un dictionnaire
    :param scores_file_path: le chemin d'accès du fichier
    :param dict_scores:  le dictionnaire pour le stockage
    :return:
    """

    with open(scores_file_path, "r") as score1:
        for nb in range(0, 5):
            ligne: str = score1.readline()
            score_liste: list = ligne.split(";")
            dict_scores[score_liste[0]] = score_liste[1:len(score_liste)]

def chargement_date_score(score_date_file_path: str, dict_date_score:dict):

    with open(score_date_file_path, "r") as date:
        for nb in range(0, 5):
            ligne: str = date.readline()
            date_liste: list = ligne.split(";")
            dict_date_score[date_liste[0]] = date_liste[1:len(date_liste)]

def maj_score(niveau_en_cours: int, dict_scores: dict, dict_date_score: dict) -> str:
    """
    Fonction mettant à jour l'affichage des scores en stockant dans un str l'affichage visible
    sur la droite du jeu.
    ("Niveau x
      1) 7699
      2) ... ").
    :param niveau_en_cours: le numéro du niveau en cours
    :param dict_scores: le dictionnaire pour stockant les scores
    :return str: Le str contenant l'affichage pour les scores ("\n" pour passer à la ligne)
    """
    if dict_scores == {}:
        return "le fichier des score n'existe pas"

    if not str(niveau_en_cours) in dict_scores.keys():
        liste: list = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
        dict_scores[str(niveau_en_cours)] = liste

    if dict_date_score == {}:
        return "le fichier des dates n'existe pas"
    if not str(niveau_en_cours) in dict_date_score.keys():
        liste2: list = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
        dict_date_score[str(niveau_en_cours)] = liste2

    affichage: str = ""
    nb: int = 1
    nb_date: int = 0

    affichage = "Niveau " + str(niveau_en_cours) + "\n"
    for elt in dict_scores[str(niveau_en_cours)]:
        affichage += str(nb) + ") " + elt + "     " + dict_date_score[str(niveau_en_cours)][nb_date] + "\n"
        nb_date += 1
        nb += 1

    return affichage

def calcule_score(temps_initial: float, nb_coups: int, score_base: int) -> int:
    """
    calcule le score du jouer
    :param temps_initial: debut du jeu
    :param nb_coups: nombre des mouvements
    :param score_base: score de base
    :return: le score du jouer
    """

    pass

def enregistre_score(temps_initial: float, nb_coups: int, score_base: int, dict_scores: dict,
                     niveau_en_cours: int, dict_date_score: dict):
    """
    Fonction enregistrant un nouveau score réalisé par le joueur. Le calcul de score est le suivant :
    score_base - (temps actuel - temps initial) - (nombre de coups * valeur d'un coup)
    Ce score est arrondi sans virgule et stocké en tant que int. Le score est mis à jour dans le
    dictionnaire.
    :param temps_initial: le temps initial
    :param nb_coups: le nombre de coups que l'utilisateurs à fait (les mouvements)
    :param score_base: Le score de base identique pour chaque partie
    :param dict_scores: Le dictionnaire stockant les scores
    :param niveau_en_cours: Le numéro du niveau en cours
    """
    temps_actuel: float = time.time()
    score: int = 0
    score = round(score_base - (temps_actuel - temps_initial) - (nb_coups * VALEUR_COUP))
    changement: int = None
    inter: int = None
    changement = str(score)
    now = datetime.datetime.now()
    date_auj: str = ""
    date_auj = now.strftime("%d/%m/%Y %H:%M:%S ")
    date_actuelle = date_auj

    for nb in range(0, len(dict_scores[str(niveau_en_cours)])):

        if changement > dict_scores[str(niveau_en_cours)][nb]:
            if not changement in dict_scores[str(niveau_en_cours)]:
                inter = str(dict_scores[str(niveau_en_cours)][nb])
                date_inter = str(dict_date_score[str(niveau_en_cours)][nb])
                dict_scores[str(niveau_en_cours)][nb] = changement
                dict_date_score[str(niveau_en_cours)][nb] = date_actuelle
                changement = inter
                date_actuelle = date_inter







def update_score_file(scores_file_path: str, dict_scores: dict, score_date_file_path: str, dict_date_score:dict):
    """
    Fonction sauvegardant tous les scores dans le fichier.txt.
    :param scores_file_path: le chemin d'accès du fichier de stockage des scores
    :param dict_scores: Le dictionnaire stockant les scores
    :return:
    """

    dict_pret: str = ""
    with open(scores_file_path, "w") as score:
        for nb in range(1,5):
            if str(nb) in dict_scores.keys():
                dict_pret += str(nb)
                for elt in dict_scores[str(nb)]:
                    dict_pret += ";"+elt
                if dict_pret[len(dict_pret)-1] != "\n":
                    dict_pret += "\n"

        score.write(dict_pret)

    dict_date_pret: str = ""

    with open(score_date_file_path, "w") as date:
        for nombre in range(1,5):
            if str(nombre) in dict_date_score.keys():
                dict_date_pret += str(nombre)
                for elt in dict_date_score[str(nombre)]:
                    dict_date_pret += ";"+elt
                if dict_date_pret[len(dict_date_pret)-1] != "\n":
                    dict_date_pret += "\n"

        date.write(dict_date_pret)

if __name__ == '__main__':
    simulateur.simulate()
