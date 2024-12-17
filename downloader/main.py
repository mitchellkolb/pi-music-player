

import autoDownload
import os, time



def main():

    os.system('clear')
    myautomation = autoDownload.MusicAutomation("http://pianostream.com/")    


    """
    1 - Uses the Text Menu in the terminal
    2 - Uses no Text Menu but loops 3 times
    """
    terminalStyle = 2

    if terminalStyle == 1:
        while True:
            print("\nMain Menu")
            print("1) Launch Browser")
            print("2) Event Listeners")
            print("3) Skip")
            print("4) Pause/Play")
            print("5) Download Cover Image")
            print("6) Add meta data")
            print("7) Rename File")
            print("9) Exit")

            try:
                choice = int(input("Select an option (1-9): "))

                if choice == 1:
                    myautomation.loadCredentails()
                    myautomation.startBrowser()
                    myautomation.login()
                elif choice == 2:
                    myautomation.eventListeners()
                elif choice == 3:
                    myautomation.clickSkip()
                elif choice == 4:
                    myautomation.clickPlayPause()
                elif choice == 5:
                    print("choice 5")
                    myautomation.downloadCoverImage()
                elif choice == 6:
                    print("choice 6")
                    myautomation.addMetaData()
                elif choice == 7:
                    print("choice 7")
                    myautomation.renameFile()
                elif choice == 9:
                    myautomation.close()
                    print("Completed myautomation")
                    break
                else:
                    print("Invalid selection. Please choose a number between 1 and 9.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9.")
    
    elif terminalStyle == 2:
        cutOff = 4
        myautomation.loadCredentails()
        myautomation.startBrowser()
        myautomation.login()
        myautomation.eventListeners()
        myautomation.clickSkip()
        for i in range(cutOff):
            # Check if the cover image is not unique OR the song is not unique
            if not myautomation.confirmCoverImage() or not myautomation.isSongUnique():
                myautomation.clickSkip()  # Skip to the next song
                continue  # Skip this iteration and move to the next one
            time.sleep(1)
            myautomation.clickPlayPause()
            time.sleep(1)
            myautomation.downloadCoverImage()
            myautomation.addMetaData()
            myautomation.renameFile()
            if i != cutOff - 1:
                myautomation.clickSkip()
        myautomation.close()



if __name__ == "__main__":
    main()
