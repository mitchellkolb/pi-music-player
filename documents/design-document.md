

# System Design Document: Pi Music Player



## Table of Contents
- [Introduction]()
- [Notes of Program](#notes-of-program)
- [Functional Requirements](#functional-requirements)
- [Nonfunctional Requirements](#nonfunctional-requirements)


### Notes of Program
- On startup the raspberry pi launches the GUI
- GUI
    - WINDOW 1 (Startup)
        - "start" button to begin the web automation 
        - "quit" button to shutdown the gui and return to the desktop
        - "restart" button to restart the PI
        - "update" to pull the latest version from the repo and restart the gui
    - WINDOW 2 (Music Player)
        - "Settings" button
            - To shutdown/quit the gui and return to the desktop
            - Restart raspberry pi
        - "Play" button 
            - When pressed the web automation presses the play button on the website to play the music
            - When pressed the button alternates to the pause icon and takes on the pause functionality
        - "Pause" button 
            - When pressed the web automation presses the pause button on the website to pause the music
            - When pressed the button alternates to the play icon and takes on the play functionality
        - "Volume Slider" button 
        - "Thumbs Up" button 
        - "Thumbs Down" button 
- Automation
    - Logs into the painostream.com
    - Save the Song image, title, artist



### Functional Requirements
- 


### Nonfunctional Requirements

