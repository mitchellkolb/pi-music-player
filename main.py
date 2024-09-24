from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
import pygame

class MP3PlayerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # File chooser to select MP3
        self.file_chooser = FileChooserIconView(filters=['*.mp3'])
        self.layout.add_widget(self.file_chooser)

        # Play button
        self.play_button = Button(text="Play Selected MP3")
        self.play_button.bind(on_press=self.play_mp3)
        self.layout.add_widget(self.play_button)

        # Initialize Pygame mixer
        pygame.mixer.init()

        return self.layout

    def play_mp3(self, instance):
        selected_file = self.file_chooser.selection
        if selected_file:
            pygame.mixer.music.load(selected_file[0])
            pygame.mixer.music.play()

if __name__ == '__main__':
    MP3PlayerApp().run()
