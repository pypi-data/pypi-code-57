# -*- coding: utf-8 -*-

#   Didacto, un logiciel d'aide à l'organisation d'un corpus didactique
#   Copyright (C) 2020  Marco de Freitas
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.
#   If not, see <https://www.gnu.org/licenses/>.
#
#    contact:marco@sillage.ch

from os import *

import tkinter
import tkinter.ttk
import tkinter.filedialog
import tkinter.simpledialog
import tkinter.messagebox

import webbrowser


class Tree():
    """Class for treeview specific functions"""
    def __init__(self, root):
        pass


class View(tkinter.Frame):
    def __init__(self, root, model, controller):
        """Initialize the main window"""
        self.model = model
        self.root = root
        self.controller = controller
        self.pref_win_statut = False
        self.about_win_statut = False
        tkinter.Frame.__init__(self)
        self.pack(fill='both', expand=True, padx=5, pady=5)
        self.create_widgets()
        self.create_popup_menu()


    def create_widgets(self):
        """Create the main window widgets"""
        # Menubar creation and event binding
        self.menubar = tkinter.Menu(self)
        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Choisir Dossier',
                                  accelerator='ctrl+i',
                                  command=self.choose_folder)
        self.filemenu.add_command(label='Rafraîchir',
                                  accelerator='ctrl+r',
                                  command=self.tree_refresh)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Préférences',
                                  command=self.create_preferences_window)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Quiter',
                                  accelerator='ctrl+q',
                                  command=self.controller.quit)
        self.menubar.add_cascade(label='Fichier', menu=self.filemenu)
        self.helpmenu = tkinter.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='Aide',
                                  command=self.open_readthedocs)
        self.helpmenu.add_command(label='A propos',
                                  command=self.create_about_window)
        self.menubar.add_cascade(label='Aide', menu=self.helpmenu)
        self.root.bind('<Control-i>', self.select_folder)
        self.root.bind('<Control-r>', self.refresh_treeview)
        self.root.bind('<Control-q>', self.close_programm)
        self.root.config(menu=self.menubar)

        # Main window content, path stringVAr, refresh and open-collapse action buttons

        self.corpora_path = tkinter.StringVar('')
        self.emplacement_label = tkinter.StringVar('')
        

        self.l0 = tkinter.Label(self, textvariable=self.emplacement_label)
        
        self.l0.grid(row=0,column=0, sticky=tkinter.W)
        self.checkbox_value = tkinter.BooleanVar()
        checkbox = tkinter.Checkbutton(self,
                               text="Inclure sous-dossiers",
                               variable=self.checkbox_value,
                               command=self.do_nothing).grid(row=0, column=1,
                                                             sticky=tkinter.W)


        self.collapsebox_value = tkinter.BooleanVar()
        collapsebox = tkinter.Checkbutton(self,
                                  text="Ouvrir/Fermer tout",
                                  variable=self.collapsebox_value,
                                  command=lambda:
                                       self.collapse_nodes(
                                           self.collapsebox_value.get())).grid(row=1, column=1,
                                                                               sticky=tkinter.W)
        # Treeview and scrollbar
        self.yscroll = tkinter.Scrollbar(self)
        
        self.tv = tkinter.ttk.Treeview(self)
        self.tv.configure(yscrollcommand=self.yscroll.set, selectmode='browse')
        self.tv['columns'] = ("files","path")
        self.tv["show"] = ['tree', 'headings']
        
        self.tv.column('#0', width=250, stretch=True)
        self.tv.column('files', width=250, stretch=True)
        self.tv.column('path', width=250, stretch=True)                            
        
        self.tv.heading('#0', text='Mots-clef')
        self.tv.heading('files', text='Fichiers', anchor='center')
        self.tv.heading('path', text='Chemin', anchor='center')
        
        self.tv.bind('<<TreeviewSelect>>', self.prout)
        self.tv.bind('<<TreeviewOpen>>', self.prouti)
        self.tv.bind('<<TreeviewClose>>', self.prouta)
        self.tv.bind("<Double-1>", self.on_double_click)
        self.tv.bind("<ButtonRelease-3>",  self.do_popup)
        
        self.tv.grid(row=4, column=0, columnspan=3, sticky=tkinter.NSEW, pady=5)

        self.yscroll.configure(orient='vertical',command=self.tv.yview)
        self.yscroll.grid(row=4, column=3, sticky=tkinter.N+tkinter.S+tkinter.W, pady=5 )

        self.buttonChoose = tkinter.Button(self,
                                   text='Choisir',
                                   command=self.choose_folder, width=7).grid(row=0, column=2)
        self.buttonRefresh = tkinter.Button(self,
                                    text='Rafraîchir',
                                    command=self.tree_refresh, width=7).grid(row=1, column=2)

        self.keyword = tkinter.StringVar()
        self.keyword.set('Double cliquer sur un mots-clef affiche ici sa définition')
        self.keyword_explained = tkinter.StringVar()
        self.l2 = tkinter.Label(self, textvariable=self.keyword).grid(row=5, sticky=tkinter.W)
        self.buttonSetKeywordExplanation = tkinter.Button (self,
                                                   text = "Définir",
                                                   command= self.set_key_explanation, width=7)
        self.buttonSetKeywordExplanation.grid(row=5, column=2, sticky=tkinter.S)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)
        
        self.get_saved_prefs()
        self.tree_initialise()
        self.curent_keyword_explanation=''

    def create_popup_menu(self):
        '''initialize the popup menu called by the right click'''
        self.popup = tkinter.Menu(self, tearoff=0)
        self.popup.add_command(label="Ouvrir fichier source",
                               command=lambda: self.open_source(self.popup_item))
        self.popup.add_command(label="Modifier mots-clés", command=self.edit_pdf_keywords)



    def do_popup(self, event):
        # display the popup menu
        self.popup.tk_popup(event.x_root, event.y_root, 0)
        self.popup_item = self.tv.identify("item", event.x, event.y)


    def open_source(self, item):
        """Function called by mouse right click, calls opend notation file function."""
        name = self.tv.item(item)["values"][0][:-4]+'.ly'
        folder = self.tv.item(item)["values"][1]
        if self.tv.item(item)["values"][1] == "":
            path = self.absolute_path(self.corpora_path.get(),name)
        else:
            folder = self.tv.item(item)["values"][1]
            path = self.absolute_path(folder, name)
        # path = self.absolute_path(self.corpora_path.get(), name)
        self.controller.run_file(path)     




    def edit_pdf_keywords(self):
        name = self.tv.item(self.popup_item)["values"][0] #prompts pdf file name
        prompt = name
        folder = self.tv.item(self.popup_item)["values"][1]
        if folder == "":
            path = self.absolute_path(self.corpora_path.get(),name)
        else:
            path = self.absolute_path(folder, name)
        curent_value = self.model.get_info(path)
        title = "Modifier mots-clefs"
        new_keywords = tkinter.simpledialog.askstring(title, prompt, initialvalue = curent_value)
        self.controller.edit_pdf_keywords(path, new_keywords)
        self.tree_refresh()


        
    def set_key_explanation(self):
        title = 'Référence des mots clés'
        prompt = ('Donnez une explication simple de ' + self.curent_keyword)
        curent_value = self.keyword_explained.get()
        prout =  tkinter.simpledialog.askstring(title, prompt, initialvalue = curent_value)
        if prout is not None:
            self.model.user_data.set(self.curent_keyword,prout)
            self.controller.write_user_data()
            self.keyword.set(self.curent_keyword+": "+prout)
  

    def get_saved_prefs(self):
        """This function recalls prefs stored values"""
        self.prefs=self.controller.open_saved_prefs()
        self.prefs_path = self.prefs['path']
        self.prefs_separator = self.prefs['separator']
        self.prefs_notation = self.prefs['notation_format']
        

    def tree_initialise(self):
        """This function init tree data and displays it"""
        if self.prefs_path == '':
            pass
        else:
            self.corpora_path.set(self.prefs_path)
            self.emplacement_label.set('Emplacement:'+ self.prefs_path)
            self.get_saved_prefs()
            self.tree_refresh()
            

    def collapse_nodes(self, value):
        """Treview function, collapse/open all nodes"""
        for tree_index in range(len(self.model.wordsDict)):
            self.tv.item(tree_index, open=value)





