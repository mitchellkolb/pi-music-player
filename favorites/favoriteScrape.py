from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os, time


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
        print(f"Current URL in context: {self.favPage.url}")
        self.favPage.wait_for_load_state("networkidle")
        pageContent = self.favPage.content()
        