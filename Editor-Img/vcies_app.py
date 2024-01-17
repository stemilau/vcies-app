import os.path
from io import BytesIO
import time
import speech_recognition as sr
from PIL import Image, ImageEnhance, ImageFilter
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem
from kivy.core.image import Image as CoreImage

# Set window size to match screen resolution
Config.set('graphics', 'width', '0')
Config.set('graphics', 'height', '0')

# Set the window to be maximized
Window.maximize()

# Set global variable to pass image path data between classes
global path_to_photo

class ImageProcessor:
    op = ""
    recognized_speech = ""
    image = Image.open(r"Empty.png")
    def __init__(self,input_image):
        self.image = input_image
    def rotate_image_to_the_left(self, image):
        return image.transpose(Image.ROTATE_270)
    def rotate_image_to_the_right(self, image):
        return image.transpose(Image.ROTATE_90)
    def process_image(self, command):
        img = self.image
        #Aplica alb-negru -> "alb negru"
        #Aplica blur -> "blur"
        #Crop -> "crop stanga 50 dreapta 100 sus 300 jos 500"
        #Luminozitate -> "luminozitatea creste cu 1 punct 5"
        #              -> "luminozitatea creste cu 1"
        #              -> "luminozitatea creste cu 1 punct 2"
        #Rotire stange -> "rotire stanga"
        #Rotire dreapta -> "rotire dreapta"

        #Aplicarea filtrului alb-negru
        if "alb negru" in command.lower():
            img = img.convert("LA")
            self.image = img
            self.op = "alb negru"

        #Aplicarea filtrului de blur
        elif "blur" in command.lower():
            img = img.filter(ImageFilter.BLUR)
            self.image = img
            self.op = "blur"

        #Aplicare crop
        elif any(keyword in command.lower() for keyword in ["crop", "tăie", "selectează"]):
            try:
                words = command.lower().split()
                left_index = words.index("stânga")
                top_index = words.index("sus")
                right_index = words.index("dreapta")
                bottom_index = words.index("jos")

                left = int(words[left_index + 1])
                top = int(words[top_index + 1])
                right = int(words[right_index + 1])
                bottom = int(words[bottom_index + 1])

                img = img.crop((left, top, right, bottom))
                self.image = img
                self.op = "crop"

            except (ValueError, IndexError):
                print("Comanda de crop nu este valida.")

        #Schimbarea luminozitatii
        elif "luminozitatea" in command and ("crește" in command or "scade" in command):
            words = command.split()
            try:
                brightness_index = next(i for i, word in enumerate(words) if
                                        word.isdigit() or (word.replace('.', '', 1).isdigit() and '.' in word))
                brightness = float(words[brightness_index].replace(",", "."))
                if "scade" in words:
                    brightness = -brightness

                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.0 + brightness)
                self.image = img
                self.op = "luminozitate"

            except (ValueError, IndexError):
                print("Valoarea luminozității nu este validă.")

        #Rotirea imaginii
        elif "rotire stânga" in command:
            imagine_rotita = self.rotate_image_to_the_left(img)
            self.image = imagine_rotita
            self.op = "rotire stanga"

        elif "rotire dreapta" in command:
            imagine_rotita = self.rotate_image_to_the_left(img)
            self.image = imagine_rotita
            self.op = "rotire dreapta"
        else:
            print("Comanda necunoscuta.")
    def recognize_and_process(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Ascultă comanda vocală...")
            audio = recognizer.listen(source)
            time.sleep(1)
            try:
                command = recognizer.recognize_google(audio, language='ro-RO')
                print("Comanda vocală recunoscută:", command)
                self.recognized_speech = command
                self.process_image(command)

            except sr.UnknownValueError:
                self.recognized_speech = "Unknown Value Error"
                print("Nu s-a putut recunoaște comanda vocală.")

            except sr.RequestError as e:
                self.recognized_speech = "Request Error"
                print(f"Eroare în obținerea rezultatelor; {e}")
    def get_processed_image(self):
        return self.image
    def get_executed_op(self):
        return self.op
    def get_recognized_speech(self):
        return self.recognized_speech

class PhotoExplorerPopup(Popup):
    def selected(self,filename):
        self.ids.preview_photo.source = filename[0]
    def select_photo_button_press(self, filename):
        global path_to_photo
        path_to_photo = filename[0]
        self.dismiss()
    def get_default_path(self):
        self.default_path = os.path.expanduser("~/Desktop")
        return self.default_path

class StartWindow(Screen):
    def __init__(self, **kwargs):
        super(StartWindow, self).__init__(**kwargs)
    def start_editing_button_press(self):
        file_explorer = PhotoExplorerPopup()
        file_explorer.open()

class OperationEntry(OneLineListItem):
    def __init__(self, op, **kwargs):
        super(OperationEntry, self).__init__(**kwargs)
        self.text = op

class EditingWindow(Screen):
    image = Image.open(r"Empty.png")
    counter_ops = 1
    def __init__(self, **kwargs):
        super(EditingWindow, self).__init__(**kwargs)

    def load_photo(self):
        global path_to_photo
        self.image = Image.open(path_to_photo)
        self.ids.display_photo.source = path_to_photo

    def add_operation(self,data):
        data = "Op. " + str(self.counter_ops) + ": " + data
        self.counter_ops = self.counter_ops + 1
        op = OperationEntry(data)
        self.ids.history.add_widget(op)

    def listen_and_exec_op(self):
        image_processor = ImageProcessor(self.image)
        image_processor.recognize_and_process()

        self.ids.feedback_label.text = image_processor.get_recognized_speech()

        operation = image_processor.get_executed_op()
        self.add_operation(operation)

        self.image = image_processor.get_processed_image()

        img_data = BytesIO()
        self.image.save(img_data, format='png')
        img_data.seek(0)
        im = CoreImage(BytesIO(img_data.read()), ext='png')
        self.ids.display_photo.texture = im.texture

class WindowManager(ScreenManager):
    pass

# this must be declared after the Window Manager Class declaration
kv_builder_instance = Builder.load_file('vcies_gui_design.kv')

class VCIESApp(MDApp):
    def build(self):
        return kv_builder_instance

if __name__ == '__main__':
    VCIESApp().run()