# Cette fonction efface le contenu de l'arbre
    def tree_delete(self, size):
            if size > 0:
                for idid in range(size):
                    self.tv.delete(idid)

    def relative_path(self, default, curent):
        """This function returns an relative from to given path"""
        return curent.replace(default+"/", "")

    def absolute_path(self, default, item):
        """This function returns an absolute path"""
        return default + "/" + item


# Cette fonction recrée un arbre à partir du dictionnaire
    def tree_repopulate(self):
        """
        Builds the tree from model.wordsDict

        Items in tree are
        """
        tree_index = 0
        for key in self.model.wordsDict:
            self.tv.insert('',
                           index=tree_index,
                           iid=tree_index,
                           text=key,
                           values=[''])
            for list_index in range(len(self.model.wordsDict[key])):
                if self.checkbox_value.get() is True:
                    path=self.model.wordsDict[key][list_index]['path']
                    self.tv.insert(tree_index,
                               index=tree_index,
                               text='',
                               values=[self.model.wordsDict[key][list_index]['name'], path])
                else:
                    path=""
                    self.tv.insert(tree_index,
                               index=tree_index,
                               text='',
                               values=[self.model.wordsDict[key][list_index]['name'],path])
            tree_index += 1

    def tree_refresh(self):  
        treeSize = len(self.model.wordsDict)
        path = self.corpora_path.get()
        recursive = self.checkbox_value.get()
        self.model.scan_repertory(path, recursive)
        self.tree_delete(treeSize)
        self.tree_repopulate()
        self.keyword_explained.set('')
        if len(self.model.errors_text)>0:
            tkinter.messagebox.showwarning("Erreurs", self.model.errors_text)
        
