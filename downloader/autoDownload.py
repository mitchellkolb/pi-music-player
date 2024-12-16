from playwright.sync_api import sync_playwright, Playwright
from dotenv import load_dotenv
import os, time
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC

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
        self.songLink = ""

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
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def hello(self):
        print("Moving on")


    def handleRequest(self, request):
        resource_type = request.resource_type
        if resource_type in ["media"]:
            if "pianostream.com/api" in request.url:
               self.songLink = request.url
               print(f"{request.url}")

               try:
                    filename = "AudioFile"
                    # Use cookies from the current context to download the file
                    cookies = self.context.cookies()
                    cookiesDict = {cookie['name']: cookie['value'] for cookie in cookies}

                    # Save file to a custom directory
                    saveDir = os.path.join(os.getcwd(), "SavedFiles")
                    os.makedirs(saveDir, exist_ok=True)
                    savePath = os.path.join(saveDir, filename)

                    print(f"Downloading file from {request.url}...")
                    with requests.get(request.url, cookies=cookiesDict, stream=True) as response:
                        response.raise_for_status()
                        with open(savePath, 'wb') as file:
                            for chunk in response.iter_content(chunk_size=8192):
                                file.write(chunk)
                    if self.commentsEnable:
                        print(f"File saved to {savePath}")
               except Exception as e:
                    print(f"Error in handleRequest media try block: {e}")


    def downloadCoverImage(self):
        try:
            albumArtURL = self.getAlbumArtUrl()
            filename = "CoverImage"
            # Create the "SavedImages" directory in the current directory if it doesn't exist
            saveDir = os.path.join(os.getcwd(), "SavedImages")
            os.makedirs(saveDir, exist_ok=True)
            savePath = os.path.join(saveDir, filename)

            # Send a GET request to the URL
            response = requests.get(albumArtURL, stream=True)
            response.raise_for_status()  # Check for HTTP errors

            # Open the file in write-binary mode and write the content
            with open(savePath, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            if self.commentsEnable:
                print(f"File saved to {savePath}")
        except requests.exceptions.RequestException as e:
            print(f"downloadCoverImage(): Error downloading the file: {e}")
                    

    def handleResponse(self, response):
        resource_type = response.request.resource_type
        if resource_type in ["media"]:
            print(f"<-- Media Response: {response.status} {response.url}")
           

    def eventListeners(self):
        if not self.page:
            print("eventListeners() -> Browser Page is not initialized. Call startBrowser() first.")
            return

        try:
            if self.commentsEnable:
                print("Starting listeners...")
            # Note the use of self.handleRequest and self.handleResponse
            self.page.on("request", self.handleRequest)
            #self.page.on("response", self.handleResponse)

        except Exception as e:
            print(f"Error setting event listeners: {e}")
        

    def clickButton(self, selector: str, attributeName: str) -> bool:
        if not self.page:
            print(f"{attributeName}: -> Browser Page is not initialized. Call startBrowser() first.")
            return None
        
        try:
            self.page.click(selector)

            if self.commentsEnable:
                print(f"Clicked on {attributeName}.")
            return True

        except Exception as e:
            print(f"Error clicking {attributeName}: {e}")
            return False


    def clickSkip(self):
        return self.clickButton("#skipButton", "Skip Button")


    def clickPlayPause(self):
        return self.clickButton("#playButton", "Play Button")


    def getWebAttribute(self, selector: str, attributeName: str) -> str:
        if not self.page:
            print(f"{attributeName}: -> Browser Page is not initialized. Call startBrowser() first.")
            return None

        try:
            self.page.wait_for_selector(selector)
            attributeValue = self.page.inner_text(selector)
            if self.commentsEnable:
                print(f"Current {attributeName}: {attributeValue}")
            return attributeValue

        except Exception as e:
            print(f"Error fetching {attributeName}: {e}")
            return None


    def getSongArtist(self) -> str:
        return self.getWebAttribute("#songArtist", "song artist")


    def getSongTitle(self) -> str:
        return self.getWebAttribute("#songTitleRow", "song title")


    def getAlbumTitle(self) -> str:
        return self.getWebAttribute("#songAlbum", "album title")


    def getAlbumArtUrl(self) -> str:
        if not self.page:
            print("getAlbumArtUrl(): -> Browser Page is not initialized. Call startBrowser() first.")
            return None

        try:
            self.page.wait_for_selector("#albumArt")
            album_art_url = self.page.get_attribute("#albumArt", "src")
            if self.commentsEnable:
                print(f"Album art URL: {album_art_url}")
            return album_art_url
        
        except Exception as e:
            print(f"Error fetching album art URL: {e}")
            return None


    def addMetaData(self) -> None:
        if not self.page:
            print("addMetaData(): -> Browser Page is not initialized. Call startBrowser() first.")
            return None

        audioFilePath = os.path.join("SavedFiles", "AudioFile")
        coverArtPath = os.path.join("SavedImages", "CoverImage")

        # Ensure the audio file exists
        if not os.path.exists(audioFilePath):
            print(f"Audio file not found: {audioFilePath}")
            return
        
        # Ensure the cover art file exists
        if not os.path.exists(coverArtPath):
            print(f"Cover art file not found: {coverArtPath}")
            return
        
        # Load and tag theMP3 File
        audio = MP3(audioFilePath, ID3=ID3)
        
        # My audio files are new and don't have the tag metadata that real mp3's have so I need to add the tag to assign information to it
        if audio.tags is None:
            audio.add_tags()
        
        # Add the metadata of the song to the song
        audio.tags.add(TPE1(encoding=3, text=self.getSongArtist()))
        audio.tags.add(TIT2(encoding=3, text=self.getSongTitle()))
        audio.tags.add(TALB(encoding=3, text=self.getAlbumTitle()))

        # Assign the Cover Art to the audio file
        with open(coverArtPath, "rb") as albumArt:
            audio.tags.add(
                APIC(
                    encoding = 3,
                    mime = "image/jpeg",
                    type = 3,
                    desc = "Cover",
                    data = albumArt.read()
                )
            )

        # Save all that stuff to the file
        audio.save()
        if self.commentsEnable:
            print(f"Metadata updated for {audioFilePath}")
