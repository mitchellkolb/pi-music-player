

# System Design Document: Pi Music Player
Mitchell Kolb


## Table of Contents
- [Outline](#outline)
- [Notes of Program](#notes-of-program)
- [Rough GUI Idea](#gui-layout-idea)
- [Functional Requirements](#functional-requirements)
- [Nonfunctional Requirements](#nonfunctional-requirements)



## Outline




## Notes of Program
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
            - A number incrementer that has like 5 options it locks to and when it does presses a certain point on the website slider.
            - This slider could also just be connected to system audio settings and keep the website volume on max but just adjust the system volume
        - "Thumbs Up" button 
            - When pressed the web automation presses the thumbs up button on the website to thumbs up the current track
        - "Thumbs Down" button
            - When pressed the web automation presses the thumbs down button on the website to thumbs down the current track
 
- Automation
    - Logs into the painostream.com
    - Save the Song image, title, artist



## GUI Layout Idea
This is a rough idea I made in figma that I will try and follow for the gui on the raspberry pi
![rough idea](rough-gui-layout.png)



## Functional Requirements
- The system must be hands off from the raspberry pi boot up
    - When the power is plugged in the system will turn on so we can use that as a On/Off switch
    - When power is on the system should boot up and open the GUI startup screen in kiosk mode.



## Nonfunctional Requirements
- Maintainability 
- Reliability
- Usability
- Performance

