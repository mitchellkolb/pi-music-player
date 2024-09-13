import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class BruhApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')  # Create a BoxLayout
        label = Label(text='Bruh', font_size=50)    # Create a label with the text "Bruh"
        layout.add_widget(label)                    # Add the label to the layout
        return layout                              # Return the layout as the root widget

if __name__ == '__main__':
    BruhApp().run()
