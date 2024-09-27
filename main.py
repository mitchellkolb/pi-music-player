from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader

class AudioPlayerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Button to open and play the MP3
        play_button = Button(text="Play MP3")
        play_button.bind(on_press=self.play_audio)
        
        layout.add_widget(play_button)
        return layout
    
    def play_audio(self, instance):
        # Load and play the MP3 file
        sound = SoundLoader.load('path/to/your/file.mp3')
        if sound:
            sound.play()

if __name__ == "__main__":
    AudioPlayerApp().run()