# fontions de la fenêtre principale
    def get_directory(self):
        givenPath = tkinter.filedialog.askdirectory()
        if givenPath :
            return givenPath
        else:
            return

    def choose_folder(self):
        treeSize = len(self.model.wordsDict)
        newPath = self.get_directory()
        if newPath is not None:
            self.corpora_path.set(newPath)
            self.emplacement_label.set('Emplacement:'+str(self.corpora_path.get()))
            
            recursive = self.checkbox_value.get()
            self.model.scan_repertory(newPath, recursive)
            self.tree_delete(treeSize)
            self.tree_repopulate()
            if len(self.model.errors_text)>0:
                tkinter.messagebox.showerror("Erreurs", self.model.errors_text)

# gestion des racourcis clavier
    def select_folder(self, event):
        """Command function for keyboard shortcuts, calls path selection function."""
        self.choose_folder()

    def refresh_treeview(self, event):
        """Command function for keyboard shortcuts, calls treeview refresh function."""
        self.tree_refresh()

    def close_programm(self, event):
        """Command function for keyboard shortcuts, calls programm quit function."""
        self.controller.quit()

# Test sur la sélection par la souris
    def prout(self, event):
        """This funtion """
        pass
        # print("selected:" + self.tv.focus())
        # region= self.tv.identify('region',event.x,event.y)
        # print(region)

    def prouti(self, event):
        pass # item = self.tv.identify("item", event.x, event.y)
        # print(item)
        # print("Open")

    def prouta(self, event):
        pass # print("Close")

