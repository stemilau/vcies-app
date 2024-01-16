import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window

# Set window size to match screen resolution
Config.set('graphics', 'width', '0')
Config.set('graphics', 'height', '0')

# Set the window to be maximized
Window.maximize()

# Set global variable to pass image path data between classes
global path_to_photo
path_to_photo = ""

class PhotoExplorerPopup(Popup):
    def selected(self,filename):
        self.ids.preview_photo.source = filename[0]
    def select_photo_button_press(self, filename):
        global path_to_photo
        path_to_photo = filename[0]
        self.dismiss()


class StartWindow(Screen):
    def __init__(self, **kwargs):
        super(StartWindow, self).__init__(**kwargs)
    def start_editing_button_press(self):
        file_explorer = PhotoExplorerPopup()
        file_explorer.open()


class EditingWindow(Screen):
    def __init__(self, **kwargs):
        super(EditingWindow, self).__init__(**kwargs)

    def load_photo(self):
        global path_to_photo
        print(path_to_photo)
        self.ids.target_photo.source = path_to_photo
    def history_revert_button_press(self):
        pass

class WindowManager(ScreenManager):
    pass

# this must be declared after the Window Mangaer Class declaration
kv_builder_instance = Builder.load_file('vcies_gui_design.kv')

class VCIESApp(App):
    def build(self):
        return kv_builder_instance

if __name__ == '__main__':
    VCIESApp().run()