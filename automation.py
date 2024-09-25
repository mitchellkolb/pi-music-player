from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)  # Set headless=True to run without GUI
    context = browser.new_context()

    # Open a new page
    start_url = "http://pianostream.com/"
    page = context.new_page()

    # Navigate to the login page
    page.goto(start_url)

    # Fill in the username and password fields using the provided selectors
    page.fill("#email", "test")      # Using the 'id' selector for the email field
    page.fill("#password", "test")   # Using the 'id' selector for the password field

    # Click the login button
    page.click("button[type='submit']")  # Update this selector if necessary

    # Wait for navigation after login
    page.wait_for_load_state("networkidle")

    # Navigate to the music page (if not redirected automatically)
    page.goto("https://www.your-music-site.com/music")  # Replace with the actual music page URL

    # Click the play button
    page.click("button.play-button")  # Update the selector based on the site's play button

    # Wait for the song title to appear
    page.wait_for_selector("div.song-title")  # Update the selector based on the site's structure

    # Extract the song title
    song_title = page.inner_text("div.song-title")
    print("Currently playing:", song_title)

    # Optionally, keep the browser open
    input("Press Enter to close the browser...")

    # Close the browser
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
