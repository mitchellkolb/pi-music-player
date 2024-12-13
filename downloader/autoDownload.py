from playwright.sync_api import sync_playwright, Playwright
from dotenv import load_dotenv
import os, time
import requests

from urllib.parse import urlparse, urlunparse


class MusicAutomation:
    def __init__(self, site_url: str):
        self.site_url = site_url
        self.playwright = None
        self.browser = None
        self.page = None
        self.email = None
        self.password = None
        self.commentsEnable = True
        self.selectedURLs = []  # To store URLs for downloading

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
        self.page = self.browser.new_page()

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



    def viewNetwork(self):
        if not self.page:
            print("downloadSong(): -> Browser Page is not initialized. Call startBrowser() first.")
            return
        
        try:
            print("viewing network links")

        except Exception as e:
            print(f"Error fetching album art URL: {e}")
            return
        

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


