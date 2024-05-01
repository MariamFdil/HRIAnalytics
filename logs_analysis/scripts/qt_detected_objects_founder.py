import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import pandas as pd
import os

class ImageReviewer(QWidget):
    def __init__(self, source_folder, csv_path):
        super().__init__()
        self.source_folder = source_folder
        self.current_index = 0
        self.load_data(csv_path)
        self.init_ui()
    
    def load_data(self, csv_path):
        self.data = pd.read_csv(csv_path)
        self.images = os.listdir(self.source_folder)
        self.images.sort()

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
        if self.current_index < len(self.images):
            pixmap = QPixmap(os.path.join(self.source_folder, self.images[self.current_index]))
            self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
        else:
            QMessageBox.information(self, 'End', 'No more images to review.')
            self.close()

    def update_csv_data(self):
        if self.current_index < len(self.data):
            self.csv_label.setText(str(self.data.iloc[self.current_index]))

    def update_progress(self):
        self.progress_label.setText(f"Progress: {self.current_index + 1}/{len(self.images)}")

    def yes(self):
        self.record_response('yes')
        self.next_image()

    def no(self):
        self.record_response('no')
        self.next_image()

    def record_response(self, response):
        if self.current_index == 0:
            with open('responses.csv', 'w') as file:
                file.write('Perception,Detection Time,Evaluation\n')
        with open('responses.csv', 'a') as file:
            perception = self.data.iloc[self.current_index]['Perception']
            detection_time = self.data.iloc[self.current_index]['Detection Time (s)']
            file.write(f"{perception}, {detection_time}, {response}\n")

    def next_image(self):
        self.current_index += 1
        if self.current_index < len(self.images):
            self.update_image()
            self.update_csv_data()
            self.update_progress()
        else:
            QMessageBox.information(self, 'End', 'No more images to review.')
            self.close()

# Main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageReviewer('/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/results', '/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/perceptions')
    sys.exit(app.exec_())
