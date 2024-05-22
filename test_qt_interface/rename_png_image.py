import os
import re
import shutil
from datetime import datetime
import uuid  # Pour générer un identifiant unique

def convert_and_copy_images(source_folder, output_folder):
    # Assurer que le dossier de sortie existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Préparer une expression régulière pour extraire les timestamps, avec ou sans décimales
    regex = re.compile(r'frame-(\d+(\.\d+)?).png')

    # Compteur pour suivre le nombre de fichiers traités
    files_processed = 0

    # Parcourir le dossier source
    for filename in os.listdir(source_folder):
        match = regex.match(filename)
        if match:
            # Utiliser seulement la partie entière du timestamp pour la conversion
            timestamp = int(float(match.group(1)))
            # Convertir le timestamp en date et heure
            date_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')
            # Générer un identifiant unique pour éviter les doublons
            unique_id = uuid.uuid4().hex[:6]  # Génère une chaîne hexadécimale de 6 caractères
            new_filename = f'frame-{date_time}_{unique_id}.png'
            # Chemin du fichier source et destination
            src_path = os.path.join(source_folder, filename)
            dest_path = os.path.join(output_folder, new_filename)
            # Copier le fichier avec le nouveau nom
            shutil.copy(src_path, dest_path)
            files_processed += 1
            print(f"Copied {filename} to {new_filename}")
    
    print(f"Total files processed: {files_processed}")
    if files_processed == 0:
        print("No matching files found. Check the regular expression and the folder content.")

source_folder = '/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/interactive_chatbot_2024-04-30-11-26-07'
output_folder = '/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/results'

# Appel de la fonction
convert_and_copy_images(source_folder, output_folder)
