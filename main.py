import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.core.audio import SoundLoader
from kivy.config import Config


class AudioPlayerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # Spinner to list MP3 files in the 'songs/' folder
        self.songs_dir = 'songs/'
        self.song_files = [f for f in os.listdir(self.songs_dir) if f.endswith('.mp3')]
        self.spinner = Spinner(text="Select MP3", values=self.song_files)
        self.layout.add_widget(self.spinner)
        
        # Play/Pause button
        self.play_button = Button(text="Play")
        self.play_button.bind(on_press=self.toggle_play)
        self.layout.add_widget(self.play_button)
        
        # Volume slider
        self.volume_label = Label(text="Volume: 50%")
        self.volume_slider = Slider(min=0, max=1, value=0.5)
        self.volume_slider.bind(value=self.adjust_volume)
        self.layout.add_widget(self.volume_label)
        self.layout.add_widget(self.volume_slider)
        
        self.sound = None  # To hold the current sound object
        return self.layout
    
    def toggle_play(self, instance):
        if self.sound and self.sound.state == 'play':
            self.sound.stop()
            self.play_button.text = "Play"
        else:
            song_path = os.path.join(self.songs_dir, self.spinner.text)
            self.sound = SoundLoader.load(song_path)
            if self.sound:
                self.sound.volume = self.volume_slider.value
                self.sound.play()
                self.play_button.text = "Pause"
    
    def adjust_volume(self, instance, value):
        self.volume_label.text = f"Volume: {int(value * 100)}%"
        if self.sound:
            self.sound.volume = value

if __name__ == "__main__":
    AudioPlayerApp().run()
