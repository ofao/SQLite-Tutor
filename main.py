from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
#from kivymd.uix.button import MDFlatButton
#from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatIconButton, MDIconButton, MDFlatButton
from kivymd.uix.card import MDCard
import sqlite3
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from board import *  #введение
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
#from kivy.uix.image import Image
from kivymd.uix.list import OneLineListItem
from kivy.uix.scrollview import ScrollView
#from kivymd.uix.fitimage import FitImage
from kivy.uix.image import Image
from kivymd.uix.navigationdrawer import (MDNavigationDrawer, MDNavigationDrawerMenu, MDNavigationLayout,
                                         MDNavigationDrawerItem, MDNavigationDrawerDivider, MDNavigationDrawerLabel,
                                         MDNavigationDrawerHeader)
from kivymd.uix.datatables import MDDataTable
Window.size = (650, 600) #https://github.com/Android-for-Python/Android-for-Python-Users#most-common-issues

class MyApp(MDApp):
    def __init__(self):
        super().__init__()
        self.title = "Электронная рабочая тетрадь SQLite"
        self.icon = 'database.png'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.theme_style_switch_animation = True
        
        self.screen = Screen()
        self.label = MDLabel(text = 'Рабочая тетрадь SQLite')
        #self.input = TextInput(hint_text = 'SQLite commands...', multiline = True)
        #b2e6f0
        self.grid = MDGridLayout(cols = 2, pos_hint = {'top': 1}, spacing = 20, size_hint_y = None, padding = 10)
        self.grid.bind(minimum_height = self.grid.setter('height'))
        self.scroll = ScrollView(size_hint=(1, None), size = (Window.width, Window.height * 0.9), bar_width = 10, bar_color = [0, 0, 255, 0.3],
                                 scroll_type = ['bars'], pos_hint = {'top': 0.9})
        self.lesson_scroll = ScrollView(size_hint=(1, None), bar_width = 10, size = (Window.width, Window.height * 0.9), bar_color = [0, 0, 255, 0.3],
                                 scroll_type = ['bars'], pos_hint = {'top': 0.9})
        
    def on_resize(self, obj, size):
        if size[0] <= 550:
            self.grid.cols = 1
        elif size[0] > 550 and size[0] <= 875:
            self.grid.cols = 2
        elif size[0] > 875 and size[0] <= 1250:
            self.grid.cols = 3
        elif size[0] > 1250:
            self.grid.cols = 4
        self.scroll.size = (size[0], size[1] * 0.9)
        self.lesson_scroll.size = (size[0], size[1] * 0.9)
        
    def build(self):
        global title, lesson, values
        title, lesson, values = [], [], []
        with open('темы.txt', 'r', encoding = 'utf8') as f:
            for line in f:
                title.append(line.split(' (')[0])
                a = line.split(' (')[1][:-2]
                lesson.append(a.split(', '))
        Window.bind(size = self.on_resize)  #привязка на изменение размерова окна
        cursor.execute('SELECT Значение from DATA where Тип="Обучение"')
        obuch_passed = cursor.fetchone()[0]
        cursor.execute('SELECT Значение from DATA where Тип="Тема"')
        self.theme_cls.theme_style = cursor.fetchone()[0]
        for i in range(len(title)):
            cursor.execute('SELECT Значение from DATA where Тип="{title[i]}"')
            if cursor.fetchone() == None:
                values.append(0)
            else:
                values.append(int(cursor.fetchone()))
        if obuch_passed == 'False':
            self.screen.add_widget(Onboarding())
        else:
            self.cards()
        return self.screen

    def cards(self):
        global title, lesson, values
        self.nav = Menu()
        self.screen.add_widget(MDBoxLayout(MDIconButton(icon = 'menu', on_release = lambda x: self.nav.set_state('open'),
                                                                 pos_hint = {'left': 0, 'top': 0.98})))
        self.nav_parent = MDNavigationLayout(self.nav)
        for i in range(len(title)):
            card = MD3Card(source = title[i] + ".png", value = values[i])
            self.text = lesson[i]
            self.num = len(lesson[i])
            panel = MDExpansionPanel(
                content = self.append(),
                panel_cls = MDExpansionPanelOneLine(text = title[i]))
            card.add_widget(panel)
            self.grid.add_widget(card)
        self.scroll.add_widget(self.grid)
        self.screen.add_widget(self.scroll)
        self.screen.add_widget(self.nav_parent)
        return self.screen  
        
    def append(self):
        box = MDBoxLayout(orientation = 'vertical', padding = 10, spacing = 10,
                          adaptive_height = True)
        for i in range(self.num):
            box.add_widget(OneLineListItem(text = self.text[i], on_release = self.panel_open))
        return box
       
    def panel_open(self, item):
        global title, lesson
        self.screen.clear_widgets()
        self.screen.add_widget(MDBoxLayout(MDIconButton(icon = 'arrow-left', on_release = self.back,
                                                                 pos_hint = {'left': 0, 'top': 0.98})))
        self.lesson_scroll.clear_widgets()
        box = MDBoxLayout(orientation = 'vertical', padding = 10, spacing = 10,
                          adaptive_height = True, size_hint_y = None, pos_hint = {'top': 1})
        for k in range(len(lesson)):
            if item.text in lesson[k]:
                break
        s = ''
        s2 = ''
        lbl = MDLabel(text = item.text, bold = True, font_size = 10, font_style = 'H6', adaptive_height = True, halign = 'center')  ##заголовок
        box.add_widget(lbl)
        with open(title[k] + '/' + item.text + '.txt', encoding = 'ANSI') as f:
            for line in f:
                if line.count('<<') > 0 or line.count('>>') > 0 or s2 != '':
                    if s != '':
                        s = s[:-1]  #убираем конечный enter (\n)
                        lbl = MDLabel(text = s, font_style = 'Body1', adaptive_height = True)
                        box.add_widget(lbl)
                        s = ''
                    if line.count('<<title>>') > 0 and s2 == '':
                        line = line.replace('<<title>>', '')
                        line = line.replace('\n', '')
                        lbl = MDLabel(text = line, bold = True, font_size = 10,
                                           font_style = 'H6', adaptive_height = True, halign = 'center')
                        box.add_widget(lbl)
                    elif line.count('<<picture>>') > 0 and s2 == '':
                        #from create import create_schema
                        line = line.replace('<<picture>>', '')
                        line = line.replace('\n', '')
                        lbl = Image(source = fr'{title[k]}\{line}', size_hint_min = (589, 272))
                        box.add_widget(lbl)
                        #box.add_widget(create_schema())
                    elif line.count('>>') > 0:
                        line = line.replace('<<', '')
                        line = line.replace('>>', '')
                        line = line.replace('\n', '')
                        s2 += line
                        inp = TextInp(text = s2)
                        box.add_widget(inp)
                        s2 = '' 
                    else:
                        line = line.replace('<<', '')
                        s2 += line
                else:
                    s += line
        self.lesson_scroll.add_widget(box)
        self.screen.add_widget(self.lesson_scroll)
        return self.screen
    
    def back(self, item):
        self.screen.clear_widgets()
        self.screen.add_widget(MDBoxLayout(MDIconButton(icon = 'menu', on_release = lambda x: self.nav.set_state('open'),
                                                                 pos_hint = {'left': 0, 'top': 0.98})))
        self.screen.add_widget(self.scroll)
        self.screen.add_widget(self.nav_parent)
        return self.screen
    
    def term(self):
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
    source = StringProperty()
    value = NumericProperty()
    
    def change_widget(self):
        myapp.screen.clear_widgets()