# Gestion de la souris        
    def on_double_click(self, event):
        """Function called by Mouse double click, calls open pdf file function."""
        item = self.tv.identify("item", event.x, event.y)
        if item.startswith('I'):
            name = self.tv.item(item)["values"][0]
            if self.checkbox_value.get() is True:
                tv_path = self.tv.item(item)["values"][1]
                path = self.absolute_path(tv_path, name)
            if self.checkbox_value.get() is False:
                path = self.absolute_path(self.corpora_path.get(), name)
            self.controller.run_file(path)
        else:
            key = self.tv.item(item)['text']#############
            self.curent_keyword= key
            #print(key)
            try:
                value = self.model.user_data.get(key)
            except:
                value = ''
            keyword = key + ': '
            self.keyword.set(keyword+value)
            self.keyword_explained.set(value)
                

    def on_right_click(self, event):
        """Function called by mouse right click, calls opend notation file function."""
        item = self.tv.identify("item", event.x, event.y)
        name = self.tv.item(item)["values"][0][:-4]+'.ly'
        folder = self.tv.item(item)["values"][1]
        if self.tv.item(item)["values"][1] == "":
            path = self.absolute_path(self.corpora_path.get(),name)
        else:
            folder = self.tv.item(item)["values"][1]
            path = self.absolute_path(folder, name)
        # path = self.absolute_path(self.corpora_path.get(), name)
        self.controller.run_file(path)








    def open_readthedocs(self):
        url = "https://didacto.readthedocs.io/fr/latest/"
        webbrowser.open(url,new=0, autoraise=True)

# création des sous-fenêtres 
    def create_about_window(self):
        """About Window Creation.Singleton mecanism"""
        about_window = AboutWindow(self.root)

    def create_preferences_window(self):
        """User preferences window creation"""
        self.prefs = PreferencesWindow(self.root, self.controller, self)

    def do_nothing(self):
        """This functino does nothing. Used as Default value for a new widget command function."""
        pass




