from playwright.sync_api import sync_playwright, Playwright
from dotenv import load_dotenv
import os



class MusicAutomation:
    def __init__(self, site_url: str):
        self.site_url = site_url
        self.browser = None
        self.page = None
        self.email = None
        self.password = None

    def loadCredentails(self):
        load_dotenv()

        email = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')

        if not email or not password:
            print("Email or password not found in environment variables.")
            return

    def start_browser(self):
        # This starts the browser instance and ope
        with sync_playwright() as playwright:
            self.browser



def run(playwright: Playwright):

    load_dotenv()

    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')

    if not email or not password:
        print("Email or password not found in environment variables.")
        return



    # Browser Code begins here:
    browser = playwright.firefox.launch(headless=False)  # Set headless=True to run without GUI
    context = browser.new_context(viewport={"width": 720, "height": 550})

    # Open a new page
    start_url = "http://pianostream.com/"
    page = context.new_page()

    # Navigate to the login page
    page.goto(start_url)

    # Fill in the username and password fields using the provided selectors
    page.fill("#email", email)
    page.fill("#password", password)


    # Click the login button
    page.click("#login-form-button-submit")  # Update this selector if necessary

    # Wait for navigation after login
    page.wait_for_selector("#playButton.btn-pause")
    
    
    # #press play
    # try:
    #     page.click("#playButton")
    # except Exception as e:
    #     print("An error occurred:", e)


    # song artist 
    page.wait_for_selector("#songArtist")
    songArtist = page.inner_text("#songArtist")

    # song title 
    page.wait_for_selector("#songTitleRow")
    songTitle = page.inner_text("#songTitleRow")

    # album title 
    page.wait_for_selector("#songAlbum")
    albumTitle = page.inner_text("#songAlbum")

    print("song artist:", songArtist)
    print("song title:", songTitle)
    print("album title:", albumTitle)


    """-----------------------------------"""
    # Optionally, keep the browser open
    input("Press Enter to close the browser...")

    # Close the browser
    browser.close()
    """-----------------------------------"""








def main():

    automation = MusicAutomation("http://pianostream.com/")



if __name__ == "__main__":
    main()