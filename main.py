from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
#from kivymd.uix.button import MDFlatButton
#from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatButton, MDFillRoundFlatButton
import sqlite3
from board import *  #введение
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

class MyApp(MDApp):
    def __init__(self):
        super().__init__()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'

        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 1
        
        self.screen = Screen()
        self.label = MDLabel(text = 'Рабочая тетрадь SQLite')
        #self.input = TextInput(hint_text = 'SQLite commands...', multiline = True)
        self.button = MDFillRoundFlatButton(text = 'Theme', on_release = self.on_text)#b2e6f0
        self.board = OnBoarding()
        
    def on_text(self, *args):
        try:
            connection = sqlite3.connect('sq.db')
            cursor = connection.cursor()
            cursor.close()
            connection.close()
            self.theme_cls.theme_style = (
                'Dark' if self.theme_cls.theme_style == 'Light' else 'Light')
            try:
                self.refresh_callback()
            except: pass
        except Exception as e: print(e)
      
    def build(self):
        self.screen.add_widget(self.board)
        return self.screen
    
class OnBoarding(MDScreen):
    def finish_callback(self):
        myapp.screen.remove_widget(myapp.board)
        myapp.screen.add_widget(myapp.button)
        
if __name__ == '__main__':
    myapp = MyApp()
    myapp.run()


