#import speech_recognition as sr

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
import os


# class FileExplorerPopup(Popup):
#     def __init__(self, **kwargs):
#         super(FileExplorerPopup, self).__init__(**kwargs)
#         self.title = "Choose a Photo"
#         self.size_hint = (0.9, 0.9)
#         self.file_chooser = FileChooserListView()
#         self.file_chooser.path = os.path.expanduser('~')  # Set initial path to user's home directory
#         self.file_chooser.filters = ['*.png', '*.jpg', '*.jpeg']  # Filter for image files
#         self.file_chooser.bind(selection=self.selected)
#         self.content = self.file_chooser
#
#     def selected(self, chooser, selection):
#         if selection:
#             self.selected_file = selection[0]
#             self.dismiss()
#             self.show_image()
#
#     def show_image(self):
#         if hasattr(self, 'selected_file'):
#             image_layout = BoxLayout(orientation='vertical')
#             image = Image(source=self.selected_file, allow_stretch=True)
#             close_button = Button(text="Close")
#             close_button.bind(on_press=self.dismiss_image)
#             image_layout.add_widget(image)
#             image_layout.add_widget(close_button)
#             self.image_popup = Popup(title="View Image", content=image_layout, size_hint=(0.9, 0.9))
#             self.image_popup.open()
#
#     def dismiss_image(self, instance):
#         self.image_popup.dismiss()
#
#
# class FileExplorerApp(App):
#     def build(self):
#         layout = BoxLayout(orientation='vertical')
#         button = Button(text="Open File Explorer")
#         button.bind(on_press=self.open_file_explorer)
#         layout.add_widget(button)
#         return layout
#
#     def open_file_explorer(self, instance):
#         file_explorer = FileExplorerPopup()
#         file_explorer.open()
#
#
# if __name__ == '__main__':
#     FileExplorerApp().run()

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


## editarea luminozitatii
# import speech_recognition as sr
# from PIL import Image, ImageEnhance
#
# def process_image(command):
#     # Load the image you want to edit
#     img = Image.open("D:\\Anul4sem1\\IOM\\free-nature-images.jpg")
#
#     # Print the words for debugging
#     print("Words:", command.split())
#
#     # Voice editing commands
#     if "pateul" in command and ("crește" in command or "scade" in command):
#         words = command.split()
#         try:
#             brightness_index = next(i for i, word in enumerate(words) if word.isdigit() or (word.replace('.', '', 1).isdigit() and '.' in word))
#             brightness = float(words[brightness_index].replace(",", "."))  # Replace "," with "." for proper float conversion
#             if "scade" in words:
#                 brightness = -brightness  # Make the brightness negative for decrease command
#
#             enhancer = ImageEnhance.Brightness(img)
#             img = enhancer.enhance(1.0 + brightness)
#             img.show()  # Display the modified image
#         except (ValueError, IndexError):
#             print("Valoarea luminozității nu este validă.")
#     else:
#         print("Comanda vocală nu este recunoscută sau nu conține valoarea luminozității.")
#
#     # Save the edited image
#     img.save("D:\\Anul4sem1\\IOM\\edited_image.jpg")
#     print("Imagine editată și salvată.")
#
# def recognize_speech():
#     recognizer = sr.Recognizer()
#
#     with sr.Microphone() as source:
#         print("Aștept comanda vocală...")
#         audio = recognizer.listen(source)
#
#         try:
#             # Use Google Speech Recognition to convert the recording to text
#             command = recognizer.recognize_google(audio, language='ro-RO')  # Choose the appropriate language
#
#             print("Comanda vocală recunoscută:", command)
#             process_image(command)
#
#         except sr.UnknownValueError:
#             print("Nu s-a putut recunoaște comanda vocală.")
#         except sr.RequestError as e:
#             print("Eroare în obținerea rezultatelor; {0}".format(e))
#
# if _name_ == "_main_":
#     recognize_speech()

# aplicarea filtrului alb-negru
from PIL import Image
import speech_recognition as sr

def process_image(command):
    # Încarcă imaginea pe care dorești să aplici filtrul alb-negru
    img = Image.open("C:/Users/anca2/Desktop/4e45eb7765daa615a06c0f738f5eb125.jpg")

    # Verifică comanda vocală pentru aplicarea filtrului alb-negru
    if "alb negru" in command.lower():
        # Converteste imaginea in alb-negru
        img = img.convert("L")
        img.show()  # Afișează imaginea modificată în fereastră

        # Salvează imaginea modificată
        img.save("C:/Users/anca2/Desktop/4e45eb7765daa615a06c0f738f5eb125.jpg")
        print("Imaginea alb-negru a fost salvată.")

    else:
        print("Comanda vocală nu a fost recunoscută sau nu este pentru aplicarea filtrului alb-negru.")

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Ascultă comanda vocală...")
        audio = recognizer.listen(source)

        try:
            # Converteste în text comanda vocală utilizând Google Speech Recognition
            command = recognizer.recognize_google(audio, language='ro-RO')  # Limba română

            print("Comanda vocală recunoscută:", command)
            process_image(command)

        except sr.UnknownValueError:
            print("Nu s-a putut recunoaște comanda vocală.")
        except sr.RequestError as e:
            print("Eroare în obținerea rezultatelor; {0}".format(e))

if __name__ == "__main__":
    recognize_speech()
