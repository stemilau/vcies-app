#import speech_recognition as sr

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
import os


class FileExplorerPopup(Popup):
    def __init__(self, **kwargs):
        super(FileExplorerPopup, self).__init__(**kwargs)
        self.title = "Choose a Photo"
        self.size_hint = (0.9, 0.9)
        self.file_chooser = FileChooserListView()
        self.file_chooser.path = os.path.expanduser('~')  # Set initial path to user's home directory
        self.file_chooser.filters = ['*.png', '*.jpg', '*.jpeg']  # Filter for image files
        self.file_chooser.bind(selection=self.selected)
        self.content = self.file_chooser

    def selected(self, chooser, selection):
        if selection:
            self.selected_file = selection[0]
            self.dismiss()
            self.show_image()

    def show_image(self):
        if hasattr(self, 'selected_file'):
            image_layout = BoxLayout(orientation='vertical')
            image = Image(source=self.selected_file, allow_stretch=True)
            close_button = Button(text="Close")
            close_button.bind(on_press=self.dismiss_image)
            image_layout.add_widget(image)
            image_layout.add_widget(close_button)
            self.image_popup = Popup(title="View Image", content=image_layout, size_hint=(0.9, 0.9))
            self.image_popup.open()

    def dismiss_image(self, instance):
        self.image_popup.dismiss()


class FileExplorerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        button = Button(text="Open File Explorer")
        button.bind(on_press=self.open_file_explorer)
        layout.add_widget(button)
        return layout

    def open_file_explorer(self, instance):
        file_explorer = FileExplorerPopup()
        file_explorer.open()


if __name__ == '__main__':
    FileExplorerApp().run()

# # Creăm un obiect Recognizer pentru a efectua recunoașterea vocală
# recognizer = sr.Recognizer()
#
# # Utilizăm microfonul pentru a înregistra sunetul
# with sr.Microphone() as source:
#     print("Vorbiți acum...")
#     audio = recognizer.listen(source)
#
#     try:
#         # Folosim Google Speech Recognition pentru a converti înregistrarea în text
#         text = recognizer.recognize_google(audio, language='ro-RO') # Alege limba corespunzătoare
#
#         print("Textul recunoscut: ", text)
#
#     except sr.UnknownValueError:
#         print("Nu s-a putut recunoaște textul.")
#     except sr.RequestError as e:
#         print("Eroare în obținerea rezultatelor; {0}".format(e))


