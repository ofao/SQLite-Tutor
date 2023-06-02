from kivymd.app import MDApp

from kivymd.uix.screen import Screen

from kivymd.uix.label import MDLabel

from kivy.uix.textinput import TextInput

#from kivymd.uix.button import MDFlatButton

#from kivymd.uix.textfield import MDTextField

from kivymd.uix.card import MDCard

import sqlite3, random

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

    def on_text(self, *args):

        try:

            connection = sqlite3.connect('sq.db')

            cursor = connection.cursor()

            cursor.close()

            connection.close()

            

        except Exception as e: print(e)

      

    def build(self):

        i = random.randint(0, 1)
        if i == 1:

            self.screen.add_widget(Onboarding())

        else:

            card1 = MD3Card(text = 'Реляционная алгебра')

            card2 = MD3Card(text = 'Тимка любимая попка')

            card3 = MD3Card(text = 'Я тебя люблюююю\nмилый')

            self.box.add_widget(card1)

            self.box.add_widget(card2)

            self.box.add_widget(card3)

            self.screen.add_widget(self.box)

        return self.screen

    

class Onboarding(MDScreen):

    def finish_callback(self):

        myapp.screen.remove_widget(self)

        card1 = MD3Card(text = 'Реляционная алгебра')

        card2 = MD3Card(text = 'Тимка любимая попка')

        card3 = MD3Card(text = 'Я тебя люблюююю\nмилый')

        myapp.box.add_widget(card1)

        myapp.box.add_widget(card2)

        myapp.box.add_widget(card3)

        myapp.screen.add_widget(myapp.box)

        

    def change_theme(self):

        myapp.theme_cls.theme_style = (

                'Dark' if myapp.theme_cls.theme_style == 'Light' else 'Light')

class MD3Card(MDCard):

    text = StringProperty()

    def change_widget(self):

        pass

if __name__ == '__main__':

    myapp = MyApp()

    myapp.run()
 
  


