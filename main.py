from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
#from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatButton, MDFillRoundFlatButton
from kivy.core.window import Window
import sqlite3
from kivymd_extensions.akivymd.uix.onboarding import *  #для красивых переходов и множества красивых виджетов
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

Window.size = (250, 250)
Window.title = 'MyApp'
Window.clearcolor = (1, 0, 0, 1)    # установка цвета нового фона

class MyApp(MDApp):
    def __init__(self):
        super().__init__()
        self.label = MDLabel(text = 'Рабочая тетрадь SQLite')
        #self.input = TextInput(hint_text = 'SQLite commands...', multiline = True)
        #self.button = MDRoundFlatButton(text = 'OK', on_release = self.text)#b2e6f0
        self.board = AKOnboarding(orientation = 'vertical')
        self.box = BoxLayout()
        self.box.add_widget(self.label)
        self.board.ids.carousel.add_widget(self.box)
        self.board2 = BoxLayout()
        #self.board2.add_widget(Image(source='SQLite.png'))
        self.board.ids.carousel.add_widget(self.board2)
        
    def text(self, *args):
        try:
            connection = sqlite3.connect('sq.db')
            cursor = connection.cursor()
            cursor.executescript(self.input.text)
            connection.commit()
            cursor.close()
            print('yes')
        except Exception as e: print(e)
      
    def build(self):
        screen = Screen()
        #screen.add_widget(self.label)
        #screen.add_widget(self.input)
        #screen.add_widget(self.button)
        screen.add_widget(self.board)

        return screen
    
if __name__ == '__main__':   
    MyApp().run()
