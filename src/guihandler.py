#
# Ce script est le gestionnaire qui crée l'interface graphique de l'application Servane.
#

if __name__ == '__main__': # Permet d'empêcher l'utilisateur de lancer ce script
    print("S'il vous plaît, exécutez le fichier main.py")
    raise FileNotFoundError("wrong file executed")

import platform                     # Pour le système d'exploitation et l'interopérabilité
from tkinter import *               # Pour les interfaces graphiques
from tkinter.filedialog import *    # Boîtes de dialogues tkinter
from src import filehandler         # Gestionnaire de fichiers pour les traductions et les listes
from datetime import datetime       # Pour les erreurs et rendre facile le débogage
from tkinter.messagebox import *
#from os import system              # chercher (ctrl+f) -> system("python3 main.py") pour voir le commentaire

# Constantes
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
BACKGROUND_FONT = '#7dc4c6'
BACKGROUND_FONT_LABEL = '#396faf'
POSTS_NIGHT = ['MAT', 'BLOC', 'NUIT BLOC', 'ASTR']
POSTS_MORNING = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'D1', 'D2', 'E1', 'SuO',
                    'F1', 'Cs Obs', 'SAS1', 'SAS2', 'S3', 'S4', 'CsG', 'NR', 'REG', 'TRA', 'TRAN']
POSTS_AFTERNOON = ['S34', 'SeA', 'SeB', 'SeC', 'SeE', 'C3F1', 'BLOC', 'RadioIj', 'RadioMaMe', 'Cobs', 'Cs G', 'CsG', 'S?']
# Choix de la langue et définition des paramètres
OPTIONS = filehandler.set_options()
LANGUAGE = filehandler.set_language(OPTIONS['language'])

