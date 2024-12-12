from playwright.sync_api import sync_playwright, Playwright
from dotenv import load_dotenv
import os, time



class MusicAutomation:
    def __init__(self, site_url: str):
        self.site_url = site_url
        self.playwright = None
        self.browser = None
        self.page = None
        self.email = None
        self.password = None
        self.commentsEnable = True


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
        # This starts the browser instance and opens the webpage and waits for it to load
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox.launch(headless=False)
        self.page = self.browser.new_page()
        self.page.goto(self.site_url)


        if self.commentsEnable == True:
            print("I'm at the site")


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


    def clickPlayPause(self):
        return self.clickButton("#playButton", "Play Button")
    

    def clickThumbsUp(self):
        return self.clickButton("#favoriteButton", "Thumbs Up")
    

    def clickThumbsDown(self):
        return self.clickButton("#rejectButton", "Thumbs Down")


    def clickMute(self):
        return self.clickButton("#muteButton", "Mute Button")

        
    def volumeSlider(self, target_percentage: int):
        """
        Adjust the volume slider to the target percentage (0-100%).

        :param target_percentage: Desired volume percentage (0-100).
        """
        if not self.page:
            print("volumeSlider(): -> Browser Page is not initialized. Call startBrowser() first.")
            return False

        try:
            # Ensure the target percentage is within valid bounds
            target_percentage = max(0, min(target_percentage, 100))

            # Locate the slider element
            slider_bar = self.page.locator("#volume")

            # Get the bounding box of the slider
            slider_box = slider_bar.bounding_box()
            if not slider_box:
                print("Failed to retrieve slider bounding box.")
                return False

            # Calculate the target x-coordinate based on percentage
            target_x = slider_box["x"] + (slider_box["width"] * target_percentage / 100)
            center_y = slider_box["y"] + slider_box["height"] / 2

            # Use the mouse to click and drag to the target position
            self.page.mouse.move(slider_box["x"], center_y)
            self.page.mouse.down()
            self.page.mouse.move(target_x, center_y)
            self.page.mouse.up()

            if self.commentsEnable:
                print(f"Volume adjusted to {target_percentage}%.")
            return True

        except Exception as e:
            print(f"Error adjusting volume slider: {e}")
            return False
    

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


