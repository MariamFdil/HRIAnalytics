import os
import pandas as pd
import argparse
from pathlib import Path

# Function to calculate the average processing time from a CSV file for GPT response
def calculate_average_gpt_response_time(csv_file_path):
    data = pd.read_csv(csv_file_path, header=None)  # Pas d'en-tête dans le fichier CSV
    # Extraction du temps de réponse avec regex
    processing_times = data[0].str.extract(r'Gpt response time : (\d+\.\d+) seconds')[0].astype(float)
    return processing_times.mean()

# General function to calculate the average processing time from a CSV file
def calculate_average_processing_time(csv_file_path):
    data = pd.read_csv(csv_file_path)
    return data['Processing Time (s)'].mean()

parser = argparse.ArgumentParser(description="Automate the analysis of processing times from CSV files.")
parser.add_argument('folder_path', type=str, help='The path to the folder containing the CSV files.')
args = parser.parse_args()

def automate_analysis(folder_path):
    folder_name = Path(folder_path).name
    results_filename = f"{folder_name}_results.txt"
    
    csv_files = {
        'Text To Speech': f"{folder_name}_tts",
        'Speech To Text': f"{folder_name}_stt",
        'GPT Response': f"{folder_name}_gptresponse",  
    }

    with open(os.path.join(folder_path, results_filename), 'w') as result_file:
        for key, filename in csv_files.items():
            try:
                full_path = os.path.join(folder_path, filename)
                if key == 'GPT Response':
                    average = calculate_average_gpt_response_time(full_path)
                else:
                    average = calculate_average_processing_time(full_path)
                result_file.write(f"Moyenne de temps de réponse pour {key}: {average} secondes\n")
            except FileNotFoundError:
                result_file.write(f"Le fichier {filename} n'a pas été trouvé dans {folder_path}.\n")
            except KeyError:
                result_file.write(f"La colonne 'Processing Time (s)' n'existe pas dans {filename}.\n")
            except Exception as e:
                result_file.write(f"Une erreur est survenue lors de l'analyse de {filename}: {e}\n")

# Running the analysis function
if __name__ == '__main__':
    automate_analysis(args.folder_path)
