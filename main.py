from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
#from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatIconButton, MDIconButton, MDFlatButton, MDFloatingActionButton, MDRectangleFlatButton
from kivymd.uix.card import MDCard
import sqlite3
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
#from board import *  #введение
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.list import OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.fitimage import FitImage
from kivy.uix.image import Image
from kivymd import images_path
from kivymd_extensions.akivymd.uix.onboarding import *
from kivymd.uix.navigationdrawer import (MDNavigationDrawer, MDNavigationDrawerMenu, MDNavigationLayout,
                                         MDNavigationDrawerItem, MDNavigationDrawerDivider, MDNavigationDrawerLabel,
                                         MDNavigationDrawerHeader)
from kivymd.uix.datatables import MDDataTable
###ИМПОРТЫ ДЛЯ МОБИЛЬНОЙ ВЕРСИИ - АНДРОИД
#from android.permissions import Parmission, request_permissions
#from android.storage import primary_external_storage_path
import xml.etree.ElementTree as ET #ЧТЕНИЕ XML ФАЙЛОВ
#https://iconscout.com/lottie-animation/win-10290126 
Builder.load_string("""
<MyAKOnboardingItem@AKOnboardingItem>
    source: ""
    text: ""
    title: ""

    MDFloatLayout:

        Image:
            source: root.source
            pos_hint: {"center_x": .5, "y": .6}
            size_hint: .5, .4

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(10)
            adaptive_height: True
            pos_hint: {"center_x": .5, "top": .5}
            spacing: dp(20)
            size_hint_x: .7

            MDLabel:
                text: root.title
                bold: True
                size_hint_y: None
                height: self.texture_size[1]
                theme_text_color: "Custom"
                text_color: app.theme_cls.text_color
                font_style: "H6"
                halign: "center"
                valign: "center"

            MDLabel:
                size_hint_y: None
                height: self.texture_size[1]
                theme_text_color: "Custom"
                text_color: app.theme_cls.text_color
                font_style: "Body1"
                halign: "center"
                valign: "center"
                text: root.text


<Onboarding>:
    name: "Onboarding"
    on_leave: boarding.reset()
    
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(10)

        AKOnboarding:
            id: boarding
            on_finish: root.finish_callback()
            circles_size: dp(15)
            skip_button: False
            
            MyAKOnboardingItem:
                source: "desk.png"
                text:
                    "Это интерактивное учебное средство комплексного назначения, " \
                    "являющееся частью образовательного ресурса по дисциплине"
                title:"Электронная рабочая тетрадь"

            MyAKOnboardingItem:
                source: "SQLite.png"
                text:
                    "Это система управления базами данных (СУБД), которая не имеет " \
                    "сервера и позволяет хранить всю базу локально на одном устройстве"
                title: "SQLite"

            AKOnboardingItem:
                MDFloatLayout:
                    Image:
                        source: "dark2light.png"
                        pos_hint: {"center_x": .5, "y": .6}
                        size_hint: .5, .4

                    MDBoxLayout:
                        orientation: "vertical"
                        padding: dp(10)
                        adaptive_height: True
                        pos_hint: {"center_x": .5, "top": .5}
                        spacing: dp(20)
                        size_hint_x: .7

                        MDLabel:
                            text: "Выберите тему приложения"
                            bold: True
                            size_hint_y: None
                            height: self.texture_size[1]
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.text_color
                            font_style: "H6"
                            halign: "center"
                            valign: "center"
                            
                        MDIconButton:
                            icon: 'weather-night' if app.theme_cls.theme_style=='Dark' else 'weather-sunny'
                            icon_size: '64sp'
                            theme_icon_color: "Custom"
                            icon_color: app.theme_cls.text_color
                            size_hint: None, None
                            pos_hint: {'center_x': .5}
                            on_release: root.change_theme()

<MD3Card>:
    size_hint: 1, None
    size: "300dp", "300dp"
    md_bg_color: [0, 0, 0, 0.05]
    border_radius: 20
    radius: [15]
    orientation: "vertical"

    FitImage:
        source: root.source

    MDProgressBar:
        size_hint_y: 0.1
        value: root.value
        
<TextInp>:
    size_hint: 1, None

    MDTextFieldRect:
        id: tex
        text: root.text
        multiline: True
        size_hint: .9, None
        scroll_from_swipe: True
        readonly: True
        background_color: [0, 0, 0, 0.1]
        border: [4, 4, 4, 4]
        #height: (len(self._lines) + 1) * self.line_height

    MDIconButton:
        text: " "
        icon: "play"
        canvas.before:
            Color:
                rgba: app.theme_cls.primary_color
            Line:
                width: 1
                circle: (self.center_x, self.center_y, min(self.width, self.height) / 2)
        theme_icon_color: "Custom"
        icon_color: app.theme_cls.primary_color
        pos_hint: {'right': 1, 'top': 1}
        on_release: root.cons(tex)

<Terminal>:
    obuch: root.obuch
    pos_hint: {'top': 0.9}
    orientation: 'vertical'
    adaptive_height: True
    size_hint: 1, None
    spacing: 10
    padding: 10

    MDLabel:
        text: root.text_label
        multiline: True
        size_hint: 1, None
        adaptive_height: True
        height: 10
        
    MDTextFieldRect:
        id: textinp
        text: root.text
        multiline: True
        background_color: [0, 0, 0, 0.1]
        scroll_from_swipe: True
        size_hint: 1, None
        adaptive_height: True
        #height: (len(self._lines) + 1) * self.line_height

    MDRectangleFlatButton:
        text: 'Готово'
        size_hint: 1, None
        on_release: root.check(textinp, lbl, root.obuch)
        md_border_color: [0, 0, 0, 0.1]
        
    MDLabel:
        id: lbl
        text: ''
        height: 10
        multiline: True
        size_hint: 1, None
        adaptive_height: True
    
""")

