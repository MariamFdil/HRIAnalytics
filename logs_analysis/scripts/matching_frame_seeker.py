import pandas as pd
import os
import shutil

# Chemin vers le fichier CSV et le dossier des images
csv_path = '/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/perceptions'
images_path = '/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/interactive_chatbot_2024-04-30-11-26-07'
output_path = '/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/results/matching_pairs'

# Assurez-vous que le dossier de sortie existe
os.makedirs(output_path, exist_ok=True)

# Lire le fichier CSV
df = pd.read_csv(csv_path)

# Fonction pour extraire le timestamp d'un nom de fichier
def extract_timestamp(filename):
    base = os.path.basename(filename)
    timestamp_str, timestamp_frac = base.split('-')[1].rstrip('.png').split('.')
    complete_timestamp = float(timestamp_str) + float('0.' + timestamp_frac)
    return complete_timestamp

# Copier les images correspondantes
for image_file in os.listdir(images_path):
    if image_file.endswith('.png'):
        image_timestamp = extract_timestamp(image_file)
        print(f"Checking image: {image_file} with timestamp: {image_timestamp}")
        # Vérifier si un timestamp dans le CSV correspond à +/- 2 secondes
        mask = (df['Timestamp (s)'] >= image_timestamp - 2) & \
               (df['Timestamp (s)'] <= image_timestamp + 2)
        if df[mask].any(axis=None):
            shutil.copy(os.path.join(images_path, image_file), output_path)
            print(f"Image {image_file} copied to {output_path}")
        else:
            print(f"No matching timestamp found for {image_file}")