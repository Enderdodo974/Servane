#!/usr/bin/env python3
#-*- coding utf-8 -*-

##########
#
#   Projet Servane (SERvice ANEsthésie)
#   Développé par Dorian Hamdani
#   Le but de ce projet est de fournir une
#   plateforme de création de trame d'emploi du temps
#   avec interface graphique et gestion de fichiers.
#
##########

from src import guihandler
from src import eventhandler
#Code principal
if __name__ == '__main__':
    Servane = guihandler.MainWindow()
    eventhandler.bind_all_keys(Servane)
    Servane.create_menu()
    Servane.create_start_widgets()
    Servane.mainloop()