#Window.size = (350, 600)

class MyApp(MDApp):                                                                                 #Класс главного окна
    def __init__(self):
        super().__init__()
        self.title = "Электронная рабочая тетрадь SQLite"                                           #Изменение заголовка окна
        self.icon = 'database.png'                                                                  #Изменение иконки окна
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.theme_style_switch_animation = True
        
        self.screen = MDScreen()
        
        self.grid = MDGridLayout(cols = 2, pos_hint = {'top': 1}, spacing = 20, size_hint_y = None, padding = 10)
        self.grid.bind(minimum_height = self.grid.setter('height'))
        self.scroll = ScrollView(size_hint=(1, None), size = (Window.width, Window.height * 0.9), scroll_type = ['content'], pos_hint = {'top': 0.9})
        self.lesson_scroll = ScrollView(size_hint=(1, None), size = (Window.width, Window.height * 0.9), scroll_type = ['content'], pos_hint = {'top': 0.9})
        
        #self.on_resize('a', Window.size)

    def on_resize(self, obj, size):                                                                 #Функция, реагирующая на изменение размеров окна
        if size[0] <= 630:
            self.grid.cols = 1
        elif size[0] > 630 and size[0] <= 875:
            self.grid.cols = 2
        elif size[0] > 875 and size[0] <= 1250:
            self.grid.cols = 3
        elif size[0] > 1250:
            self.grid.cols = 4
        self.scroll.size = (size[0], size[1] * 0.9)
        self.lesson_scroll.size = (size[0], size[1] * 0.9)
        
    def build(self):                                                                                #Функция, которая вызывается 1 раз при запуске программы
        global title, lesson, values
        Window.bind(size = self.on_resize)                                                          #привязка на изменение размеров окна
        #self.grid.cols = 2 #в мобильной версии 2 столбца
        #self.scroll.size = (Window.width, Window.height * 0.9)
        #self.lesson_scroll.size = (Window.width, Window.height * 0.9)
        self.on_resize('a', Window.size)
        try:
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
        except:
            obuch_passed = 'False'
            values = [0, 0, 0, 0, 0, 0]
        if obuch_passed == 'False':                                                                 #Если первый запуск программы, то будет показано приветствующее окно
            self.screen.add_widget(Onboarding())
        else:
            self.cards()
        return self.screen

    def cards(self):                                                                                #Функция, которая вызывается в случае, когда окно приветствия пройдено
        global title, lesson, values
        self.nav = Menu()
        self.screen.add_widget(MDBoxLayout(MDIconButton(icon = 'menu', on_release = lambda x: self.nav.set_state('open'),
                                                                 pos_hint = {'left': 0, 'top': 0.98})))
        self.nav_parent = MDNavigationLayout(self.nav)
        for i in range(len(title)):
            card = MD3Card(source = str(i + 1) + ".png", value = values[i])
            self.text = lesson[i]
            self.num = len(lesson[i])
            panel = MDExpansionPanel(
                content = self.append(),
                panel_cls = MDExpansionPanelOneLine(text = title[i]))
            panel.opening_transition = 'out_sine'
            card.add_widget(panel)
            self.grid.add_widget(card)
        self.scroll.add_widget(self.grid)
        self.screen.add_widget(self.scroll)
        self.screen.add_widget(self.nav_parent)
        return self.screen  
        
    def append(self):                                                                               #Функция добавления уроков в раздел
        box = MDBoxLayout(orientation = 'vertical', padding = 10, spacing = 10,
                          adaptive_height = True)
        for i in range(self.num):
            box.add_widget(OneLineListItem(text = self.text[i], on_release = self.panel_open))
        return box
       
    def panel_open(self, item):                                                                     #Функция, которая вызывается на открытие раздела, открывает список уроков
        global title, lesson
        self.screen.clear_widgets()
        self.screen.add_widget(MDBoxLayout(MDIconButton(icon = 'arrow-left', on_release = lambda x: self.back('to cards'),
                                                                 pos_hint = {'left': 0, 'top': 0.98})))
        self.lesson_scroll.clear_widgets()
        box = MDBoxLayout(orientation = 'vertical', padding = 10, spacing = 10,
                          adaptive_height = True, size_hint_y = None, pos_hint = {'top': 1})
        for k in range(len(lesson)):
            if item.text in lesson[k]:
                j = lesson[k].index(item.text)
                break
        s = ''
        s2 = ''
        lbl = MDLabel(text = item.text, bold = True, font_size = 10, font_style = 'H6', adaptive_height = True, halign = 'center')  ##заголовок
        box.add_widget(lbl)
        try:
            tree = ET.parse(str(k + 1) + '/' + str(j + 1) + '.xml')
            root = tree.getroot()
            for elem in root.iter():
                box.add_widget(MDLabel(text = str(elem.tag) + ' ' + str(elem.attrib), font_style = 'Body1', adaptive_height = True))
                print(elem.tag, elem.attrib)
            '''
            with open(str(k + 1) + '/' + str(j + 1) + '.pickle', 'rb') as f:
                lines = pickle.load(f)
                for line in lines:
                    if line.count('<<') > 0 or line.count('>>') > 0 or s2 != '':
                        if s != '':
                            s = s[:-1]                                                                  #убираем конечный enter (\n)
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
                            try:
                                lbl = Image(source = fr'{k + 1}/{line}', size_hint_y = None)
                                if Window.width < lbl.texture_size[0]:
                                    lbl.height = lbl.texture_size[1] / (lbl.texture_size[0] / Window.width)
                                else:
                                    lbl.height = lbl.texture_size[1] * (Window.width/lbl.texture_size[0])
                                lbl.width = Window.width
                                #lbl.bind(on_touch_move = self.images_open)
                                box.add_widget(lbl)
                            except Exception as e: box.add_widget(MDLabel(text = 'Width: ' + str(Window.width) + ' Picture size: ' + str(lbl.texture_size) +
                                                                          ' Norm size: ' + str(lbl.norm_image_size) + ' Exception: ' + str(e)))
                            #box.add_widget(create_schema())
                        elif line.count('<<answer>>') > 0 and s2 == '':
                            line = line.replace('\n', '')
                            self.answer = line.replace('<<answer>>', '')
                        elif line.count('<<URL>>') > 0 and s2 == '':
                            print(00000000000)
                            line = line.replace('\n', '')
                            line = line.replace('<<URL>>', '')
                            lbl = Image(source = fr'{k + 1}\URL.jpeg', width = Window.width, height = Window.width, size_hint_y = None)
                            #lbl.on_touch_up = lambda x: webbrowser.open_new_tab(line)
                            box.add_widget(lbl)
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
            if s != '':
                lbl = MDLabel(text = s, font_style = 'Body1', adaptive_height = True)
                box.add_widget(lbl)'''
        except Exception as e:
            box.add_widget(MDLabel(text = 'error: ' + str(e), font_style = 'Body1', adaptive_height = True))
        self.lesson_scroll.add_widget(box)
        self.screen.add_widget(self.lesson_scroll)
        return self.screen
    
    def back(self, item):                                                                           #Функция нажатия на стрелку возврата в урок, либо в меню
        if item == 'to cards':
            self.screen.clear_widgets()
            self.screen.add_widget(MDBoxLayout(MDIconButton(icon = 'menu', on_release = lambda x: self.nav.set_state('open'),
                                                                     pos_hint = {'left': 0, 'top': 0.98})))
            self.screen.add_widget(self.scroll)
            self.screen.add_widget(self.nav_parent)
        else:
            self.screen.clear_widgets()
            self.screen.add_widget(MDBoxLayout(MDIconButton(icon = 'arrow-left', on_release = lambda x: self.back('to cards'),
                                                                 pos_hint = {'left': 0, 'top': 0.98})))
            self.screen.add_widget(self.lesson_scroll)
        return self.screen
    
    def term(self, textinp):                                                                        #Функция перехода в терминал
        self.screen.clear_widgets()
        self.screen.add_widget(MDBoxLayout(MDIconButton(icon = 'arrow-left', on_release = lambda x: self.back('to lesson'),
                                                                 pos_hint = {'left': 0, 'top': 0.98})))
        if textinp.text != '':
            self.screen.add_widget(Terminal(text = textinp.text, text_label = '', obuch = ''))      
        else:
            self.screen.add_widget(Terminal(text = textinp.text, text_label = self.lesson_scroll.children[0].children[1].text, obuch = 'kontrol'))
        return self.screen
        
    def images_open(self, a, b):
        print(a, b)
        self.screen.clear_widgets()
        self.screen.add_widget(MDBoxLayout(MDIconButton(icon = 'arrow-left', on_release = lambda x: self.back('to lesson'),
                                                                 pos_hint = {'left': 0, 'top': 0.98})))
        self.screen.add_widget(FitImage(source = a.source, adaptive_size = True))
        #print(dir(FitImage))
        
