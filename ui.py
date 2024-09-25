# main.py

import os
from threading import Thread
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from automation import MusicAutomation

class AudioPlayerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # Initialize the MusicAutomation instance to None
        self.music_automation = None
        
        # Start Button
        self.start_button = Button(text="Start")
        self.start_button.bind(on_press=self.start_music)
        self.layout.add_widget(self.start_button)
        
        # Play/Pause Button
        self.play_button = Button(text="Play")
        self.play_button.bind(on_press=self.toggle_play_pause)
        self.layout.add_widget(self.play_button)
        
        # Get Info Button
        self.info_button = Button(text="Get Info")
        self.info_button.bind(on_press=self.get_info)
        self.layout.add_widget(self.info_button)
        
        # End Button
        self.end_button = Button(text="End")
        self.end_button.bind(on_press=self.end_music)
        self.layout.add_widget(self.end_button)
        
        # Label to display song information
        self.info_label = Label(text="Song Info will appear here")
        self.layout.add_widget(self.info_label)
        
        return self.layout
    
    def start_music(self, instance):
        if self.music_automation:
            self.music_automation.close()
        self.music_automation = MusicAutomation()
        # Wait for initialization
        def check_initialized(dt):
            result = self.music_automation.get_result()
            if result and result[0] == "initialized":
                print("Music automation started.")
            else:
                Clock.schedule_once(check_initialized, 0.5)
        Clock.schedule_once(check_initialized, 0.5)
    
    def toggle_play_pause(self, instance):
        if self.music_automation:
            def toggle():
                self.music_automation.send_command("play_pause")
                while True:
                    result = self.music_automation.get_result()
                    if result:
                        if result[0] == "play":
                            Clock.schedule_once(lambda dt: setattr(self.play_button, 'text', "Pause"))
                            break
                        elif result[0] == "pause":
                            Clock.schedule_once(lambda dt: setattr(self.play_button, 'text', "Play"))
                            break
                        elif result[0] == "error":
                            print("Error:", result[1])
                            break
            Thread(target=toggle).start()
        else:
            self.info_label.text = "Please press Start first."
    
    def get_info(self, instance):
        if self.music_automation:
            def fetch_info():
                self.music_automation.send_command("get_song_info")
                while True:
                    result = self.music_automation.get_result()
                    if result:
                        if result[0] == "song_info":
                            info = result[1]
                            if info:
                                song_info = f"Artist: {info['song_artist']}\nTitle: {info['song_title']}\nAlbum: {info['album_title']}"
                                Clock.schedule_once(lambda dt: setattr(self.info_label, 'text', song_info))
                            else:
                                Clock.schedule_once(lambda dt: setattr(self.info_label, 'text', "Unable to retrieve song info."))
                            break
                        elif result[0] == "error":
                            print("Error:", result[1])
                            Clock.schedule_once(lambda dt: setattr(self.info_label, 'text', "Error retrieving song info."))
                            break
            Thread(target=fetch_info).start()
        else:
            self.info_label.text = "Please press Start first."
    
    def end_music(self, instance):
        if self.music_automation:
            self.music_automation.close()
            self.music_automation = None
            Clock.schedule_once(lambda dt: setattr(self.play_button, 'text', "Play"))
            Clock.schedule_once(lambda dt: setattr(self.info_label, 'text', "Music automation ended."))
            print("Music automation ended.")
        else:
            self.info_label.text = "Music automation is not running."
    
    def info_label_update(self, text):
        self.info_label.text = text

if __name__ == "__main__":
    AudioPlayerApp().run()