class TextInp(MDBoxLayout):
    text = StringProperty()

    def cop(self, text):
        import pyperclip
        pyperclip.copy(text)
        Snackbar(text = 'Текст скопирован').open()

    def cons(self):
        print(2)

class Menu(MDNavigationDrawer):
    def __init__(self):
        super().__init__()
        self.add_widget(MDNavigationDrawerMenu(MDNavigationDrawerHeader(title = "SQLite tutor", text = "", spacing = "4dp", padding = ("12dp", 0, 0, "56dp")),
                           MDNavigationDrawerLabel(text = "Помощь"),
                           MDNavigationDrawerItem(icon = "information", text = "Инструкция", on_release = self.info),
                           MDNavigationDrawerDivider(),
                           MDNavigationDrawerItem(text = "О программе", icon = "information", on_release = self.oprog)))
    
    def info(self, item):
        dialog('Для начала Вам необходимо выбрать раздел команд SQL, интересующий Вас, затем выбрать урок по необходимой команде. После прочтения теоретического материала, содержащегося в каждом уроке, Вам предлагается пройти блок проверки, в котором будут задания на выбор верных ответов или на самостоятельное вписывание команд. При прохождении последнего урока раздела Вам предлагается пройти тест по всему разделу.').open()

    def oprog(self, item):
        dialog('Программный продукт SQLite tutor был создан в рамках курсового проекта курсантом 331 группы Хачатрян О. А. Дата создания: 13.06.2023').open()
        
class dialog(MDDialog):
    def __init__(self, text):
        super().__init__()
        self.text = text
        
if __name__ == '__main__':
    myapp = MyApp()
    connection = sqlite3.connect('sq.db')
    cursor = connection.cursor()
    myapp.run()
    cursor.close()
    connection.close() 