class Onboarding(MDScreen):                                                                         #Класс приветствующего окна
    def finish_callback(self):                                                                      #Функция выхода из окна приветствия
        myapp.screen.clear_widgets()
        cursor.execute('UPDATE DATA set Значение="True" where Тип="Обучение"')
        if myapp.theme_cls.theme_style == 'Dark':
            cursor.execute('UPDATE DATA set Значение="Dark" where Тип="Тема"')
        else:
            cursor.execute('UPDATE DATA set Значение="Light" where Тип="Тема"')
        connection.commit()
        myapp.cards()
        
    def change_theme(self):                                                                         #Функция смены цветовой гаммы окна
        myapp.theme_cls.theme_style = (
                'Dark' if myapp.theme_cls.theme_style == 'Light' else 'Light')

class MD3Card(MDCard):                                                                              #Класс разделов с уроками
    source = StringProperty()
    value = NumericProperty()
    
    def change_widget(self):                                                                        #Функция перехода в урок
        myapp.screen.clear_widgets()

class TextInp(MDBoxLayout):                                                                         #Класс текстового поля ввода команд
    text = StringProperty()
    #Snackbar(text = 'Текст скопирован').open()

    def cons(self, textinp):                                                                        #Функция перехода в терминал
        myapp.term(textinp)

