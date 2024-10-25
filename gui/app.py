

#Code from tutorial. https://youtu.be/wdEpWCFf40U?si=OodxvwZWVYtBb2OD

import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QUrl, QTimer, QFile, QTextStream
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


class AudioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.eventHandler()
        self.loadStyle()  # Load the CSS after setting up the UI

    def loadStyle(self):
        css_path = os.path.join(os.path.dirname(__file__), 'style.css')
        css_file = QFile(css_path)
        if css_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(css_file)
            self.setStyleSheet(stream.readAll())
            css_file.close()
        else:
            print(f"Error: Cannot open {css_path}")



    # Settings portion
    def settings(self):
        self.setWindowTitle("Audio-Adjuster") # Title of the window that the OS sees 
        self.setGeometry(500, 700, 600, 300) # Where on the screen does it appear
        #self.resize(600, 300) # Size of the indow when it appears

    # Desing of the UI
    def initUI(self):
        self.title = QLabel("Audio Adjuster")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileTitle = QListWidget()
        self.btnOpener = QPushButton("Choose a File")
        self.btnPlay = QPushButton("Play")
        self.btnPause = QPushButton("Pause")
        self.btnReset = QPushButton("Reset")
        self.btnResume = QPushButton("Resume")

        #Deactivate button for now
        self.btnPause.setDisabled(True)
        self.btnReset.setDisabled(True)
        self.btnResume.setDisabled(True)


        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(50)
        self.slider.setMaximum(150)
        self.slider.setValue(100) #Playback speed
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(10)

        self.sliderText = QLabel("Speed: 100x")
        self.sliderText.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sliderLayout = QHBoxLayout()
        sliderLayout.addWidget(self.sliderText)
        sliderLayout.addWidget(self.slider)

        #Create a layout
        self.mainLayout = QVBoxLayout()
        row = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        self.mainLayout.addWidget(self.title)
        self.mainLayout.addLayout(sliderLayout)

        col1.addWidget(self.fileTitle)
        col2.addWidget(self.btnOpener)
        col2.addWidget(self.btnPlay)
        col2.addWidget(self.btnPause)
        col2.addWidget(self.btnResume)
        col2.addWidget(self.btnReset)

        row.addLayout(col1, 2)
        row.addLayout(col2, 4)

        self.mainLayout.addLayout(row)
        self.setLayout(self.mainLayout)

        self.style()

        # Audio classes from pyqt
        self.audioOutput = QAudioOutput()
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setAudioOutput(self.audioOutput)



    # Event Handler
    def eventHandler(self):
        self.slider.valueChanged.connect(self.updateSlider)
        self.btnOpener.clicked.connect(self.openFile)
        self.btnPlay.clicked.connect(self.playAudio)
        self.btnPause.clicked.connect(self.pauseAudio)
        self.btnResume.clicked.connect(self.resumeAudio)
        self.btnReset.clicked.connect(self.resetAudio)
        self.fileTitle.itemSelectionChanged.connect(self.enablePlayButton)

    def enablePlayButton(self):
        # Enable the play button if there is an item selected
        if self.fileTitle.selectedItems():
            self.btnPlay.setEnabled(True)



    # Change slider number
    def updateSlider(self):
        speed = self.slider.value() / 100
        self.sliderText.setText(f"Speed: {speed:.2f}x")

    # Open files
    def openFile(self):
        self.folderPath = QFileDialog.getExistingDirectory(self, "Pick Folder")
        if self.folderPath:
            self.fileTitle.clear()
            for fileName in os.listdir(self.folderPath):
                if fileName.endswith(".mp3"):
                    self.fileTitle.addItem(fileName)


    # Play Audio Files
    def playAudio(self):
        if self.fileTitle.selectedItems() and hasattr(self, 'folderPath'):
            fileName = self.fileTitle.selectedItems()[0].text()
            filePath = os.path.join(self.folderPath, fileName)
            fileUrl = QUrl.fromLocalFile(filePath)

            self.mediaPlayer.setSource(fileUrl)
            self.mediaPlayer.setPlaybackRate(self.slider.value() / 100.0)
            self.mediaPlayer.play()

            #Deactivate button for now
            self.btnPause.setEnabled(True)
            self.btnResume.setDisabled(True)
            self.btnReset.setEnabled(True)
            self.btnPlay.setDisabled(True)


    def pauseAudio(self):
        self.mediaPlayer.pause()
        self.btnPause.setDisabled(True)
        self.btnResume.setEnabled(True)
    
    def resumeAudio(self):
        self.mediaPlayer.play()
        self.btnPause.setEnabled(True)
        self.btnResume.setDisabled(True)
    
    def resetAudio(self):
        if self.mediaPlayer.isPlaying():
            self.mediaPlayer.stop()
        
        self.mediaPlayer.setPosition(0)
        self.mediaPlayer.setPlaybackRate(self.slider.value() / 100.0)
        self.mediaPlayer.play()

        self.btnPause.setEnabled(True)
        self.btnResume.setDisabled(True)
        self.btnReset.setDisabled(True)
        self.btnPlay.setDisabled(True)

        QTimer.singleShot(100, lambda: self.btnReset.setEnabled(True))


if __name__ in "__main__":
    app = QApplication([])
    main = AudioApp()
    main.show()
    app.exec()