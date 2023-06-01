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
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
#from kivy.uix.image import Image
from kivymd.uix.list import OneLineListItem
from kivy.uix.scrollview import ScrollView

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
        self.box = MDGridLayout(adaptive_width = True, cols = 2, pos_hint = {'top': 1})
        #self.box = MDBoxLayout(orientation = 'vertical', adaptive_height = True, spacing = 20, width = 800)
        self.scroll = ScrollView(bar_width = 10)
      
    def build(self):
        #self.icon = 'database.png'
        cursor.execute('SELECT Значение from DATA where Тип="Обучение"')
        obuch_passed = cursor.fetchone()[0]
        cursor.execute('SELECT Значение from DATA where Тип="Тема"')
        self.theme_cls.theme_style = cursor.fetchone()[0]
        if obuch_passed == 'False':
            self.screen.add_widget(Onboarding())
        else:
            self.cards()
        return self.screen

    def cards(self):
        title, lesson = [], []
        with open('темы.txt', 'r', encoding = 'utf8') as f:
            for line in f:
                title.append(line.split(' (')[0])
                a = line.split(' (')[1][:-2]
                lesson.append(a.split(', '))
        for i in range(len(title)):
            card = MD3Card(text = title[i])
            self.box.add_widget(card)
            '''
            self.text = lesson[i]
            self.num = len(lesson[i])
            panel = MDExpansionPanel(
                on_open = self.panel_open,
                on_close = self.panel_close,
                content = self.append(),
                panel_cls = MDExpansionPanelOneLine(text = title[i]))
            self.box.add_widget(panel)
        self.scroll.add_widget(self.box)
        self.screen.add_widget(self.scroll)'''
        self.screen.add_widget(self.box)
        return self.screen
    
    def append(self):
        box = MDBoxLayout(orientation = 'vertical', padding = 10, spacing = 10,
                          adaptive_height = True)
        for i in range(self.num):
            box.add_widget(OneLineListItem(text = self.text[i], on_release = self.panel_open))
        return box
       
    def panel_open(self, i):
        pass

    def panel_close(self, i):
        pass
        
class Onboarding(MDScreen):
    def finish_callback(self):
        myapp.screen.clear_widgets()
        cursor.execute('UPDATE DATA set Значение="True" where Тип="Обучение"')
        if myapp.theme_cls.theme_style == 'Dark':
            cursor.execute('UPDATE DATA set Значение="Dark" where Тип="Тема"')
        else:
            cursor.execute('UPDATE DATA set Значение="Light" where Тип="Тема"')
        connection.commit()
        myapp.cards()
        
    def change_theme(self):
        myapp.theme_cls.theme_style = (
                'Dark' if myapp.theme_cls.theme_style == 'Light' else 'Light')

class MD3Card(MDCard):
    text = StringProperty()

    def change_widget(self):
        myapp.screen.clear_widgets()
    
if __name__ == '__main__':
    myapp = MyApp()
    connection = sqlite3.connect('sq.db')
    cursor = connection.cursor()
    myapp.run()
    cursor.close()
    connection.close() 


