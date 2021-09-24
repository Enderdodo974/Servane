##########
#
#Ceci est le gestionnaire qui crée l'interface graphique de l'application Servane.
#
##########

import platform as pf
from tkinter import *
from tkinter.filedialog import *
from src import filehandler
#CONSTANTES
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
BACKGROUND_FONT = '#7dc4c6'
BACKGROUND_FONT_LABEL = '#396faf'

# Choix de la langue
filehandler.set_language(filehandler.options['language'])
languageText = filehandler.traduction
#Classe principale
class MainWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.geometry(str(self.WINDOW_WIDTH) + "x" + str(self.WINDOW_HEIGHT))
        self.title(languageText['app.title'])
        self.minsize(720, 720)
        self.maxsize(1920, 1080)
        self.configure(background=BACKGROUND_FONT)
        if filehandler.options['fullscreen'] == 'true':
            self.set_full_screen()
        self.menuBar = Menu(self)
        self.config(menu=self.menuBar)

    def set_full_screen(self):
        '''
        Met la fenêtre principale en plein écran en fonction du système d'exploitation actuel.
        '''
        if pf.system() == 'Linux':
            self.attributes('-zoomed', True)
        elif pf.system() == 'Windows':
            self.attributes('-fullscreen', True)
        elif pf.system() == 'Darwin':
            self.attributes('-zoomed', True)

    def create_menu(self):
        '''
        Fonction pour créer le menu déroulant de l'application.
        '''
        # Partie 'fichier':
        menuFile = Menu(self.menuBar, tearoff=0)

        menuFile.add_command(label=languageText['menu.file.new_list'], underline=0, accelerator='Ctrl+N', command=self.new_list)
        menuFile.add_command(label=languageText['menu.file.open_list'], underline=0, accelerator='Ctrl+O', command=self.import_list)
        menuFile.add_separator()
        menuFile.add_command(label=languageText['menu.file.save'], underline=6, accelerator='Ctrl+S', command=self.save)
        menuFile.add_command(label=languageText['menu.file.save_as'], underline=6, accelerator='Ctrl+Maj+S', command=self.save_as)
        menuFile.add_command(label=languageText['menu.file.export_as_ods'])
        menuFile.add_separator()
        menuFile.add_command(label=languageText['menu.file.open_settings'], command=self.servane_options)
        menuFile.add_command(label=languageText['menu.file.quit_app'], underline=0, accelerator='Ctrl+Q', command=self.quit)

        self.menuBar.add_cascade(label=languageText['menu.file'], menu=menuFile)

        # Partie 'éditer':
        menuEdit = Menu(self.menuBar, tearoff=0)

        menuEdit.add_command(label=languageText['menu.edit.cancel'], underline=None, accelerator='Ctrl+Z', command=self.cancel)
        menuEdit.add_command(label=languageText['menu.edit.reset'], underline=None, accelerator='Ctrl+Y', command=self.reset)
        menuEdit.add_separator()
        menuEdit.add_command(label=languageText['menu.edit.cut'], underline=None, accelerator='Ctrl+X', command=self.cut)
        menuEdit.add_command(label=languageText['menu.edit.copy'], underline=0, accelerator='Ctrl+C', command=self.copy)
        menuEdit.add_command(label=languageText['menu.edit.paste'], underline=None, accelerator='Ctrl+V', command=self.paste)
        menuEdit.add_separator()
        menuEdit.add_command(label=languageText['menu.edit.select_all'], underline=None, accelerator='Ctrl+A', command=self.select_all)
        menuEdit.add_command(label=languageText['menu.edit.search'], underline=None, accelerator='Ctrl+F', command=self.search)
        menuEdit.add_command(label=languageText['menu.edit.replace'], underline=3, accelerator='Ctrl+H', command=self.replace)

        self.menuBar.add_cascade(label=languageText['menu.edit'], menu=menuEdit)
        
        # Partie 'aide':
        menuHelp = Menu(self.menuBar, tearoff=0)

        menuHelp.add_command(label=languageText['menu.help.show_help'], accelerator='F11', command='')
        menuHelp.add_command(label=languageText['menu.help.about'], command='')

        self.menuBar.add_cascade(label=languageText['menu.help'], menu=menuHelp)

    def create_start_widgets(self):
        try:
            self.newListFrame.destroy()
        except:
            pass
        # Canvas de choix des listes
        self.listCanvas = Canvas(self, background=BACKGROUND_FONT_LABEL, width=720, height=540, highlightbackground='#1177DD')
        self.listCanvas.place(relx=0.5, rely=0.5, anchor='center')
        self.listCanvas.pack_propagate(False)
        # Texte de bienvenue
        welcomeLabel = Label(self.listCanvas, background=BACKGROUND_FONT_LABEL, text='Bienvenue sur l\'application Servane', font=('Helvetica', 30))
        welcomeLabel.pack(side='top', anchor='n', pady=60)
        # Bouton de création de liste
        newListButton = Button(self.listCanvas, background='white', foreground='black', text=' Créer une nouvelle liste ', font=('Helvetica', 30), command=self.new_list)
        newListButton.place(relx=0.5, rely=0.4, anchor='center')
        # Texte 'ou'
        labelOR = Label(self.listCanvas, background=BACKGROUND_FONT_LABEL, text='ou', font=('Helvetica', 30))
        labelOR.place(relx=0.5, rely=0.5, anchor='center')
        # Bouton d'importation de liste
        importListButton = Button(self.listCanvas, background='white', foreground='black', text='Ouvrir une liste existante', font=('Helvetica', 30), command=self.import_list)
        importListButton.place(relx=0.5, rely=0.6, anchor='n')

    def new_list(self):
        try:
            self.newListFrame.destroy()
        except:
            pass

        self.listCanvas.destroy()
        # Frame de nouvelle liste (plus facile pour tout supprimer)
        self.newListFrame = Frame(self, background=BACKGROUND_FONT)
        self.newListFrame.pack(side='top', expand=True, fill='both')
        self.newListFrame.pack_propagate(False)
        # Liste des personnes
        self.idListBox = Listbox(self.newListFrame, width=40, height=10, font=('Verdana', 20))
        self.idListBox.pack(pady=10)
        self.idListBox.insert(END, *['test', 'coucou', 'salut'])
        # Bouton pour continuer
        continueButton = Button(self.newListFrame, text='Continuer', font=('Helvetica', 30))
        continueButton.pack(side='bottom', anchor='s', pady=30)
        # Bouton pour supprimer une ligne
        deleteButton = Button(self.newListFrame, text='Supprimer la ligne sélectionnée', font=('Helvetica', 12), command=lambda: self.idListBox.delete(ACTIVE))
        deleteButton.place(relx=0.99, rely=0.6, anchor='e')

    def import_list(self):
        self.listCanvas.destroy()
        self.listFile = askopenfilename(title='Choisissez une liste à importer', filetypes=[
            ('Texte', '.txt'),
            ('Emploi du temps Servane', '.edth'),
            ('Fichier CSV', '.csv'),
            ('Tous les fichiers', '.*')])
        if self.listFile == () or self.listFile == "":
            self.create_start_widgets()
    def save(self):
        pass

    def save_as(self):
        pass

    def servane_options(self):
        pass

    def cancel(self):
        pass

    def reset(self):
        pass

    def cut(self):
        pass

    def copy(self):
        pass

    def paste(self):
        pass

    def select_all(self):
        pass

    def search(self):
        pass

    def replace(self):
        pass
if __name__ == '__main__':
    print("S'il vous plaît, exécutez le fichier main.py")
    raise FileNotFoundError("wrong file executed")