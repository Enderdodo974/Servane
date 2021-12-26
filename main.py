#!/usr/bin/env python3
#-*- coding utf-8 -*-

'''   Projet Servane (SERvice ANEsthésie)
   Développé par Dorian Hamdani
   Le but de ce projet est de fournir une
   plateforme de création de trame d'emploi du temps
   avec interface graphique et gestion de fichiers.

 A FAIRE:
 - Fenêtre des paramètres
 - Améliorer les graphiques 
 - Fenêtre de sélection de la date
 - Générateur d'emplois du temps
 - Fenêtre 'à propos'
 '''

from os import chdir, path; chdir(path.realpath(__file__)[:-7]) # On met le dossier de travail au dossier actuel
from src import guihandler # Importation du gestionnaire de l'interface graphique
from src import eventhandler # Importation du gestionnaire des évenements (touches)

# Code principal
if __name__ == '__main__':
    Servane = guihandler.MainWindow() # Classe principale
    eventhandler.bind_all_keys(Servane) # Attribution des touches
    Servane.create_menu() # Création des menus
    Servane.start_window() # Fenêtre de départ
    Servane.mainloop() # Boucle tkinter