class PreferencesWindow():
    def __init__(self, root, controller, view):
        self.root = root
        self.controller = controller
        self.view = view
        self.preferences_window = tkinter.Toplevel(self.root, padx=5, pady=5)
        self.preferences_window.wm_title("Préférences")
       
        self.buttonChooseDefaultPath = tkinter.Button(
                            self.preferences_window,
                            text='Choisir un dossier a indexer par défaut',
                            command=self.choose_default)

        self.buttonChooseDefaultPath.pack()
        self.path_label = tkinter.StringVar()

        self.l1 = tkinter.Label(self.preferences_window,
                        textvariable=self.path_label)
        self.l1.pack()
        self.l2 = tkinter.Label(self.preferences_window,
                       text="Séparateur par défaut")
        self.l2.pack()
        self.separator = tkinter.StringVar()
        self.R1 = tkinter.Radiobutton(self.preferences_window,
                         text="espace",
                         variable=self.separator,
                         value=" ",
                         command=lambda: self.set_temp_prefs('', None))
        self.R1.pack(anchor=tkinter.CENTER)
        self.R2 = tkinter.Radiobutton(self.preferences_window,
                         text="virgule",
                         variable=self.separator,
                         value=",",
                         command=lambda: self.set_temp_prefs(',', None))
        self.R2.pack(anchor=tkinter.CENTER)
        self.l3 = tkinter.Label(self.preferences_window,
                       text="Format des fichiers de notation")
        self.l3.pack()
        self.notation_format = tkinter.StringVar()
        self.R3 = tkinter.Radiobutton(self.preferences_window,
                         text="Lylipond",
                         variable=self.notation_format,
                         value=".ly ",
                         command=lambda: self.set_temp_prefs(None, '.ly'))
        self.R3.pack(anchor=tkinter.CENTER)
        self.R4 = tkinter.Radiobutton(self.preferences_window,
                         text="Musescore",
                         variable=self.notation_format,
                         value=".mscz",
                         command=lambda: self.set_temp_prefs(None, '.mscz'))
        self.R4.pack(anchor=tkinter.CENTER)
        self.R5 = tkinter.Radiobutton(self.preferences_window,
                         text="Sibélius",
                         variable=self.notation_format,
                         value=".sib",
                         command=lambda: self.set_temp_prefs(None, '.sib'))
        self.R5.pack(anchor=tkinter.CENTER)
        self.R6 = tkinter.Radiobutton(self.preferences_window,
                         text="Finale",
                         variable=self.notation_format,
                         value=".musx",
                         command=lambda: self.set_temp_prefs(None, '.musx'))
        self.R6.pack(anchor=tkinter.CENTER)
        self.buttonResetPreferences = tkinter.Button(self.preferences_window,
                                             text='Rétablir valeurs par défaut',
                                             command=self.reset_prefs)
        self.buttonResetPreferences.pack(side=tkinter.RIGHT)
        self.buttonDiscardPreferences = tkinter.Button(self.preferences_window,
                                               text='Annuler',
                                               command=self.close_prefs)
        self.buttonDiscardPreferences.pack(side=tkinter.RIGHT)
        self.buttonSavePreferences = tkinter.Button(self.preferences_window,
                                            text='Sauvegarder',
                                            command=self.save_temp_prefs)
        self.buttonSavePreferences.pack(side=tkinter.RIGHT)
        self.prefs=self.controller.open_saved_prefs()
        self.prefs_path=self.prefs['path']
        self.prefs_separator=self.prefs['separator']
        self.prefs_notation=self.prefs['notation_format']
        self.display_saved_prefs()
        self.invoke_prefs()

    def get_saved_prefs(self):
        """This function recalls stored values"""
        self.prefs=self.controller.open_saved_prefs()
        self.prefs_path=self.prefs['path']
        self.prefs_separator=self.prefs['separator']
        self.prefs_notation=self.prefs['notation_format']

    def invoke_prefs(self):
        """This functions displays current prefs values"""
        self.path_label.set(self.prefs_path)#
        if self.prefs_separator == '':
            self.R1.invoke()
        elif self.prefs_separator == ',':
            self.R2.invoke()
        if self.prefs_notation == '.ly':
            self.R3.invoke()
        elif self.prefs_notation == '.mscz':
            self.R4.invoke()
        elif self.prefs_notation == '.sib':
            self.R5.invoke()
        elif self.prefs_notation == '.musx':
            self.R6.invoke()

    def choose_default(self):
        """This function calls system specific select path mecanism and displays new path value, not saved"""
        newPath = self.view.get_directory()
        self.path_label.set(newPath)
        self.prefs_path=newPath

    def reset_prefs(self):
        """This function dispays default values, not saved"""
        self.prefs_path=''
        self.set_temp_prefs('', '.ly')
        self.invoke_prefs()

    def set_temp_prefs(self, separator, notation):
        if separator != None:
            self.prefs_separator=separator
        if notation != None:
            self.prefs_notation=notation

    def save_temp_prefs(self):
        self.prefs={'path': self.prefs_path , 'separator':self.prefs_separator,
                    'notation_format':self.prefs_notation}
        self.controller.save_new_user_prefs(self.prefs)
        self.close_prefs()

    def display_saved_prefs(self):
        """ This function asks curent prefs to controller and display them"""
        self.get_saved_prefs()
        self.path_label.set(self.prefs_path)
        self.invoke_prefs()

    def close_prefs(self):
        """Manual single window Preferences Window destruction."""
        self.view.pref_win_statut = False
        self.preferences_window.destroy()

class AboutWindow():  
    def __init__(self, arg):
        self.val = arg
        self.filewin = tkinter.Toplevel(self.val)
        text = tkinter.Text(self.filewin)
        text.insert(tkinter.INSERT,
"""\
Didacto 0.1.9\n
Un logiciel développé pour vous par Marco de Freitas.

\n
Dépôt du projet: https://gitlab.inubo.ch/glag/didacto
Documentation: https://didacto.readthedocs.io/fr/latest/

    Copyright (C) 2020  Marco de Freitas

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.



""")
        text.config(wrap=tkinter.WORD, state=tkinter.DISABLED, padx=10, pady=10)
        text.pack()
 

