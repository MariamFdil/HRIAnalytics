import pandas as pd
import sys

def load_and_extract(csv_path, output_path):

    df = pd.read_csv(csv_path)

    gaze_data = df[['gaze_angle_x', 'gaze_angle_y']]

    gaze_data.to_csv(output_path, index=False)
    print(f"Les données ont été sauvegardées dans {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py chemin_du_fichier.csv chemin_du_fichier_sortie.csv")
    else:
        csv_path = sys.argv[1]
        output_path = sys.argv[2]
        load_and_extract(csv_path, output_path)