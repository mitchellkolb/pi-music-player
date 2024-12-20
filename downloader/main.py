

import playwright
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
        browserStatupBool = True
        while browserStatupBool == True:
            try:
                time.sleep(5)
                print("\n")
                downloadingLoop = 0
                myautomation.loadCredentails()
                myautomation.startBrowser()
                try:
                    myautomation.login()
                except playwright._impl._errors.TimeoutError as e:
                    print(f"Login timeout detected: {e}")
                    print("Resetting main loop due to popup or timeout issue...")
                    continue 
                time.sleep(5)
                myautomation.eventListeners()
                myautomation.clickSkip()
                while downloadingLoop <= 10:
                    print("\n")
                    startTime = time.time()
                    myautomation.errorMenu()
                    time.sleep(5)

                    # Check if the cover image is not unique OR the song is not unique
                    if not myautomation.confirmCoverImage() or not myautomation.isSongUnique():
                        myautomation.errorMenu()
                        myautomation.clickSkip()
                        downloadingLoop += 1
                        continue  # Skip this iteration and move to the next one
                    else:
                        time.sleep(2)
                        myautomation.clickPlayPause()
                        time.sleep(2)
                        myautomation.downloadCoverImage()
                        myautomation.addMetaData()
                        myautomation.renameFile()
                        
                        downloadingLoop = 0
                        # Skipping the song in the scenario where the loop is about to break makes the browser take a long time to close. So in the world where we are just gonna to close it there is no need to skip.  
                        if downloadingLoop < 10:
                            myautomation.clickSkip()
                        
                        elapsedTime = time.time() - startTime
                        print(f"Time Taken: {elapsedTime: .2f} seconds")

                myautomation.close()
            
            except Exception as e:
                print(f"\nUnexpected error occurred: {e}")
                print("Restarting the main loop...")
                myautomation.close()

            # finally:
            #     myautomation.close()



if __name__ == "__main__":
    main()
