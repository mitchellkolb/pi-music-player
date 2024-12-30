from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os, time, requests


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

    def AscrapeFavorites(self):
        print(f"Current URL: {self.favPage.url}\n")
        self.favPage.wait_for_load_state("networkidle")

        # Wait for the specific <tr> to load
        self.favPage.wait_for_selector("tr:has(b:has-text('our Favorite Songs...'))")
        
        # Select the specific <tr> containing 'Your Favorite Songs...'
        target_row = self.favPage.query_selector("tr:has(b:has-text('our Favorite Songs...'))")
        
        if target_row:
            # Find all links within the targeted row
            artistLinks = target_row.query_selector_all("a.artistlinks[target='_blank']")
            
        print(f"Found {len(artistLinks)} elements matching the selector.")
        
        data = []
        for link in artistLinks:
            try:
                textContent = link.inner_text()
                data.append(textContent)
            except Exception as e:
                print(f"Error fetching text for a link: {e}")

        #print(f"\n\nHere is the Data\n\n{data} \n\n")

        cleanData = [i for i in data if i != '']

        with open("data.txt", "w") as file:
            file.write("\n".join(cleanData))


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





