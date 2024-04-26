import pandas as pd
import sys

def calculate_gaze_percentage(csv_path):
    """
    Calculate the percentage of time a person is looking directly at the camera.
    
    Parameters:
        csv_path (str): The path to the CSV file containing gaze angle data.
    """
    # Load the CSV file
    data = pd.read_csv(csv_path)
   # data = pd.read_csv(csv_path, encoding='ISO-8859-1')

    # Define thresholds for looking directly ahead
    horizontal_threshold = 0.05  # in radians
    vertical_threshold = 0.25    # in radians

    # Calculate moments when the person is looking directly ahead
    looking_directly_ahead = (abs(data['gaze_angle_x']) < horizontal_threshold) & (abs(data['gaze_angle_y']) < vertical_threshold)

    # Calculate the percentage of time looked directly ahead
    percentage_directly_ahead = 100 * looking_directly_ahead.mean()

    print(f"Percentage of time looking directly ahead: {percentage_directly_ahead:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_csv_file>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    calculate_gaze_percentage(csv_file_path)
