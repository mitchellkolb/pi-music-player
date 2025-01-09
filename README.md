


<h1 align="center">Pi Music Player</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/mitchellkolb/pi-music-player?color=A22846">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/mitchellkolb/pi-music-player?color=A22846">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/mitchellkolb/pi-music-player?color=A22846">

  <img alt="Github stars" src="https://img.shields.io/github/stars/mitchellkolb/pi-music-player?color=A22846" />
</p>

<p align="center">
<img
    src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"
    alt="Website Badge" />
<img
    src="https://img.shields.io/badge/raspberrypi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white"
    alt="Website Badge" />
<img
    src="https://img.shields.io/badge/PyQT6-41cd52?style=for-the-badge&logo=qt&logoColor=white"
    alt="Website Badge" />
</p>

This is a music player that boots off of a Raspberry Pi 3B+ that opens a browser using playwright and plays music from [pianostream](http://pianostream.com/) with a custom GUI audio controls built with the PyQT UI Python UI library. All of this is going to be placed within a 3D printed case that has openings for all ports and the 5 inch touchscreen.


<details>
<summary style="color:#5087dd">Watch the Full Video Demo Here</summary>

[![Full Video Demo Here](https://img.youtube.com/vi/VidKEY/0.jpg)](https://www.youtube.com/watch?v=VidKEY)

</details>

---


# Table of Contents
- [What I Learned](#what-i-learned-in-this-project)
- [Tools Used / Development Environment](#tools-used--development-environment)
- [How to Set Up](#how-to-set-up)
- [Project Overview](#project-overview)


---

# What I Learned in this Project
- Producing complete software that is used by the client
- Programming using web automation and a new UI library
- Creating specific utility tools to download and sort song files
- Learning how to create 3D models that can be printed and fit with other peripherals.



# Tools Used / Development Environment
- Python
- VS Code
- Terminal
- Windows 10
- Music Site: [pianostream.com](http://pianostream.com/) 
- UI Library: [PyQT](https://doc.qt.io/qtforpython-6/)
- Web Automation: [playwright.dev](https://playwright.dev/) 





# How to Set Up
- This is optional step you can take before the installation & setup section to help keep the project libraries seperate
  - ***(OPTIONAL)*** Create a virtual environment if you choose to do so
      - In the /pi-music-player folder
      - `python3 -m venv venv`
      - On macOS and Linux `source venv/bin/activate`
  - ***(OPTIONAL)*** Managing the virtual environment
      - When you want to leave use `deactivate`
      - Make sure to upgrade pip `python -m pip install --upgrade pip`

- This project was implemented on our local machine inside of a virtual machine using:
  - Clone this repository 
  - Open terminal at the codebase `~.../pi-music-player/`





# Project Overview
This project utilizes playwright now



## Project Details
 - This project contains 3 supplementary folders with utility tools that help when setting up the program.
 1) Downloader: This tool automates the process or downloading songs from the piano site and assigning album art and artist info to the mp3 file when created.
 2) Favorites: This tool saves the liked and disliked songs from your piano stream profile and then once linked to you local folder for where you downloaded your songs will sort them into seperate folders so you can clean your downloaded songs similar to how they are on the player online
 3) Documentation: This contains the documentation and diagrams for the project.

## Files and Structure
- `main.py` Contains the UI code.
- `automation.py` Contains the Web Automation class that controls the browser
- `documents/...` Folder contains the workflow diagrams and project specification documents
- `downloader/...` Folder contains the codebase for the utility tool that automates the downloading of songs from the music player site
- `favorites/...` Folder contains the codebase for the utility tool that auomates the process of downloading the favorites list from the music player account page and then sorts the downloaded songs according to their list preferences.
- `gui/...` Folder contains the codebase to the PyQT6 gui files that are needed to run development builds of the program.
- `savedFiles/...` Folder contains some development png's and jpeg's that can be loaded into the gui folder. 



## Implementation

This Python script automates interactions with a music streaming website using the Playwright library. It includes features like logging in with credentials from a `.env` file, controlling playback (play/pause, thumbs up/down, mute, and volume adjustment), and retrieving metadata such as the current song's title, artist, album name, and album art URL. The script uses CSS selectors to interact with webpage elements and includes detailed error handling and debug messages for seamless operation. Ideal for automating repetitive tasks or gathering music metadata programmatically.

## Future Work
Future improvements could include 
- Having the UI have gestures and actions that are animated to some degree so make the user interface be more identifiable to what they are functionally doing. This could include a colored slider adjustment for the volume slider or clicking sounds for the buttons or sliding animations for when the next song plays instead of the current fading in and out non-animation.
- 