# Classe principale
class MainWindow(Tk):
    '''
    Classe tkinter pour l'application Servane
    '''
    def __init__(self) -> None:
        '''
        Initialisation de la classe
        '''
        Tk.__init__(self)
        self.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT)) # Taille de la fenêtre
        self.title(LANGUAGE['app.title']) # Titre
        self.minsize(960, 720) # Tailles minimum et maximum
        self.maxsize(1920, 1080)
        self.configure(background=BACKGROUND_FONT) # Couleur de fond d'écran
        self.iconphoto(True, PhotoImage(file=filehandler.APPICONPATH)) # Icone de l'application
        if OPTIONS['fullscreen'] == 'true': # Plein écran si la valeur est mise à True dans le fichier d'options
            self.set_full_screen()
        self.menuBar = Menu(self) # Menu de l'application
        self.config(menu=self.menuBar)
        self.IDList = [] # Liste de personnes
        self.postsVarList = [] # Liste des variables pour les menu-boutons pour les postes
        self.filelink = ''
        self.isListSaved = False

    def set_full_screen(self) -> None:
        '''
        Met la fenêtre principale en plein écran en fonction du système d'exploitation actuel.
        '''
        if platform.system() not in ('Linux', 'Windows', 'Darwin'): # Système d'exploitation non déterminé
            print('[{0}][ERR] - Current OS is unknown ({1})'.format(datetime.now(),platform.system()))
            print('[{0}][ERR] - Cannot set window in fullscreen. Skipping'.format(datetime.now()))
            return
        elif platform.system() == 'Linux': # Linux
            self.attributes('-zoomed', True)
        elif platform.system() == 'Windows': # Windows
            self.attributes('-fullscreen', True)
        elif platform.system() == 'Darwin': # macOS
            self.attributes('-zoomed', True)

    def save_as_list(self) -> None:
        '''
        Enregistre la liste de personnes dans un fichier
        '''
        if self.IDList == []:
            showerror(LANGUAGE['app.messagebox.save_as_list.no_list_found.title'],
                      LANGUAGE['app.messagebox.save_as_list.no_list_found.text'])
            print('[{0}][ERR] - No list found! Create a list before saving it.'.format(datetime.now()))
        else:
            self.filelink = asksaveasfilename(title=LANGUAGE['app.messagebox.continue_window.ask_save_as_file.title'],
                                              filetypes=[
            (LANGUAGE['app.messagebox.ask_open_list.text_type'], '.txt'),
            (LANGUAGE['app.messagebox.ask_open_list.timetable_type'], '.edth'),
            (LANGUAGE['app.messagebox.ask_open_list.csv_type'], '.csv'),
            (LANGUAGE['app.messagebox.ask_open_list.all_files_type'], '.*')])
            if self.filelink != '' and self.filelink != ():
                print('[{0}][INFO] - Saved list in file "{1}"'.format(datetime.now(),self.filelink))
                filehandler.open_file(self.filelink, 'write', None, self.IDList)
                self.isListSaved = True
            else:
                print('[{0}][INFO] - Cancelled operation for saving list'.format(datetime.now()))

    def save_current_list(self) -> None:
        '''
        Enregistre la liste de personnes actuelle dans le même fichier
        '''
        if not self.isListSaved:
            if self.IDList == []:
                showerror(LANGUAGE['app.messagebox.save_as_list.no_list_found.title'],
                          LANGUAGE['app.messagebox.save_as_list.no_list_found.text'])
                print('[{0}][ERR] - No list found! Create a list before saving it.'.format(datetime.now()))
            elif self.filelink == '' or self.filelink == ():
                self.save_as_list()
            else:
                print('[{0}][INFO] - Saved list (file: {1})'.format(datetime.now(),self.filelink))
                filehandler.open_file(self.filelink, 'write', None, self.IDList)
                self.isListSaved = True

    def import_list(self) -> None:
        '''
        Fenêtre messagebox tkinter pour l'importation de liste
        '''
        if self.IDList != []:
            print('[{0}][INFO] - List already existing, overwritting ?'.format(datetime.now()))
            if askyesno(LANGUAGE['app.messagebox.continue_window.ask_save_as_list.title'],
                        LANGUAGE['app.messagebox.continue_window.ask_save_as_list.text']):
                self.save_as_list()
        self.listCanvas.destroy()
        listFile = askopenfilename(title=LANGUAGE['app.messagebox.ask_open_list.title'], filetypes=[
            (LANGUAGE['app.messagebox.ask_open_list.text_type'], '.txt'),
            (LANGUAGE['app.messagebox.ask_open_list.timetable_type'], '.edth'),
            (LANGUAGE['app.messagebox.ask_open_list.csv_type'], '.csv'),
            (LANGUAGE['app.messagebox.ask_open_list.all_files_type'], '.*')])
        if listFile == () or listFile == '':
            print('[{0}][INFO] - Cancelled operation for opening list'.format(datetime.now()))
            self.start_window()
        else:
            self.filelink = listFile
            print('[{0}][INFO] - Opened list {1}'.format(datetime.now(), listFile))
            self.new_list_window()
            self.IDList = filehandler.open_file(listFile, 'read')
            for elem in self.IDList:
                elem = elem.split(';')
                self.IDListBox.insert('end', '{: <30}| {: <30}| {: <5}| {: <5}'.format(elem[0],elem[1],elem[2],elem[3]))
                # Le format {: <x} permet de coller le texte à gauche
            self.isListSaved = True

    def quit_app(self) -> None:
        '''
        Demande l'enregistrement de la liste avant de quitter
        '''
        if not self.isListSaved and self.IDList != []:
            ask_save_list = askyesnocancel(LANGUAGE['app.messagebox.continue_window.ask_save_as_list.title'],
                                           LANGUAGE['app.messagebox.continue_window.ask_save_as_list.text'])
            if ask_save_list == None:
                return
            elif ask_save_list == False:
                self.quit()
                exit(0)
            else:
                self.save_current_list()
                self.quit()
                exit(0)
        self.quit()
        exit(0)

    def create_menu(self) -> None:
        '''
        Fonction pour créer le menu déroulant de l'application.
        '''
        # Partie 'fichier':
        menuFile = Menu(self.menuBar, tearoff=0)

        menuFile.add_command(label=LANGUAGE['menu.file.new_list'], 
                             underline=0, 
                             accelerator='Ctrl+N', 
                             command=self.new_list_window)
        menuFile.add_command(label=LANGUAGE['menu.file.open_list'], 
                             underline=0, 
                             accelerator='Ctrl+O', 
                             command=self.import_list)
        menuFile.add_separator()
        menuFile.add_command(label=LANGUAGE['menu.file.save'], 
                             underline=6, 
                             accelerator='Ctrl+S', 
                             command=self.save_current_list)
        menuFile.add_command(label=LANGUAGE['menu.file.save_as'], 
                             underline=6, 
                             accelerator='Ctrl+Maj+S', 
                             command=self.save_as_list)
        menuFile.add_command(label=LANGUAGE['menu.file.export_as_ods'])
        menuFile.add_separator()
        menuFile.add_command(label=LANGUAGE['menu.file.open_settings'], command=self.show_options)
        menuFile.add_command(label=LANGUAGE['menu.file.quit_app'], 
                             underline=0, 
                             accelerator='Ctrl+Q', 
                             command=self.quit)

        self.menuBar.add_cascade(label=LANGUAGE['menu.file'], menu=menuFile)

        # Partie 'aide':
        menuHelp = Menu(self.menuBar, tearoff=0)

        menuHelp.add_command(label=LANGUAGE['menu.help.show_help'], 
                             accelerator='F11', 
                             command=self.show_help)
        menuHelp.add_command(label=LANGUAGE['menu.help.about'], command='')

        self.menuBar.add_cascade(label=LANGUAGE['menu.help'], menu=menuHelp)

    def show_help(self) -> None:
        '''
        Affichage de la fenêtre d'aide
        '''
        showinfo(LANGUAGE['app.messagebox.help_window.title'], LANGUAGE['app.messagebox.help_window.text'])

    def show_options(self) -> Toplevel:
        '''
        Affichage de la fenêtre d'options
        '''
        optionsWindow = Toplevel(self, background='#dbdbdb', takefocus=False)
        optionsWindow.geometry(str(WINDOW_WIDTH) + 'x' + str(WINDOW_HEIGHT))
        optionsWindow.title(LANGUAGE['app.options_window.title'])
        optionsWindow.minsize(960, 720) # Tailles minimum et maximum
        optionsWindow.maxsize(1920, 1080)

        # Bouton pour valider et quitter
        Button(optionsWindow,
               text=LANGUAGE['widget.options_window.button.quit'],
               font=('Arial', 16), command=optionsWindow.destroy).pack(side='bottom', pady=5)

        # Label pour le choix de la langue
        Label(optionsWindow,
              text='Langue de l\'application',
              background='#dbdbdb',
              font=('Arial', 16)).pack(pady=20)

        # Bouton-menu pour le choix de la langue
        self.selectedLanguage = StringVar(value=OPTIONS['language'])
        OptionsMenu = OptionMenu(optionsWindow,
                                self.selectedLanguage,
                                *(filehandler.list_languages_files()),
                                command=self.change_language)
        OptionsMenu.pack()

        # Label pour le plein écran
        fullScreenVar = IntVar(value=int(str(OPTIONS['fullscreen']).replace('true', '1').replace('false', '0')))
        Checkbutton(optionsWindow,
                    text='Affichage en plein écran',
                    font=('Arial', 16),
                    background='#dbdbdb',
                    variable=fullScreenVar).pack(pady=20)

    def change_language(self, language: str) -> None:
        '''
        Change la langue de l'application dans le langage souhaité
        '''
        if language != OPTIONS['language']:
            if askokcancel(LANGUAGE['app.messagebox.options_window.change_language.title'], 
                           LANGUAGE['app.messagebox.options_window.change_language.text']):
                optionFile = filehandler.open_file(filehandler.OPTIONSFILEPATH, 'readdict', ': ')
                optionFile['language'] = language
                filehandler.open_file(filehandler.OPTIONSFILEPATH, 'writedict', ': ', optionFile)
                self.destroy()
                print('[{0}][INFO] - Changed option \'language\'. Quitting application'.format(datetime.now()))
                #system("python3 main.py") pas fan de ça à cause de l'interopérabilité, 
                # même si ça fait l'effet attendu càd redémarrer le script
                exit(0)
            else:
                self.selectedLanguage.set(OPTIONS['language'])

    def remove_line(self) -> None:
        '''
        Retire la ligne sélectionnée de la liste de personnes
        '''
        selection: list = self.IDListBox.get('anchor').replace(' ','').split('|')
        self.IDListBox.delete('anchor')
        for elem in self.IDList:
            elemSplitted = elem.split(';')
            if elemSplitted[0] == selection[0]:
                self.IDList.remove(elem)

    def add_line(self) -> None:
        '''
        Ajoute une ligne à la liste de personnes
        '''
        try:
            int(self.hoursEntry.get())
        except ValueError:
            print('[{0}][INFO] - Invalid value for hours count. Try again'.format(datetime.now()))
            showwarning(LANGUAGE['app.messagebox.new_list.wrong_hours_count.title'], 
                        LANGUAGE['app.messagebox.new_list.wrong_hours_count.text'])
            return
        if self.nameEntry.get() == LANGUAGE['widget.new_list.default_value.name'] \
                or self.firstNameEntry.get() == LANGUAGE['widget.new_list.default_value.first_name'] \
                or self.pseudoEntry.get() == LANGUAGE['widget.new_list.default_value.pseudo'] \
                or ';' in self.firstNameEntry.get() or ';' in self.nameEntry.get() or ';' in self.pseudoEntry.get():
            print('[{0}][INFO] - Invalid values for identifier. Try again'.format(datetime.now()))
            showwarning(LANGUAGE['app.messagebox.new_list.wrong_entry.title'], 
                        LANGUAGE['app.messagebox.new_list.wrong_entry.text'])
        else:
            postsType = ''
            for elem in self.postsVarList:
                if elem.get() == 1:
                    postsType += '1'
                else:
                    postsType += '0'
            self.IDList.append(f'{self.nameEntry.get()};{self.firstNameEntry.get()}; \
                {(self.pseudoEntry.get()).upper()};{self.hoursEntry.get()};{postsType}')
            self.IDListBox.insert('end', '{: <30}| {: <30}| {: <5}| {: <5}'.format(self.nameEntry.get(), 
                self.firstNameEntry.get(),
                (self.pseudoEntry.get()).upper(), 
                self.hoursEntry.get()))
            self.isListSaved = False
            for elem in self.postsVarList:
                elem.set(1)
            print('[{0}][INFO] - Added identifiant to the list.'.format(datetime.now()))

    def start_window(self) -> None:
        '''
        Crée les objets de la fenêtre de départ
        '''
        try:
            self.newListFrame.destroy()
        except:
            print("[{0}][WARN] - Failed trying to destroy 'self.newListFrame'. Skipping".format(datetime.now()))
        # Canvas de choix des listes
        self.listCanvas = Canvas(self,
                                 background=BACKGROUND_FONT_LABEL,
                                 width=720, height=540,
                                 highlightbackground=BACKGROUND_FONT)
        self.listCanvas.place(relx=0.5, rely=0.5, anchor='center')
        self.listCanvas.pack_propagate(False)
        # Texte de bienvenue
        welcomeLabel = Label(self.listCanvas,
                             background=BACKGROUND_FONT_LABEL,
                             text=LANGUAGE['widget.start.label.welcome'],
                             font=('Helvetica', 30))
        welcomeLabel.pack(side='top', anchor='n', pady=60)
        # Bouton de création de liste
        newListButton = Button(self.listCanvas,
                               background='white',
                               foreground='black',
                               relief='solid',
                               text=LANGUAGE['widget.start.button.new_list'],
                               font=('Helvetica', 30),
                               command=self.new_list_window)
        newListButton.place(relx=0.5, rely=0.4, anchor='center')
        # Texte 'ou'
        labelOR = Label(self.listCanvas,
                        background=BACKGROUND_FONT_LABEL,
                        text=LANGUAGE['widget.start.label.or'],
                        font=('Helvetica', 30))
        labelOR.place(relx=0.5, rely=0.5, anchor='center')
        # Bouton d'importation de liste
        importListButton = Button(self.listCanvas,
                                  background='white',
                                  foreground='black',
                                  relief='solid',
                                  text=LANGUAGE['widget.start.button.import_list'],
                                  font=('Helvetica', 30),
                                  command=self.import_list)
        importListButton.place(relx=0.5, rely=0.6, anchor='center')

    def new_list_window(self) -> None:
        '''
        Fenêtre de création d'une nouvelle liste
        '''
        try:
            self.newListFrame.destroy()
        except:
            print("[{0}][WARN] - Failed trying to destroy 'self.newListFrame'. Skipping".format(datetime.now()))

        self.listCanvas.destroy()
        # Frame de nouvelle liste (plus facile pour tout supprimer)
        self.newListFrame = Frame(self, background=BACKGROUND_FONT)
        self.newListFrame.pack(side='top', expand=True, fill='both')
        self.newListFrame.pack_propagate(False)
        # Barre ascenseur
        scrollbar = Scrollbar(self.newListFrame, width=20)
        scrollbar.pack(side='right', fill='y')
        # Label de légende
        Label(self.newListFrame,
            text='{: <30}| {: <30}| {: <5}| {: <5}'.format(LANGUAGE['widget.new_list.default_value.name'],
                                                            LANGUAGE['widget.new_list.default_value.first_name'],
                                                            LANGUAGE['widget.new_list.default_value.pseudo'],
                                                            LANGUAGE['widget.new_list.default_value.hours_count']),
            font=('Arial', 16),
            background=BACKGROUND_FONT).pack(side='top', anchor='n')
        # Liste des personnes
        self.IDListBox = Listbox(self.newListFrame,
                                 width=50,
                                 height=10,
                                 relief='solid',
                                 font=('Arial', 20),
                                 yscrollcommand=scrollbar.set)
        self.IDListBox.pack(pady=4)
        scrollbar.config(command=self.IDListBox.yview)
        # Bouton pour continuer
        Button(self.newListFrame,
               relief='solid',
               text=LANGUAGE['widget.new_list.button.continue'],
               font=('Helvetica', 30),
               command=self.continue_window).pack(side='bottom', anchor='s', pady=10)
        # Bouton pour supprimer une ligne
        Button(self.newListFrame,
               relief='solid',
               text=LANGUAGE['widget.new_list.button.delete_line'],
               font=('Helvetica', 16),
               command=self.remove_line).pack(side='top', anchor='n')
        # Bouton pour ajouter une ligne
        Button(self.newListFrame,
               relief='solid',
               text=LANGUAGE['widget.new_list.button.add_id'],
               font=('Helvetica', 20),
               command=self.add_line).pack(side='bottom', anchor='s')
        # Entrée pour le nom
        self.nameEntry = Entry(self.newListFrame, width=30, relief='solid', font=('Arial', 16))
        self.nameEntry.place(relx=0.5, rely=0.6, anchor='center')
        self.nameEntry.insert(0, LANGUAGE['widget.new_list.default_value.name'])
        # Entrée pour le prénom
        self.firstNameEntry = Entry(self.newListFrame, width=30, relief='solid', font=('Arial', 16))
        self.firstNameEntry.place(relx=0.5, rely=0.65, anchor='center')
        self.firstNameEntry.insert(0, LANGUAGE['widget.new_list.default_value.first_name'])
        # Entrée pour le diminutif
        self.pseudoEntry = Entry(self.newListFrame, width=10, relief='solid', font=('Arial', 16))
        self.pseudoEntry.place(relx=0.5, rely=0.8, anchor='center')
        self.pseudoEntry.insert(0, LANGUAGE['widget.new_list.default_value.pseudo'])
        # Entrée pour le nombre d'heures
        self.hoursEntry = Entry(self.newListFrame, width=15, relief='solid', font=('Arial', 16))
        self.hoursEntry.place(relx=0.5, rely=0.75, anchor='center')
        self.hoursEntry.insert(0, LANGUAGE['widget.new_list.default_value.hours_count'])
        # Bouton-menu pour les gardes
        postsPart1Menu = Menubutton(self.newListFrame,
                                    relief='solid',
                                    text=LANGUAGE['widget.new_list.menubutton.posts_part1'],
                                    direction='above',
                                    font=('Arial', 16))
        postsPart2Menu = Menubutton(self.newListFrame,
                                    relief='solid',
                                    text=LANGUAGE['widget.new_list.menubutton.posts_part2'],
                                    direction='above',
                                    font=('Arial', 16))
        postsPart3Menu = Menubutton(self.newListFrame,
                                    relief='solid',
                                    text=LANGUAGE['widget.new_list.menubutton.posts_part3'],
                                    direction='above',
                                    font=('Arial', 16))
        postsMenu1 = Menu(postsPart1Menu, tearoff=0)
        postsMenu2 = Menu(postsPart2Menu, tearoff=0)
        postsMenu3 = Menu(postsPart3Menu, tearoff=0)
        counter = 0

        for elem in POSTS_NIGHT:
            self.postsVarList.append(IntVar(value=1))
            postsMenu1.add_checkbutton(label=elem, variable=self.postsVarList[counter], onvalue=1, offvalue=0)
            counter += 1

        for elem in POSTS_MORNING:
            self.postsVarList.append(IntVar(value=1))
            postsMenu2.add_checkbutton(label=elem, variable=self.postsVarList[counter])
            counter += 1

        for elem in POSTS_AFTERNOON:
            self.postsVarList.append(IntVar(value=1))
            postsMenu3.add_checkbutton(label=elem, variable=self.postsVarList[counter])
            counter += 1

        postsPart1Menu.config(menu=postsMenu1)
        postsPart2Menu.config(menu=postsMenu2)
        postsPart3Menu.config(menu=postsMenu3)
        postsPart1Menu.place(relx=0.3, rely=0.7, anchor='center')
        postsPart2Menu.place(relx=0.5, rely=0.7, anchor='center')
        postsPart3Menu.place(relx=0.7, rely=0.7, anchor='center')

    def continue_window(self) -> None:
        '''
        Fenêtre de choix de l'emploi du temps à créer
        '''
        if askyesno(LANGUAGE['app.messagebox.continue_window.ask_save_as_list.title'], 
                    LANGUAGE['app.messagebox.continue_window.ask_save_as_list.text']):
            self.save_as_list()
        self.newListFrame.destroy()
        Button(self, text='Générer l\'emploi du temps', font=('Arial', 30), ).place(relx=0.5, rely=0.5, anchor='center')