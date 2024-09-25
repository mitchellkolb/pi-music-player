# music_automation.py

from playwright.sync_api import sync_playwright
from threading import Thread, Event
import queue
from dotenv import load_dotenv
import os

class MusicAutomation:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Get email and password from environment variables
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')

        if not self.email or not self.password:
            print("Email or password not found in environment variables.")
            return

        # Command queue for communication
        self.command_queue = queue.Queue()
        self.result_queue = queue.Queue()

        # Event to signal thread termination
        self.stop_event = Event()

        # Start the Playwright thread
        self.thread = Thread(target=self.playwright_thread)
        self.thread.start()

    def playwright_thread(self):
        # Initialize Playwright in this thread
        with sync_playwright() as playwright:
            # Launch the browser
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 720, "height": 550})
            page = context.new_page()

            # Navigate to the login page
            start_url = "http://pianostream.com/"
            page.goto(start_url)

            # Fill in the username and password fields
            page.fill("#email", self.email)
            page.fill("#password", self.password)

            # Click the login button
            page.click("#login-form-button-submit")

            # Wait for the play button to change to pause state
            page.wait_for_selector("#playButton.btn-pause")

            # Signal that initialization is complete
            self.result_queue.put(("initialized", None))

            while not self.stop_event.is_set():
                try:
                    # Wait for a command with a timeout
                    command, args = self.command_queue.get(timeout=1)
                    if command == "play":
                        self._play(page)
                    elif command == "pause":
                        self._pause(page)
                    elif command == "get_song_info":
                        info = self._get_song_info(page)
                        self.result_queue.put(("song_info", info))
                    elif command == "close":
                        break
                    elif command == "play_pause":
                        self._play_pause(page)
                    elif command == "get_class_name":
                        class_name = page.get_attribute("#playButton", "class")
                        self.result_queue.put(("class_name", class_name))
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Error in playwright_thread: {e}")
                    self.result_queue.put(("error", str(e)))
            # Clean up
            try:
                browser.close()
                context.close()
                print("Browser closed.")
            except Exception as e:
                print(f"Error closing browser: {e}")
        # Playwright automatically stops when exiting the 'with' block
        print("Playwright stopped.")


    def _play_pause(self, page):
        class_name = page.get_attribute("#playButton", "class")
        if "btn-play" in class_name:
            page.click("#playButton")
            page.wait_for_selector("#playButton.btn-pause")
            print("Music started playing.")
            self.result_queue.put(("play", "Music started playing."))
        elif "btn-pause" in class_name:
            page.click("#playButton")
            page.wait_for_selector("#playButton.btn-play")
            print("Music paused.")
            self.result_queue.put(("pause", "Music paused."))
        else:
            print("Unable to determine play/pause state.")
            self.result_queue.put(("error", "Unable to determine play/pause state."))

    def _get_song_info(self, page):
        try:
            page.wait_for_selector("#songArtist", timeout=10000)
            song_artist = page.inner_text("#songArtist")
            page.wait_for_selector("#songTitle", timeout=10000)
            song_title = page.inner_text("#songTitle")
            page.wait_for_selector("#songAlbum", timeout=10000)
            album_title = page.inner_text("#songAlbum")
            return {
                "song_artist": song_artist,
                "song_title": song_title,
                "album_title": album_title
            }
        except Exception as e:
            print(f"Error getting song info: {e}")
            return None

    def send_command(self, command, args=None):
        self.command_queue.put((command, args))

    def get_result(self):
        try:
            return self.result_queue.get_nowait()
        except queue.Empty:
            return None

    def close(self):
        if self.thread.is_alive():
            self.stop_event.set()
            self.send_command("close")
            self.thread.join()
            print("Playwright thread closed.")
