from exif import Image
import os
import shutil
from datetime import datetime
import csv

class ApplicationLogic:

    images = []
    image_data = {}



    def get_exif_date(self,image_path):
        """Diese Funktion liest das Datum aus den EXIF-Daten eines Bildes."""
        try:
            with open(image_path, 'rb') as img_file:
                img = Image(img_file)
                if img.has_exif:
                    datetime_str = img.datetime_original
                    return datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S')
        except Exception as e:
            print(f"Fehler beim Lesen der EXIF-Daten für {image_path}: {e}")
        return None


    def getPicPaths(self,source_folder):
            # Liste aller Bildpfade im Verzeichnis erstellen
            self.images = [os.path.join(source_folder, i)
                           for i in os.listdir(source_folder) if i.lower().endswith(('.jpg', '.jpeg', '.png'))]

            # Extrahieren der EXIF-Datumsdaten und Sortieren der Liste!!
            self.images.sort(key=lambda x: self.get_exif_date(x) or datetime.min)


    def getPicPathsSub(self, source_folder):
        self.images = []
        for root, dirs, files in os.walk(source_folder):
            # Liste aller Bildpfade im Verzeichnis erstellen
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    self.images.append(os.path.join(root, file))

            # Extrahieren der EXIF-Datumsdaten und Sortieren der Liste!!
        self.images.sort(key=lambda x: self.get_exif_date(x) or datetime.min)


    def writeCSVSub(self,csv_filepath,source_folder):
        self.getPicPathsSub(source_folder)
        with open(csv_filepath, 'w', newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Image Path', 'Date'])

            for img_path in self.images:
                date = self.get_exif_date(img_path)
                date_str = date.strftime('%Y-%m-%d %H:%M:%S') if date else 'No Date'
                writer.writerow([img_path, date_str])
                # Dictionary erzeugen - key in KLammern und den Wert zuweisen
                self.image_data[img_path] = date_str

        print("CSV-Datei wurde erstellt und Daten im Dictionary gespeichert.")



    def writeCSV(self,csv_filepath,source_folder):

        self.getPicPaths(source_folder)

        with open(csv_filepath, 'w', newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Image Path', 'Date'])

            for img_path in self.images:
                date = self.get_exif_date(img_path)
                date_str = date.strftime('%Y-%m-%d %H:%M:%S') if date else 'No Date'
                writer.writerow([img_path, date_str])
                # Dictionary erzeugen - key in KLammern und den Wert zuweisen
                self.image_data[img_path] = date_str

        print("CSV-Datei wurde erstellt und Daten im Dictionary gespeichert.")



    def delete_subfolder(self,path):
        # Überprüfen, ob der Pfad existiert
        if os.path.exists(path):
            # Überprüfen, ob der Pfad zu einem Verzeichnis führt
            if os.path.isdir(path):
                # Löschen des Verzeichnisses und aller darin enthaltenen Dateien
                shutil.rmtree(path)
                print(f"Das Verzeichnis {path} wurde gelöscht.")
            else:
                print(f"{path} ist kein Verzeichnis.")
        else:
            print(f"Der Pfad {path} existiert nicht.")



    def copyImages(self, source_folder, target_folder=None, subCheck=False):
        def is_image(file):
            return file.lower().endswith(('.jpg', '.jpeg', '.png'))

        def get_new_filename(date, img_path):
            return date.strftime('%Y-%m-%d_%H-%M-%S') + os.path.splitext(img_path)[1]

        def move_file_without_date(img_path, root):
            withoutFolder = os.path.join(root, "without_Date")
            if not os.path.exists(withoutFolder):
                os.makedirs(withoutFolder)
            shutil.move(img_path, withoutFolder)
            print(f"Datei {img_path} verschoben nach {withoutFolder}")

        if subCheck and target_folder:
            for root, dirs, files in os.walk(source_folder):  # inkludiert subfolders
                for file in files:  # geht durch jedes file
                    if is_image(file):  # setzt die namen auf lowercase und nimmt nur bestimmte endungen
                        img_path = os.path.join(root,
                                                file)  # setzt einen pfad aus dem root verzeichnigs und dem filenamen zusammen
                        date = self.get_exif_date(
                            img_path)  # öffnet diesen oben erzeugten pfad und liest das exif datum aus
                        if date:  # falls ein Datum existiert
                            # Erstellen eines neuen Dateinamens basierend auf dem Datum
                            new_filename = get_new_filename(date,
                                                            img_path)  # erzeugt einen neuen Dateinnamen aus dem Datum und der Dateiendung ais img_path vrher
                            relative_path = os.path.relpath(root, source_folder)
                            old_path = os.path.join(source_folder, relative_path)
                            new_folder = os.path.join(target_folder, relative_path)
                            os.makedirs(new_folder, exist_ok=True)
                            new_filepath = os.path.join(new_folder,
                                                        new_filename)  # macht aus dem root verzeichnis und dem neuen dateinmaen mit dem datum einen pfad

                            # Umbenennen des Bildes
                            os.rename(img_path, new_filepath)  # benennt die alte datei in die neue um
                            print(f"Bild umbenannt von {os.path.basename(img_path)} zu {new_filename}")
                        else:
                            print(f"Kein gültiges Datum gefunden für: {img_path}")
                            move_file_without_date(img_path, target_folder)
            self.delete_subfolder(old_path)

        elif subCheck and not target_folder:
            for root, dirs, files in os.walk(source_folder):  # inkludiert subfolders
                for file in files:  # geht durch jedes file
                    if is_image(file):  # setzt die namen auf lowercase und nimmt nur bestimmte endungen
                        img_path = os.path.join(root,
                                                file)  # setzt einen pfad aus dem root verzeichnigs und dem filenamen zusammen
                        date = self.get_exif_date(
                            img_path)  # öffnet diesen oben erzeugten pfad und liest das exif datum aus
                        if date:  # falls ein Datum existiert
                            # Erstellen eines neuen Dateinamens basierend auf dem Datum
                            new_filename = get_new_filename(date,
                                                            img_path)  # erzeugt einen neuen Dateinnamen aus dem Datum und der Dateiendung ais img_path vrher
                            new_filepath = os.path.join(root,
                                                        new_filename)  # macht aus dem root verzeichnis und dem neuen dateinmaen mit dem datum einen pfad

                            # Umbenennen des Bildes
                            os.rename(img_path, new_filepath)  # benennt die alte datei in die neue um
                            print(f"Bild umbenannt von {os.path.basename(img_path)} zu {new_filename}")
                        else:
                            print(f"Kein gültiges Datum gefunden für: {img_path}")
                            move_file_without_date(img_path, root)

        elif not subCheck and target_folder:
            root = source_folder
            for file in os.listdir(source_folder):
                if is_image(file):
                    img_path = os.path.join(source_folder, file)
                    date = self.get_exif_date(img_path)
                    if date:
                        new_filename = get_new_filename(date, img_path)
                        relative_path = os.path.relpath(root, source_folder)
                        new_folder = os.path.join(target_folder, relative_path)
                        os.makedirs(new_folder, exist_ok=True)
                        new_filepath = os.path.join(new_folder, new_filename)

                        os.rename(img_path, new_filepath)
                        print(f"Bild umbenannt von {os.path.basename(img_path)} zu {new_filename}")
                    else:
                        print(f"Kein gültiges Datum gefunden für: {img_path}")
                        move_file_without_date(img_path, target_folder)

        elif not subCheck and not target_folder:
            root = source_folder
            for file in os.listdir(source_folder):
                if is_image(file):
                    img_path = os.path.join(source_folder, file)
                    date = self.get_exif_date(img_path)
                    if date:
                        new_filename = get_new_filename(date, img_path)
                        new_filepath = os.path.join(source_folder, new_filename)

                        os.rename(img_path, new_filepath)
                        print(f"Bild umbenannt von {os.path.basename(img_path)} zu {new_filename}")
                    else:
                        print(f"Kein gültiges Datum gefunden für: {img_path}")
                        move_file_without_date(img_path, source_folder)







    def moveImages(self,target_folder,source_folder,subCheck=False):
        pass


