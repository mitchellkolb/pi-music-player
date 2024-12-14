

import autoDownload
import os



def main():

    os.system('clear')
    myautomation = autoDownload.MusicAutomation("http://pianostream.com/")    

    while True:
        print("\nMain Menu")
        print("1) Launch Browser")
        print("2) Skip")
        print("3) Pause/Play")
        print("4) Hello Print")
        print("9) Exit")

        try:
            choice = int(input("Select an option (1-9): "))

            if choice == 1:
                myautomation.loadCredentails()
                myautomation.startBrowser()
                myautomation.eventListeners()
                myautomation.login()
            elif choice == 2:
                myautomation.clickSkip()
            elif choice == 3:
                myautomation.clickPlayPause()
            elif choice == 4:
                myautomation.hello()
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
