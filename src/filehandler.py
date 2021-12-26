# Gestionnaire de fichier de l'application Servane
# Utilisation de fichiers de langages et de fichier d'options.
# J'avais originellement utilisé le module CSV mais je n'en ai pas besoin en fait (je peux m'en passer avec .readlines(), .split() et .write())

if __name__ == '__main__': # Permet d'empêcher l'utilisateur de lancer ce script
    print("S'il vous plaît, exécutez le fichier main.py")
    raise FileNotFoundError("wrong file executed")

from os import path, getcwd # Pour avoir la gestion de fichiers
from datetime import datetime
from glob import glob # Outil pour le listing de fichiers

# Constantes
APPICONPATH = path.join(getcwd(), 'src/files/images/icon.png')
OPTIONSFILEPATH = path.join(getcwd(), 'src/files/options.txt')

def set_options() -> dict:
    '''
    Ouvre le fichier ~/src/files/options.txt ou le crée si il n'existe pas et retourne un dictionnaire contenant {option:valeur...}
    '''
    try:
        testFile = open(path.join(getcwd(),'src/files/options.txt'), 'r')
        testFile.close()
    except: # Fichier non existant
        print("[{0}][ERROR] - File ~/src/files/options.txt does not exist. Creating a new one".format(datetime.now()))
        with open(path.join(getcwd(),'src/files/options.txt'), 'w') as optionsFile: # Si le fichier n'existe pas on en crée un nouveau
            optionsFile.write("language: fr_fr\nfullscreen: true")
    return open_file(path.join(getcwd(),'src/files/options.txt'), 'readdict', ': ')

def set_language(language: str) -> dict:
    '''
    Ouvre le fichier ~/src/files/languages/[language].txt et renvoie un dictionnaire contenant {key:value}
    '''
    return open_file(file=path.join(getcwd(),'src/files/languages/{0}.txt'.format(language)), mode='readdict', delimiter=': ')
    # à faire: mettre un langage par défaut si aucun langage n'existe dans le dossier ?

def list_languages_files() -> list:
    '''
    Liste tous les fichiers de langues dans le dossier ~/src/files/languages/
    '''
    return [file[-9:-4] for file in glob(path.join(getcwd(), 'src/files/languages/*.txt'))]

def open_file(file: str, mode: str = 'read', delimiter: str or None = ..., writeItem: list or dict or None = ...):
    '''
    Ouvre le fichier 'file' avec 'mode' qui peut être:
        - 'read' pour une lecture. La fonction retourne une liste contenant chaque ligne du fichier
        - 'readdict' pour une lecture. La fonction retourne un dictionnaire d'éléments contenant chaque ligne 'ligne'.
            Chaque ligne du fichier doit être sous la forme: ligne[0] delimiter ligne[1] et la fonction retourne {ligne[0]:ligne[1],...}
        - 'write' pour une écriture qui remplace les lignes du fichier.
            La donnée à écrire est 'writeItem' et doit être une liste.
        - 'append' pour un écriture sans effaçage des lignes précédentes.
            La donnée à écrire est 'writeItem' et doit être une liste.
        - 'writedict' pour une écriture qui remplace les lignes du fichier. Les données à écrire doit être de type dictionnaire de la forme:
            {elem[0]:elem[1],...} et sont écrites dans le fichier sous la forme: elem[0] delimiter elem[1]
        - 'appenddict' pour une écriture qui ajoute les données à la fin du fichier. Le processus est le même que pour 'writedict'
        
        'delimiter' peut être un seul caractère (exemples: ';', '|'...) ou plusieurs caractères (exemples: ': ', '; '...) 
    '''
    assert mode in ('read', 'readdict', 'write', 'append', 'writedict', 'appenddict')
    try:
        testFile = open(file, 'r')
        testFile.close()
    except FileNotFoundError:
        if mode not in ('write', 'append', 'writedict', 'appenddict'):
            print('[{0}][ERR/FATAL] - File {1} does not exist. Aborting'.format(datetime.now(), file))
            raise FileNotFoundError(f'File {file} does not exist!')
    if mode in ('read', 'readdict'):
        if mode == 'read':
            with open(file, 'r') as openedFile:
                return [line.replace('\n','') for line in openedFile.readlines()] # Retourne une liste d'éléments
        else:
            with open(file, 'r') as openedFile:
                data = [line.replace('\n','') for line in openedFile.readlines()]
                return {row[0]:row[1] for row in [data[i].split(delimiter) for i in range(len(data))]} # Retourne un dictionnaire
    elif mode in ('write', 'append'):
        if mode == 'write':
            with open(file, 'w') as openedFile: # Le 'w' signifie write
                for elem in writeItem:
                    openedFile.write(elem+'\n')
        else:
            with open(file, 'a') as openedFile: # Le 'a' signifie append
                for elem in writeItem:
                    openedFile.write(elem+'\n')
    elif mode == 'writedict':
        with open(file, 'w') as openedFile:
            for elem in writeItem:
                openedFile.write(f'{elem}{delimiter}{writeItem[elem]}\n')
    else:
        with open(file, 'a') as openedFile:
            for elem in writeItem:
                openedFile.write(f'{elem}{delimiter}{writeItem[elem]}\n')