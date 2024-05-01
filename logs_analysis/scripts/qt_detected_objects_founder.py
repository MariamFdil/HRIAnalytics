import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import pandas as pd
import os

class ImageReviewer(QWidget):
    def __init__(self, source_folder, csv_path):
        super().__init__()
        self.source_folder = source_folder
        self.csv_path = csv_path
        self.current_index = 0
        self.load_data()
        self.init_ui()

    def extract_timestamp(self, filename):
        base = os.path.basename(filename)
        timestamp_str, timestamp_frac = base.split('-')[1].rstrip('.png').split('.')
        complete_timestamp = float(timestamp_str) + float('0.' + timestamp_frac)
        return complete_timestamp

    def load_data(self):
        self.data = pd.read_csv(self.csv_path)
        self.data.reset_index(drop=True, inplace=True)
        self.matched_images = []
        
        for image_file in os.listdir(self.source_folder):
            if image_file.endswith('.png'):
                image_timestamp = self.extract_timestamp(image_file)
                mask = (self.data['Timestamp (s)'] >= image_timestamp - 2) & (self.data['Timestamp (s)'] <= image_timestamp + 2)
                if self.data[mask].any(axis=None):
                    self.matched_images.append(image_file)

        self.matched_images.sort()

    def init_ui(self):
        # Layout
        vbox = QVBoxLayout()

        # Image display
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)  # Allow image to scale with label size
        self.update_image()

        # CSV data display
        self.csv_label = QLabel(self)
        self.update_csv_data()

        # Progress Label
        self.progress_label = QLabel(self)
        self.update_progress()

        # Buttons
        yes_button = QPushButton('Yes', self)
        yes_button.clicked.connect(self.yes)
        no_button = QPushButton('No', self)
        no_button.clicked.connect(self.no)

        # Add widgets to layout
        vbox.addWidget(self.image_label, 1)  # Image label has a higher stretch factor
        vbox.addWidget(self.csv_label)
        vbox.addWidget(self.progress_label)
        vbox.addWidget(yes_button)
        vbox.addWidget(no_button)

        self.setLayout(vbox)

        # Set initial window size
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Image Reviewer')
        self.show()

    def update_image(self):
        if self.current_index < len(self.matched_images):
            image_path = os.path.join(self.source_folder, self.matched_images[self.current_index])
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap)
        else:
            QMessageBox.information(self, 'End', 'No more images to review.')
            self.close()

    def update_csv_data(self):
        if self.current_index < len(self.matched_images):
            image_file = self.matched_images[self.current_index]
            image_timestamp = self.extract_timestamp(image_file)
            # Trouver la ligne de données correspondante en utilisant une tolérance de 2 secondes
            mask = (self.data['Timestamp (s)'] >= image_timestamp - 2) & (self.data['Timestamp (s)'] <= image_timestamp + 2)
            if any(mask):
                # Obtenir la première ligne correspondante pour l'image actuelle
                matching_row = self.data.loc[mask].iloc[0]
                self.csv_label.setText(str(matching_row))
            else:
                self.csv_label.setText("No matching CSV data found.")


    def update_progress(self):
        self.progress_label.setText(f"Progress: {self.current_index + 1}/{len(self.matched_images)}")

    
    def yes(self):
        self.record_response('yes')
        self.next_image()

    def no(self):
        self.record_response('no')
        self.next_image()
    
    def record_response(self, response):
        if self.current_index < len(self.matched_images):
            image_file = self.matched_images[self.current_index]
            image_timestamp = self.extract_timestamp(image_file)
            # Trouver la ligne de données correspondante en utilisant une tolérance de 2 secondes
            mask = (self.data['Timestamp (s)'] >= image_timestamp - 2) & (self.data['Timestamp (s)'] <= image_timestamp + 2)
            if any(mask):
                # Obtenir la première ligne correspondante pour l'image actuelle
                matching_row = self.data.loc[mask].iloc[0]
                # Préparer la ligne avec les colonnes spécifiées
                output_row = pd.DataFrame({
                    'Perception': [matching_row['Perception']],
                    'is_visible': [matching_row['is_visible']],
                    'Timestamp (s)': [matching_row['Timestamp (s)']],
                    'Evaluation': [response]
                })
                # Écrire ou ajouter la ligne dans le fichier CSV de réponse
                with open('responses.csv', 'a') as file:
                    output_row.to_csv(file, header=file.tell()==0, index=False)
            else:
                print("No matching CSV data found, unable to record response.")



    def next_image(self):
        self.current_index += 1
        if self.current_index < len(self.matched_images):
            self.update_image()
            self.update_csv_data()
            self.update_progress()
        else:
            QMessageBox.information(self, 'End', 'No more images to review.')
            self.close()




# Main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageReviewer('/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/results/matching_pairs', '/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/perceptions')
    sys.exit(app.exec_())
