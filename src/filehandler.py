
from os import path, getcwd
from csv import *

with open(path.join(getcwd(),'src/files/options.txt'), newline='') as optionsFile:
    csvread = reader(optionsFile, delimiter=':')
    options = {str(row[0]):str(row[1]).replace(' ', '') for row in csvread}
def set_language(language):
    '''
    Met la langue en la langue choisie
    '''
    global traduction
    with open(path.join(getcwd(),'src/files/languages/{0}.txt'.format(language)), newline='') as languageFile:
        traduction = {row[0]:row[1].replace(' ', '', 1) for row in reader(languageFile, delimiter=':')}

if __name__ == '__main__':
    print("S'il vous plaît, exécutez le fichier main.py")
    raise FileNotFoundError("wrong file executed")