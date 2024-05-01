from exif import Image
import os
import shutil
from datetime import datetime
import csv

class ApplicationLogic:

    images = []
    image_data = {}



        # image_folder = "/Users/maboeh/Library/Mobile Documents/com~apple~CloudDocs/Bilder und Videos"
        #image_folder = "/Users/maboeh/bilder_test"
        #csv_file_path = "/Users/maboeh/bilder_test/image_data.csv"

        #destination_folder = "/Users/maboeh/bilder_test/ohne_Datum"


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
        images = [os.path.join(source_folder, i)
                for i in os.listdir(source_folder) if i.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # Extrahieren der EXIF-Datumsdaten und Sortieren der Liste!!
        images.sort(key=lambda x: self.get_exif_date(x) or datetime.min)


    def writeCSV(self,csv_filepath):
        with open(csv_filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Image Path', 'Date'])

            for img_path in self.images:
                date = self.get_exif_date(img_path)
                date_str = date.strftime('%Y-%m-%d %H:%M:%S') if date else 'No Date'
                writer.writerow([img_path, date_str])
                # Dictionary erzeugen - key in KLammern und den Wert zuweisen
                self.image_data[img_path] = date_str

        print("CSV-Datei wurde erstellt und Daten im Dictionary gespeichert.")

    def copyImages(self,target_folder,source_folder):
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(root, file)
                    date = self.get_exif_date(img_path)
                    if date:
                        # Erstellen eines neuen Dateinamens basierend auf dem Datum
                        new_filename = date.strftime('%Y-%m-%d_%H-%M-%S') + os.path.splitext(img_path)[1]
                        new_filepath = os.path.join(root, new_filename)

                        # Umbenennen des Bildes
                        os.rename(img_path, new_filepath)
                        print(f"Bild umbenannt von {os.path.basename(img_path)} zu {new_filename}")
                    else:
                        print(f"Kein gültiges Datum gefunden für: {img_path}")
                        if not os.path.exists(target_folder):
                            os.makedirs(target_folder)
                        shutil.move(img_path, target_folder + "/ohneDatum")
                        print(f"Datei {img_path} verschoben nach {target_folder}")


