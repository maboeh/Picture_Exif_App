from exif import Image
import os
import shutil
from datetime import datetime
import csv
import logging

class ApplicationLogic:
    MAX_FILES = 1000
    def __init__(self):
        pass

    def get_exif_date(self,image_path):
        """Diese Funktion liest das Datum aus den EXIF-Daten eines Bildes."""
        try:
            with open(image_path, 'rb') as img_file:
                img = Image(img_file)
                if img.has_exif and hasattr(img, 'datetime_original'):
                    datetime_str = img.datetime_original
                    return datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S')
        except (IOError, KeyError, AttributeError, ValueError) as e:
            logging.error(f"Fehler beim Lesen der EXIF-Daten für {image_path}: {e}")
        return None


    def getPicPaths(self,source_folder):
            # Liste aller Bildpfade im Verzeichnis erstellen
            images = [os.path.join(source_folder, i)
                           for i in os.listdir(source_folder) if i.lower().endswith(('.jpg', '.jpeg', '.png'))]

            if len(images) > self.MAX_FILES:
                raise ValueError(f"Zu viele Dateien im Quellordner. Das Limit liegt bei {self.MAX_FILES} Dateien.")

            # Extrahieren der EXIF-Datumsdaten und Sortieren der Liste!!
            images.sort(key=lambda x: self.get_exif_date(x) or datetime.min)
            return images


    def getPicPathsSub(self, source_folder):
        images = []
        for root, dirs, files in os.walk(source_folder):
            # Liste aller Bildpfade im Verzeichnis erstellen
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    images.append(os.path.join(root, file))
                if len(images) > self.MAX_FILES:
                    raise ValueError(f"Zu viele Dateien im Quellordner und den Unterordnern. Das Limit liegt bei {self.MAX_FILES} Dateien.")

            # Extrahieren der EXIF-Datumsdaten und Sortieren der Liste!!
        images.sort(key=lambda x: self.get_exif_date(x) or datetime.min)
        return images


    def writeCSV(self, csv_filepath, images):
        try:
            with open(csv_filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Image Path', 'Date'])

                image_data = {}
                for img_path in images:
                    date = self.get_exif_date(img_path)
                    date_str = date.strftime('%Y-%m-%d %H:%M:%S') if date else 'No Date'
                    writer.writerow([img_path, date_str])
                    image_data[img_path] = date_str
            logging.info("CSV-Datei wurde erstellt und Daten im Dictionary gespeichert.")
            return image_data
        except IOError as e:
            logging.error(f"Fehler beim Schreiben der CSV-Datei {csv_filepath}: {e}")
            return None

    def delete_subfolders(self, main_folder):
        # Überprüfen, ob der Pfad existiert
        if os.path.exists(main_folder):
            # Überprüfen, ob der Pfad zu einem Verzeichnis führt
            if os.path.isdir(main_folder):
                # Iterieren durch alle Unterverzeichnisse
                for subfolder in os.listdir(main_folder):
                    subfolder_path = os.path.join(main_folder, subfolder)
                    # Überprüfen, ob das Unterverzeichnis leer ist
                    if os.path.isdir(subfolder_path) and not os.listdir(subfolder_path):
                        try:
                            # Löschen des Unterverzeichnisses und aller darin enthaltenen Dateien
                            shutil.rmtree(subfolder_path)
                            logging.info(f"Das Unterverzeichnis {subfolder_path} wurde gelöscht.")
                        except OSError as e:
                            logging.error(f"Fehler beim Löschen des Unterverzeichnisses {subfolder_path}: {e}")
            else:
                logging.warning(f"{main_folder} ist kein Verzeichnis.")
        else:
            logging.warning(f"Der Pfad {main_folder} existiert nicht.")

    def moveImagesByExif(self, source_folder, images, target_folder=None, subCheck=False, deleteEmptyFolders=False):
        def is_image(file):
            return file.lower().endswith(('.jpg', '.jpeg', '.png'))

        def get_new_filename(date, img_path):
            return date.strftime('%Y-%m-%d_%H-%M-%S') + os.path.splitext(img_path)[1]

        def move_file(img_path, new_filepath):
            try:
                os.rename(img_path, new_filepath)
                logging.info(f"Bild umbenannt von {os.path.basename(img_path)} zu {os.path.basename(new_filepath)}")
            except OSError as e:
                logging.error(f"Fehler beim Umbenennen der Datei {img_path}: {e}")

        def move_file_without_date(img_path, root):
            without_folder = os.path.join(root, "without_Date")
            if not os.path.exists(without_folder):
                os.makedirs(without_folder)
            try:
                shutil.move(img_path, without_folder)
                logging.info(f"Datei {img_path} verschoben nach {without_folder}")
            except (OSError, shutil.Error) as e:
                logging.error(f"Fehler beim Verschieben der Datei {img_path}: {e}")

        for img_path in images:
            date = self.get_exif_date(img_path)
            if date:
                new_filename = get_new_filename(date, img_path)
                if target_folder:
                    relative_path = os.path.relpath(os.path.dirname(img_path), source_folder)
                    new_folder = os.path.join(target_folder, relative_path)
                    os.makedirs(new_folder, exist_ok=True)
                    new_filepath = os.path.join(new_folder, new_filename)
                else:
                    new_filepath = os.path.join(os.path.dirname(img_path), new_filename)
                move_file(img_path, new_filepath)
            else:
                logging.warning(f"Kein gültiges Datum gefunden für: {img_path}")
                move_root = target_folder if target_folder else os.path.dirname(img_path)
                move_file_without_date(img_path, move_root)

        if subCheck and target_folder and deleteEmptyFolders:
            self.delete_subfolders(source_folder)


