from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os, time, requests, shutil
from pathlib import Path


class MusicAutomation:
    def __init__(self, site_url: str):
        self.site_url = site_url
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.email = None
        self.password = None
        self.commentsEnable = True
        self.favPage = None

    def loadCredentails(self):
        # Loads the creds from the local .env file to use in the browser instance
        load_dotenv()

        self.email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')
        if self.commentsEnable == True:
           print({self.email})

        if not self.email or not self.password:
            print("Email or password not found in environment variables.")
            return


    def startBrowser(self):
        # This starts the browser instance and opens the webpage
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox.launch(headless=False)  # Set headless=True for headless mode
        self.context = self.browser.new_context(accept_downloads=True)
        self.page = self.context.new_page()

        # Navigate to the website
        self.page.goto(self.site_url)
        self.page.wait_for_load_state("networkidle")

        if self.commentsEnable:
            print("Browser navigated to the site.")


    def login(self):
        if not self.page:
            print("login() -> Browser page is not initalized. Need to call startBrowser() correctly")
            return
        
        self.page.fill("#email", self.email)
        self.page.fill("#password", self.password)
        self.page.click("#login-form-button-submit")
        self.page.wait_for_selector("#playButton.btn-pause")
        time.sleep(1)
        if self.commentsEnable == True:
           print("Logged in")
 

    def close(self):
        if self.page:
            self.page.close()
        if self.favPage:
            self.favPage.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        if self.commentsEnable:
            print("*** Playwright was Successfully Closed ***")


    def clickButton(self, selector: str, attributeName: str) -> None:
        if not self.page:
            print(f"{attributeName}: -> Browser Page is not initialized. Call startBrowser() first.")
            return None
        try:
            self.page.click(selector)
            if self.commentsEnable:
                print(f"Clicked on {attributeName}.")

        except Exception as e:
            print(f"Error clicking {attributeName}: {e}")


    def clickPlayPause(self) -> None:
        return self.clickButton("#playButton", "Play/Pause Button")
    
    def clickTools(self) -> None:
        return self.clickButton("#toolsButton", "Tools Button")
    
    def clickViewFavorites(self) -> None:
        with self.context.expect_page() as newPage:
            self.clickButton("#viewFavoritesSubmit", "View Favorites")

        self.favPage = newPage.value
        if self.commentsEnable:
            print(f"New focus is {self.favPage.url}")
    
    def printSiteTitle(self) -> None:
        if self.commentsEnable:
            print(f"Browser on {self.favPage.url} --> {self.favPage.title()}")


    def scrapeFavorites(self) -> None:
        
        """
        Either opens the playwright browser instance to save favorites html list or pulls in the webpage.txt html from a local file if you decided to save it and then scrapes the favorites and deleted song lists and exports them to their own files respectively.

        Parameters:
            None

        Returns:
            No values returned but two files are created/modifed in this local dir, favorites.txt and deletes.txt
       """
        # Used for debugging and only allowing one to go at a time
        enableFavorites = True
        enableDeletes = True
        enableBrowser = True  #True means it will use playwright (Make sure to set up the browser before using this option in the main menu), False means it will use local webpage.txt which should basically have the saved html from the site that the playwright goes to
        enableExport = False  #In the Browser option you can export the site html. This made it so in dev I didn't have to open the site a bunch of times and wait for it to load to scrape it.


        if enableBrowser == True:
            if self.commentsEnable:
                print(f"Current URL in context: {self.favPage.url}")
            self.favPage.wait_for_load_state("networkidle")

            if enableExport:
                #Export the page to a .txt file to test locally
                pageContent = self.favPage.content()
                with open("webpage.txt", "w") as file:
                    file.write(pageContent)

            #Uses the live site info to extract the html
            # cookies = self.context.cookies()
            # cookiesDict = {cookie['name']: cookie['value'] for cookie in cookies}
            # requestsFavPage =  requests.get(self.favPage.url, cookies=cookiesDict, stream=True)
            # if self.commentsEnable:
            #     print(f"cookies are:\n {cookiesDict}...")
            #     print(f"status code: {requestsFavPage.status_code}")
            # soup = BeautifulSoup(requestsFavPage.text, features="html.parser")
            
            # Use Playwright's page content directly for BeautifulSoup
            pageContent = self.favPage.content()  # Get live page HTML
            soup = BeautifulSoup(pageContent, 'html.parser')
        
        else:
            # Dynamically find the file in the local directory
            currentDir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
            fileName = "webpage.txt"  # Change to .html if you rename the file
            filePath = os.path.join(currentDir, fileName)
            # Open the file and load into BeautifulSoup
            with open(filePath, "r", encoding="utf-8") as file:
                htmlContent = file.read()
            soup = BeautifulSoup(htmlContent, 'html.parser')
            if self.commentsEnable:
                print("Using Webpage.txt for info")
                print(f"File that is loaded: ->  {soup.title.text}")

        if enableFavorites:
            favorites = soup.find_all("tr")[6]
            # Find all artistblock divs within this specific row
            artistBlocks = favorites.find_all('div', class_='artistblock')
            
            # Initialize a list to store song names
            songNames = []
            # Loop through each artist block and find the relevant <a> tags
            for block in artistBlocks:
                artistLinks = block.find_all('a', class_='artistlinks', href=True)
                # Extract every second <a> tag as it contains the song names
                for i in range(1, len(artistLinks), 2):  # Skip every other <a> tag
                    songNames.append(artistLinks[i].text.strip())

            with open("favorites.txt", "w", encoding="utf-8") as file:
                for index, song in enumerate(songNames):
                    if index < len(songNames) - 1:  # Not the last item
                        file.write(song + "\n")
                    else:  # Last item
                        file.write(song)

            if self.commentsEnable:
                print(f"Number of Favorites: {len(songNames)}")

        if enableDeletes:
            deletes = soup.find_all("tr")[8]
            # Find all artistblock divs within this specific row
            artistLinks = deletes.find_all('a', class_='artistlinks', href=True)

            # Assign all the song items to a list. This only appends the name of the song and not the whole <a> tag
            deleteNames = []
            for name in artistLinks:
                deleteNames.append(name.text)

            with open("deletes.txt", "w", encoding="utf-8") as file:
                for index, song in enumerate(deleteNames):
                    if index < len(deleteNames) - 1:  # Not the last item
                        file.write(song + "\n")
                    else:  # Last item
                        file.write(song)

            if self.commentsEnable:
                print(f"Number of Deletes: {len(deleteNames)}")



    def cleanFolder(self) -> None:
        """
        This function takes the song names from favorites.txt and deletes.txt and then goes through the folder where my unsorted downloaded songs are and seperates the songs into their respective folders

        Parameters:
            None from the function call.
            FilePath needs to be specified in .env

        Returns:
            None from function.
            Folders within the .env FILEPATH folder where the songs are seperated into
        
        """
        # --- This is the file path of the .mp3s songs folder
        load_dotenv()
        songFilePath = os.getenv("FILEPATH")
        print(songFilePath)

        # Get the directory of this script. I'm trying out pathlib becuase I read on an article it is better cuase its newer.
        scriptDir = Path(__file__).parent
        
        # --- Define file paths
        favoritesTXTPath = scriptDir / "favorites.txt"
        deletesTXTPath = scriptDir / "deletes.txt"
        notMovedTXTPath = scriptDir / "notMoved.txt"
        
        # Check if .txt exists
        if not favoritesTXTPath.exists():
            print("favorites.txt does not exist.")
        
        if not deletesTXTPath.exists():
            print("deletes.txt does not exist.")
        

        # --- Creating the Folders for where the songs will be placed in.
        favoritesFolderPath = scriptDir / "favoritesSorted"
        deletesFolderPath = scriptDir / "deletesSorted"

        # Create the folder if it doesn't exist
        if not favoritesFolderPath.exists():
            favoritesFolderPath.mkdir()
            print(f"Folder '{favoritesFolderPath.name}' created successfully.")
        else:
            print(f"Folder '{favoritesFolderPath.name}' already exists.")
        if not deletesFolderPath.exists():
            deletesFolderPath.mkdir()
            print(f"Folder '{deletesFolderPath.name}' created successfully.")
        else:
            print(f"Folder '{deletesFolderPath.name}' already exists.")


        # -- Reading and adding the data from the .txt to sets to loop through 
        favoritesList = []
        with open(favoritesTXTPath, "r", encoding="utf-8") as favoritesFile:
            for line in favoritesFile:
                line = line.strip()
                if line:
                    favoritesList.add(line)

        deletesList = []
        with open(deletesTXTPath, "r", encoding="utf-8") as deletesFile:
            for line in deletesFile:
                line = line.strip()
                if line:
                    deletesList.add(line)

        # --- Going through each song and moving them to the correct folder
        notMovedList = []
        # Go through each file in the lists
        for songName in deletesList:
            self.movedMatchedFiles(songName, songFilePath, deletesFolderPath)




        # Write the not moved songs to notMoved.txt
        if notMovedList:  # go on only if the list has items
            with open(notMovedTXTPath, "w", encoding="utf-8") as notMovedFile:
                for item in notMovedList:
                    notMovedFile.write(item + "\n")
            print(f"File '{notMovedTXTPath.name}' created/updated with {len(notMovedList)} items.")


    def movedMatchedFiles(self, songName, sourceDir, outputDir) -> bool:

        """
        This function matches a given song name (without extension) to an existing file in the source directory, appending '.mp3' to the name.
        If the file exists, it moves the song to the specified output directory.

        Parameters:
            songName (str): The base name of the song (without the .mp3 extension).
            sourceDir (str): The directory where the unsorted songs are located.
            outputDir (str): The directory where matched songs should be moved.

        Returns:
            bool: True if the song was successfully found and moved, False otherwise.
       
        """

        # Make sure the destination directory exists in the system
        Path(outputDir).mkdir(exist_ok=True)

        fullSongName = f"{songName}.mp3"
        sourceFilePath = os.path.join(sourceDir, fullSongName)
        outputFilePath = os.path.join(outputDir, fullSongName)

        # Check if the file exists in the source dir
        if os.path.exists(sourceFilePath):
            # This means that the song is matched so we will move it out
            shutil.move(sourceFilePath, outputFilePath)
            if self.commentsEnable:
                print(f"Moved {fullSongName} to {outputDir}")
            return True
        else:
            if self.commentsEnable:
                print(f"{fullSongName} : Not found")
            return False

            