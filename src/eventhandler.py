# Gestionnaire d'attributions des touches de l'application Servane

from tkinter import Tk

def bind_all_keys(classType: Tk) -> None:
    '''
    Associe tous les raccourcis claviers à la fenêtre.
    '''
    classType.bind_all('<Control-n>', lambda x: classType.new_list_window())
    classType.bind_all('<Control-o>', lambda x: classType.import_list())
    classType.bind_all('<Control-s>', lambda x: classType.save_current_list())
    classType.bind_all('<Control-Shift-S>', lambda x: classType.save_as_list())
    classType.bind_all('<Control-q>', lambda x: classType.quit_app())
    classType.bind_all('<F11>', lambda x: classType.show_help())