class Menu(MDNavigationDrawer):                                                                     #Класс меню пользователя
    def __init__(self):
        super().__init__()
        self.add_widget(MDNavigationDrawerMenu(MDNavigationDrawerHeader(title = "SQLite tutor", text = "", spacing = "4dp", padding = ("12dp", 0, 0, "56dp")),
                           MDNavigationDrawerLabel(text = "Помощь"),
                           MDNavigationDrawerItem(icon = "information", text = "Инструкция", on_release = self.info, text_color = myapp.theme_cls.text_color),
                           MDNavigationDrawerDivider(),
                           MDNavigationDrawerItem(text = "О программе", icon = "information", on_release = self.oprog, text_color = myapp.theme_cls.text_color)))
    
    def info(self, item):                                                                           #Функция для вывода инструкции
        dialog('Для начала Вам необходимо выбрать раздел команд SQL, интересующий Вас, затем выбрать урок по необходимой команде. После прочтения теоретического материала, содержащегося в каждом уроке, Вам предлагается пройти блок проверки, в котором будут задания на выбор верных ответов или на самостоятельное вписывание команд. При прохождении последнего урока раздела Вам предлагается пройти тест по всему разделу.').open()

    def oprog(self, item):                                                                          #Функция для вывода информации о программе
        dialog('Программный продукт был создан в рамках курсового проекта курсантов 331 группы Хачатрян О. А. Дата создания системы - 14.06.2023').open()
        
