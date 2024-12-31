
import playwright
import favoriteScrape
import os, time



def main():

    os.system('clear')
    scrapper = favoriteScrape.MusicAutomation("http://pianostream.com/")    

    terminalStyle = 1

    if terminalStyle == 1:
        while True:
            print("\nMain Menu")
            print("1) Launch Browser and go to favorites")
            print("2) Scrape the lists")
            print("3) Print Current Tab Focus")
            print("4) Clean Favorites/Deletes From Song List")
            
            print("9) Exit")

            try:
                choice = int(input("Select an option (1-9): "))

                if choice == 1:
                    scrapper.loadCredentails()
                    scrapper.startBrowser()
                    scrapper.login()
                    scrapper.clickPlayPause()
                    scrapper.clickTools()
                    scrapper.clickViewFavorites()
                elif choice == 2:
                    print("choice 2")
                    scrapper.scrapeFavorites()
                elif choice == 3:
                    print("choice 3")
                    scrapper.printSiteTitle()
                elif choice == 4:
                    print("choice 4")
                    scrapper.cleanFolder()
                elif choice == 5:
                    print("choice 5")
                    
                elif choice == 6:
                    print("choice 6")
                    
                elif choice == 7:
                    print("choice 7")
                    
                elif choice == 9:
                    scrapper.close()
                    print("Completed scrapper")
                    break
                else:
                    print("Invalid selection. Please choose a number between 1 and 9.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9.")
            


if __name__ == "__main__":
    main()

