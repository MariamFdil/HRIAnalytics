import pandas as pd
import sys

def analyze_gaze_data(file_path, output_stats_path):
    """
    Reads a CSV file with gaze angles and writes descriptive statistics to a CSV file.

    Parameters:
    - file_path: str, path to the input CSV file containing gaze angles.
    - output_stats_path: str, path to the output CSV file where the statistics will be saved.
    """
    try:
        # Load the CSV file into a DataFrame
        data = pd.read_csv(file_path)

        # Calculate descriptive statistics
        stats = data.describe()

        # Write the descriptive statistics to a CSV file
        stats.to_csv(output_stats_path)
        print(f"Descriptive statistics written to {output_stats_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file_path> <output_stats_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    output_stats_path = sys.argv[2]
    analyze_gaze_data(file_path, output_stats_path)
