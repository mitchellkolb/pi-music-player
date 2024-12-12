

import automation
import os


import sys
import requests
from PyQt6.QtCore import QSize, QRect, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage



class ImageViewer(QWidget):
    def __init__(self, image_url):
        super().__init__()

        self.setWindowTitle("Image Viewer")

        # Create a label to display the image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Load the image
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = response.content
                image = QImage()
                if image.loadFromData(image_data):
                    pixmap = QPixmap.fromImage(image)
                    self.image_label.setPixmap(pixmap)
                else:
                    self.image_label.setText("Failed to load image")
            else:
                self.image_label.setText(f"Error downloading image: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.image_label.setText(f"Error: {e}")

        # Create a button to close the app
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)

        # Create a layout and add the widgets
        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        layout.addWidget(self.close_button)

def guiTest(imageURL: str):
    app = QApplication(sys.argv)
    viewer = ImageViewer(imageURL)
    viewer.show()
    app.exec()




def main():

    os.system('clear')
    myautomation = automation.MusicAutomation("http://pianostream.com/")    

    while True:
        print("\nMain Menu")
        print("1) Launch Browser")
        print("2) Play/Pause")
        print("3) Thumbs UP Click")
        print("4) Thumbs DOWN Click")
        print("5) Run GUI for Info Test")
        print("6) Show Song Info")
        print("7) Mute")
        print("8) Volume Slider")
        print("9) Exit")

        try:
            choice = int(input("Select an option (1-9): "))

            if choice == 1:
                myautomation.loadCredentails()
                myautomation.startBrowser()
                myautomation.login()
            elif choice == 2:
                myautomation.clickPlayPause()
            elif choice == 3:
                myautomation.clickThumbsUp()
            elif choice == 4:
                myautomation.clickThumbsDown()
            elif choice == 5:
                imageURL = myautomation.getAlbumArtUrl()
                guiTest(imageURL)
            elif choice == 6:
                myautomation.getSongTitle()
                myautomation.getSongArtist()
                myautomation.getAlbumTitle()
            elif choice == 7:
                myautomation.clickMute()
            elif choice == 8:
                new = input("Enter Volume Num: ")
                myautomation.volumeSlider(int(new))
            elif choice == 9:
                myautomation.close()
                print("Completed myautomation")
                break
            else:
                print("Invalid selection. Please choose a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()
