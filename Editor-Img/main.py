#import speech_recognition as sr

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup


class ImageOpener(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10)

        # Funcția pentru deschiderea File Explorer-ului și selectarea imaginii
        def open_image_selector(instance):
            try:
                file_chooser = FileChooserIconView()

                # Funcția care se execută când se selectează o imagine
                def select_image(path, filename):
                    image_path = path + '/' + filename[0]
                    show_image(image_path)

                file_chooser.bind(on_selection=select_image)

                popup = Popup(title='Selectează o imagine', content=file_chooser, size_hint=(0.8, 0.8))
                popup.open()
            except Exception as e:
                print("Eroare la deschiderea imaginii:", e)

        # Funcția pentru afișarea imaginii în fereastra aplicației
        def show_image(image_path):
            # Creează o fereastră pop-up pentru imagine
            image_popup = Popup(title='Imagine selectată', size_hint=(0.8, 0.8))

            # Adaugă imaginea la fereastra pop-up
            img = Image(source=image_path)
            image_popup.content = img

            # Afișează fereastra pop-up
            image_popup.open()

        # Butonul pentru a deschide File Explorer-ul și a selecta imaginea
        button = Button(text="Selectează Imaginea")
        button.bind(on_press=open_image_selector)
        layout.add_widget(button)

        return layout


if __name__ == '__main__':
    ImageOpener().run()

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


