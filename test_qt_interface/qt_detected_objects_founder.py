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
        self.load_data()
        self.current_index = 0
        self.current_image_index = 0
        self.init_ui()

    def extract_timestamp(self, filename):
        base = os.path.basename(filename)
        timestamp_str, timestamp_frac = base.split('-')[1].rstrip('.png').split('.')
        complete_timestamp = float(timestamp_str) + float('0.' + timestamp_frac)
        return complete_timestamp

    def load_data(self):
        self.data = pd.read_csv(self.csv_path)
        self.data.reset_index(drop=True, inplace=True)
        self.matched_images = {index: [] for index in self.data.index}

        for image_file in os.listdir(self.source_folder):
            if image_file.endswith('.png'):
                image_timestamp = self.extract_timestamp(image_file)
                # Assign the image to the closest CSV entry within a 2-second tolerance
                for index, row in self.data.iterrows():
                    if abs(image_timestamp - row['Timestamp (s)']) <= 0.1:
                        self.matched_images[index].append(image_file)

    def init_ui(self):
        self.setWindowTitle('Image Reviewer')
        self.setGeometry(100, 100, 800, 600)
        vbox = QVBoxLayout(self)

        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)
        vbox.addWidget(self.image_label, 1)

        self.csv_label = QLabel(self)
        vbox.addWidget(self.csv_label)

        self.progress_label = QLabel(self)
        vbox.addWidget(self.progress_label)

        yes_button = QPushButton('VP', self)
        yes_button.clicked.connect(lambda: self.record_response('VP'))
        vbox.addWidget(yes_button)

        no_button = QPushButton('FP', self)
        no_button.clicked.connect(lambda: self.record_response('FP'))
        vbox.addWidget(no_button)

        self.show()
        self.update_view()

    def update_view(self):
        self.update_image()
        self.update_csv_data()
        self.update_progress()

    def update_image(self):
        images = self.matched_images[self.current_index]
        if self.current_image_index < len(images):
            image_path = os.path.join(self.source_folder, images[self.current_image_index])
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap)

    def update_csv_data(self):
        self.csv_label.setText(str(self.data.iloc[self.current_index]))

    def update_progress(self):
        self.progress_label.setText(f"Progress: {self.current_index + 1}/{len(self.data)}, Image: {self.current_image_index + 1}/{len(self.matched_images[self.current_index])}")

    def record_response(self, response):
        # Append response to a CSV file
        row = self.data.iloc[self.current_index]
        output_row = pd.DataFrame({
            'Timestamp': [row['Timestamp (s)']],
            'Object Name': [row['Perception']], 
            'Evaluation': [response]
        })
        with open('/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/results/confusion_matrix/confusion_matrix.csv', 'a') as file:
            output_row.to_csv(file, header=file.tell() == 0, index=False)
        self.next_image()

    def next_image(self):
        self.current_image_index += 1
        if self.current_image_index >= len(self.matched_images[self.current_index]):
            self.current_index += 1
            self.current_image_index = 0
        if self.current_index < len(self.data):
            self.update_view()
        else:
            QMessageBox.information(self, 'End', 'No more images to review.')
            self.close()

# Main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageReviewer('/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/results/matching_pairs', '/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/filtred_perceptions.csv')
    sys.exit(app.exec_())
