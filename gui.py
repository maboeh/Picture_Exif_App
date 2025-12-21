import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
import os
from tkinter import filedialog
import logging


class Gui:
        # Konfigurieren Sie das Logging, um Informationen in eine Datei zu schreiben
        logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)

        # Verwenden Sie logging.info(), um Informationen zu protokollieren
        logging.info('Start der Anwendung')

        def __init__(self,root,logic):
                self.root = root
                self.logic = logic
                # Erstellen der BooleanVar und Hinzufügen von Beobachtern
                self.sourceCheck_var = tk.BooleanVar()
                self.sourceCheck_var.trace('w', self.log_variable_change)
                self.targetCheck_var = tk.BooleanVar()
                self.targetCheck_var.trace('w', self.log_variable_change)
                self.create_widgets()


        def create_widgets(self):
                #Quellenblock
                self.sourceLabel = ttk.Label(self.root, text="Sourcefolder")
                self.sourceLabel.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
                self.sourceEntry = ttk.Entry(self.root)
                self.sourceEntry.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
                self.sourceBrowse = ttk.Button(self.root, text="Browse", command=self.browseSource)
                self.sourceBrowse.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)

                self.sourceCheck = ttk.Checkbutton(self.root, text="include Subfolders", variable=self.sourceCheck_var)
                self.sourceCheck.grid(row=2, column=2, sticky="w", pady=10)


                #Dropdown
                self.optionDrop = ttk.Combobox(self.root, values=["Date and Time", "Author", "Place"])
                self.optionDrop.current(0)
                self.optionDrop.grid(row=4, column=1, sticky="nsew", padx=10)


                #Zielblock
                self.targetLabel = ttk.Label(self.root, text="Targetfolder")
                self.targetLabel.grid(row=6, column=1, sticky="nsew", padx=10, pady=10)
                self.targetEntry = ttk.Entry(self.root)
                self.targetEntry.grid(row=6, column=2, sticky="nsew", padx=10, pady=10)
                self.targetBrowse = ttk.Button(self.root, text="Browse",command=self.browseTarget)
                self.targetBrowse.grid(row=6, column=3, sticky="nsew", padx=10, pady=10)

                self.targetCheck = ttk.Checkbutton(self.root, text="generate CSV-file", variable=self.targetCheck_var)
                self.targetCheck.grid(row=7, column=2, sticky="w", pady=10)



                #Textausgabe
                self.textWidget = ttk.ScrolledText(self.root, height=5, width=50)
                self.textWidget.grid(row=8, column=1, columnspan=5, sticky="nsew", padx=10, pady=10)

                #Submit
                self.submitButton = ttk.Button(self.root, text="Submit", command=self.submit)
                self.submitButton.grid(row=9, column=1,columnspan=3, sticky="nsew", padx=10, pady=10)

        def browseTarget(self):
                filepath = filedialog.askdirectory()
                if filepath:
                        self.targetEntry.delete(0, END)
                        self.targetEntry.insert(0, filepath)

        def browseSource(self):
                filepath = filedialog.askdirectory()
                if filepath:
                        self.sourceEntry.delete(0, END)
                        self.sourceEntry.insert(0, filepath)

        def log_variable_change(self, *args):
                logging.info(
                        f'Änderung erkannt: sourceCheck_var = {self.sourceCheck_var.get()}, targetCheck_var = {self.targetCheck_var.get()}')

        def submit(self):
                logging.info('Submit-Methode aufgerufen')
                source_folder = self.sourceEntry.get()
                target_folder = self.targetEntry.get()
                logging.info(f'Source folder: {source_folder}, Target folder: {target_folder}')
                logging.info(f'Wert von sourceCheck_var: {self.sourceCheck_var.get()}')
                logging.info(f'Wert von targetCheck_var: {self.targetCheck_var.get()}')

                if self.sourceCheck_var.get():
                        logging.info('Die if-Schleife für sourceCheck_var.get() wurde ausgeführt')
                        self.logic.getPicPathsSub(source_folder)
                        if target_folder:
                                logging.info('Die if-Schleife für target_folder wurde ausgeführt')
                                self.logic.copyImages(source_folder,target_folder,  subCheck=True)
                        else:
                                self.logic.copyImages(source_folder, subCheck=True)
                elif not self.sourceCheck_var.get():
                        self.logic.getPicPaths(source_folder)
                        if target_folder:
                                self.logic.copyImages(source_folder,target_folder,  subCheck=False)
                        else:
                                self.logic.copyImages(source_folder, subCheck=False)

                if self.targetCheck_var.get():
                        logging.info('Die if-Schleife für targetCheck_var.get() wurde ausgeführt')
                        csv_filepath = os.path.join(target_folder if target_folder else source_folder, "data.csv")
                        if self.sourceCheck_var.get():
                                self.logic.writeCSVSub(csv_filepath, target_folder if target_folder else source_folder)
                        else:
                                self.logic.writeCSV(csv_filepath, source_folder)
































