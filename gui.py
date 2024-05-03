import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
import os
from tkinter import filedialog


class Gui:
        def __init__(self,root,logic):
                self.root = root
                self.logic = logic
                # Erstellen der BooleanVar
                self.check_var = tk.BooleanVar()
                self.create_widgets()


        def create_widgets(self):
                #Quellenblock
                self.sourceLabel = ttk.Label(self.root, text="Sourcefolder")
                self.sourceLabel.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
                self.sourceEntry = ttk.Entry(self.root)
                self.sourceEntry.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
                self.sourceBrowse = ttk.Button(self.root, text="Browse", command=self.browseSource)
                self.sourceBrowse.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)
                self.sourceCheck = tk.Checkbutton(self.root, variable=self.check_var)
                self.sourceCheck.grid(row=2, column=1, sticky="e", pady=10)
                self.checkLabel = ttk.Label(self.root, text="include Subfolders" )
                self.checkLabel.grid(row=2, column=2, sticky="w", pady=10)

                #Zielblock
                self.targetLabel = ttk.Label(self.root, text="Sourcefolder")
                self.targetLabel.grid(row=4, column=1, sticky="nsew", padx=10, pady=10)
                self.targetEntry = ttk.Entry(self.root)
                self.targetEntry.grid(row=4, column=2, sticky="nsew", padx=10, pady=10)
                self.targetBrowse = ttk.Button(self.root, text="Browse",command=self.browseTarget)
                self.targetBrowse.grid(row=4, column=3, sticky="nsew", padx=10, pady=10)

                #Dropdown
                self.optionDrop = ttk.Combobox(self.root, values=["copy", "move"])
                self.optionDrop.current(0)
                self.optionDrop.grid(row=5, column=1, sticky="nsew", padx=10)


                #Textausgabe
                self.textWidget = ttk.ScrolledText(self.root, height=5, width=50)
                self.textWidget.grid(row=6, column=1, columnspan=5, sticky="nsew", padx=10, pady=10)

                #Submit
                self.submitButton = ttk.Button(self.root, text="Submit", command=self.submit)
                self.submitButton.grid(row=7, column=1,columnspan=3, sticky="nsew", padx=10, pady=10)

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



        def submit(self):
                source_folder = self.sourceEntry.get()
                self.logic.getPicPaths(source_folder)

                #if self.check_var.get():



                target_folder = self.targetEntry.get()
                self.logic.copyImages(target_folder,source_folder)


                csv_filepath = os.path.join(target_folder, "data.csv")
                self.logic.writeCSV(csv_filepath)











