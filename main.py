from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen, Screen
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
Builder.load_string("""
<MyAKOnboardingItem@AKOnboardingItem>
    source: ""
    text: ""
    title: ""

    MDFloatLayout:

        Image:
            source: root.source
            pos_hint: {"center_x": .5, "y": .6}
            size_hint: .4, .3

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(10)
            adaptive_height: True
            pos_hint: {"center_x": .5, "top": .5}
            spacing: dp(20)
            size_hint_x: .7

            canvas.before:
                Color:
                    rgba: app.theme_cls.primary_dark
                RoundedRectangle:
                    pos: self.pos
                    size: self.size

            MDLabel:
                text: root.title
                bold: True
                size_hint_y: None
                height: self.texture_size[1]
                theme_text_color: "Primary"
                font_style: "H6"
                halign: "center"
                valign: "center"

            MDLabel:
                size_hint_y: None
                height: self.texture_size[1]
                theme_text_color: "Primary"
                font_style: "Body1"
                halign: "center"
                valign: "center"
                text: root.text


<Onboarding>
    name: "Onboarding"
    on_leave: boarding.reset()

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(10)

        AKOnboarding:
            id: boarding
            on_finish: root.finish_callback()
            circles_size: dp(15)

            MyAKOnboardingItem:
                text:
                    "Это интерактивное учебное средство комплексного назначения, " \
                    "являющееся частью образовательного ресурса по дисциплине"
                title:"Электронная рабочая тетрадь"

            MyAKOnboardingItem:
                text:
                    "Это система управления базами данных (СУБД), которая не имеет " \
                    "сервера и позволяет хранить всю базу локально на одном устройстве"
                title: "SQLite"

            MyAKOnboardingItem:
                text:
                    "Поможет вам в изучении SQLite." \
                    "Желаем успехов!"
                title: "Эта программа"
""")

class MyApp(MDApp):
    def __init__(self):
        super().__init__()
        self.label = MDLabel(text = 'Рабочая тетрадь SQLite')
        #self.input = TextInput(hint_text = 'SQLite commands...', multiline = True)
        self.button = MDRoundFlatButton(text = 'OK', on_release = self.text)#b2e6f0
        '''
        self.board = AKOnboarding(orientation = 'vertical')
        self.box = BoxLayout()
        self.box.add_widget(self.label)
        self.board.ids.carousel.add_widget(self.box)
        #self.board.ids.carousel.add_widget(self.box)
        self.board2 = BoxLayout()
        self.board2.add_widget(Image(source='SQLite.png'))
        self.board.ids.carousel.add_widget(self.board2)'''
        
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

        return OnBoarding()
    
class OnBoarding(MDScreen):
    def finish_callback(self):
        print("yjngh")
        
if __name__ == '__main__':   
    MyApp().run()

