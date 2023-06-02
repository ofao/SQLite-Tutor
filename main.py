from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
#from kivymd.uix.button import MDFlatButton
#from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
import sqlite3
from board import *  #введение
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image

class MyApp(MDApp):
    def __init__(self):
        super().__init__()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'

        self.theme_cls.theme_style_switch_animation = True
        
        self.screen = Screen()
        self.label = MDLabel(text = 'Рабочая тетрадь SQLite')
        #self.input = TextInput(hint_text = 'SQLite commands...', multiline = True)
        #b2e6f0
        self.box = MDBoxLayout(adaptive_size = True, spacing = 15, pos_hint = {'top': 1})
      
    def build(self):
        self.screen.add_widget(self.label)
        return self.screen
    
if __name__ == '__main__':
    myapp = MyApp()
    myapp.run()

