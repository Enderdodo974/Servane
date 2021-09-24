from tkinter import *

def bind_all_keys(classType):
    '''
    Associe tous les raccourcis claviers à la fenêtre.
    '''
    classType.bind_all('<Control-n>', lambda x: classType.new_list())
    classType.bind_all('<Control-o>', lambda x: classType.import_list())
    classType.bind_all('<Control-s>')
    classType.bind_all('<Control-Shift-s>')
    classType.bind_all('<Control-q>', lambda x: classType.quit())
    classType.bind_all('<Control-z>')
    classType.bind_all('<Control-y>')
    classType.bind_all('<Control-x>')
    classType.bind_all('<Control-c>')
    classType.bind_all('<Control-v>')
    classType.bind_all('<Control-a>')
    classType.bind_all('<Control-f>')
    classType.bind_all('<Control-h>')