class dialog(MDDialog):                                                                             #Класс информационного окна
    def __init__(self, text):
        super().__init__()
        self.text = text

class Terminal(MDBoxLayout):                                                                        #Класс терминала
    text_label = StringProperty()
    text = StringProperty()
    obuch = StringProperty()

    def check(self, textinp, lbl, obuch):                                                           #Функция проверки введенного кода
        try:
            cursor.execute(textinp.text.replace('\n', ''))
            connection.commit()
            c = textinp.text.casefold()
            if c.count('create table') == 1 or c.count('create temp table') == 1 or c.count('create temporary table') == 1:
                #t = textinp.text.split()[2].split("(")[0]
                try:
                    t = textinp.text.split("(")[0].split()[-1]
                    cursor.execute('select sql from sqlite_master where name = "' + t.strip() + '";')
                    result = cursor.fetchone()[0]
                except Exception as e: print(e)
                if obuch == 'kontrol':
                    if result == myapp.answer:
                        lbl.text = 'Верно'    
                    else:
                        lbl.text = 'Неверно, попробуйте еще'
                        return
                cursor.execute('pragma table_info("' + t + '");')
                cols = [i[1] for i in cursor.fetchall()]                                            #считывание стобцов
                data = []
                for k in cols:
                    data.append(((k, dp(30))))
                self.add_widget(MDDataTable(size_hint = (1, None), column_data = data))
            elif textinp.text.casefold().count('drop table') == 1:
                if obuch == 'kontrol':
                    if textinp.text.casefold() == myapp.answer:
                        lbl.text = 'Верно, таблица удалена'    
                    else:
                        lbl.text = 'Неверно, попробуйте еще'
                        return
            elif textinp.text.casefold().count('alter table') == 1:
                if obuch == 'kontrol':
                    if textinp.text.casefold() == myapp.answer:
                        lbl.text = 'Верно, таблица изменена'    
                    else:
                        lbl.text = 'Неверно, попробуйте еще'
                        return
        except Exception as e:
            lbl.text = 'Некорректный ввод, попробуйте еще'
            return
                
        
if __name__ == '__main__':
    title, lesson, values = [], [], []
    connection = sqlite3.connect('sq.db')                                                           #Соединение с базой данных
    cursor = connection.cursor()
    cursor.execute('select name from sqlite_master where type = "table";')                          #Команда для вывода всех таблиц из этой базы
    result = cursor.fetchall()
    for i in result:
        for k in i:
            if k != 'DATA':
                try:
                    cursor.execute('DROP TABLE ' + k)                                               #Удаление ненужных таблиц
                except: pass
    connection.commit()
    with open('themes.txt', 'r', encoding = 'utf8') as f:                                             #Считывание разделов и уроков из текстового файла
        for line in f:
            title.append(line.split(' (')[0])
            a = line.split(' (')[1][:-2]
            lesson.append(a.split(', '))
    '''
    title = ['Создание базы данных', 'Связи и внешние ключи', 'Создание таблиц',
                 'Заполнение таблиц', 'Запросы', 'Реляционная алгебра', 'Триггеры']
    lesson = [['Создание и хранение БД', 'Метакоманды'], ['Ограничения', 'Первичный и внешний ключ'], ['CREATE', 'DROP', 'ALTER'],
                  ['INSERT', 'UPDATE', 'DELETE'], ['SELECT'], ['Операции'], ['Создание триггеров']]'''
    #print(title, lesson,sep = '\n')         
    #cursor.execute('select sql from sqlite_master where name = "DATA";')   
    myapp = MyApp()
    myapp.run()
    cursor.close()
    connection.close() 


