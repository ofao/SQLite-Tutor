from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel, MDIcon
#from kivy.uix.video import Video
from kivy.uix.textinput import TextInput
#from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatIconButton, MDIconButton, MDFlatButton, MDFloatingActionButton, MDRectangleFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDFadeSlideTransition
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast #для файлового менеджера
import sqlite3, json, os
from kivy.properties import ColorProperty, StringProperty, NumericProperty, BooleanProperty
import re #для обработки вводимого пользователем скрипта
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.snackbar import Snackbar
#from board import *  #введение
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.list import OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.fitimage import FitImage
from kivy.uix.image import Image, AsyncImage
from kivymd import images_path
from kivymd_extensions.akivymd.uix.onboarding import *
from kivymd.uix.navigationdrawer import (MDNavigationDrawer, MDNavigationDrawerMenu, MDNavigationLayout,
                                         MDNavigationDrawerItem, MDNavigationDrawerDivider, MDNavigationDrawerLabel,
                                         MDNavigationDrawerHeader)
from kivymd.uix.datatables import MDDataTable
from kivy.utils import platform  #для определения ОС
###ИМПОРТЫ ДЛЯ МОБИЛЬНОЙ ВЕРСИИ - АНДРОИД
if platform == 'android':
    from android.storage import primary_external_storage_path
    from android.permissions import request_permissions, Permission
#from android.permissions import Permission, request_permissions
#from android.storage import primary_external_storage_path
import xml.etree.ElementTree as ET #ЧТЕНИЕ XML ФАЙЛОВ
#https://iconscout.com/lottie-animation/win-10290126
from kivymd_extensions.akivymd.uix.imageview import *
from kivy.core.clipboard import Clipboard, CutBuffer  #для копирования текста
from kivymd.uix.selectioncontrol import MDCheckbox
#from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
#from kivy.uix.togglebutton import ToggleButton
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.chip import MDChip
from kivymd.uix.textfield import MDTextField
from kivymd_extensions.akivymd.uix.spinners import AKSpinnerDoubleBounce #загрузка
from sql_metadata import Parser #для получения имен таблиц и столбцов
from sql_metadata.compat import get_query_columns, get_query_tables
from kivy.config import Config
kv = ("""
<MCQLabel@ButtonBehavior+MDLabel>:
    size_hint_y: None
    text_size: self.size
    theme_text_color: "Custom"
    text_color: app.theme_cls.text_color
    
<MyCheckbox>:
    adaptive_height: True
    size_hint_y: None
    MDCheckbox:
        id: check
        color_inactive: app.theme_cls.text_color
        #text: root.text
        size_hint: .1, None
        #group: root.group
    MCQLabel:
        size_hint_y: None
        text: root.text
        on_press: check._do_press()
    
<MyDialog>:
    MDBoxLayout:
        id: mybox
        orientation: "horizontal" if app.platform!="android" else "vertical"
        spacing: dp(20)
        size_hint_y: 1
        md_bg_color: app.theme_cls.bg_normal
        radius: 15
        
        MDFloatLayout:
            md_bg_color: root.color
            size_hint_x: .5 if app.platform!="android" else 1
            pos: (0, 0)
            radius: (5, 0, 0, 5)
            MDIcon:
                icon: root.source
                pos_hint: {"center_x": .5, "center_y": .5}
                icon_color: app.theme_cls.text_color
                font_size: dp(50)
        MDScrollView:
            MDBoxLayout:
                id: box
                orientation: 'vertical'
                adaptive_height: True
                size_hint_y: None
                pos_hint: {'top': 1}
                padding: (0, 10, 20, 20)
                spacing: 25
                MDLabel:
                    padding: 10, 10
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None
                    text: root.textBox
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.text_color
            
<MyAKOnboardingItem@AKOnboardingItem>:
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
    on_leave: boarding.reset()
    on_enter: setattr(boarding.ids.rounded_box.children[0], 'text', 'Завершить обучение')
    
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(10)

        AKOnboarding:
            id: boarding
            on_finish: root.finish_callback()
            circles_size: dp(15)
            skip_button: True
            
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
                            on_release: app.change_theme()

<MD3Card>:
    size_hint: 1, None
    size: "300dp", "300dp"
    md_bg_color: '#DFDFDF' if app.theme_cls.theme_style=='Light' else '#393939'
    text_color: app.theme_cls.text_color
    foreground_color: app.theme_cls.text_color
    #border_radius: 20
    radius: [15]
    orientation: "vertical"

    FitImage:
        source: root.source
        radius: [15, 15, 0, 0]

    MDProgressBar:
        id: progress
        size_hint_y: 0.1
        value: root.value
        
<TextInp>:
    size_hint_y: None
    md_bg_color: app.theme_cls.bg_normal

    MDTextFieldRect:
        id: tex
        text: root.text
        #multiline: True
        size_hint_x: .9
        #scroll_from_swipe: True
        readonly: True if not root.isKontrol else False
        foreground_color: app.theme_cls.text_color
        background_color: '#DFDFDF' if app.theme_cls.theme_style=='Light' else '#393939'
        background_normal: ''
        border: [4, 4, 4, 4]
        #height: (len(self._lines) + 1) * self.line_height
    
    MDIconButton:
        text: " "
        icon: "play"
        theme_icon_color: "Custom"
        size_hint: .1, 1
        height: tex.height
        icon_color: app.theme_cls.primary_color
        pos_hint: {'right': 1}
        on_release: app.term(tex.text, root.isKontrol)

    MDIconButton:
        text: " "
        icon: "content-copy"
        theme_icon_color: "Custom"
        size_hint: .1, 1
        height: tex.height
        icon_color: app.theme_cls.primary_color
        pos_hint: {'right': 1}
        on_release: app.copyText(tex.text)    

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
        background_color: '#DFDFDF' if app.theme_cls.theme_style=='Light' else '#393939'
        background_normal: ''
        foreground_color: app.theme_cls.text_color
        scroll_from_swipe: True
        size_hint: 1, None
        adaptive_height: True
        height: (len(self._lines) + 1) * self.line_height if len(root.text) > 1 else Window.height/2

    MDRectangleFlatButton:
        text: 'Готово'
        size_hint: 1, None
        on_release: root.check(textinp, root.obuch)
        md_border_color: [0, 0, 0, 0.1]
        
<ScreenCards>:
    MDTopAppBar:
        id: topapp
        left_action_items: [['menu', lambda x : nav.set_state('open')]]
        elevation: 0
        pos_hint: {'top': 1}
        
    MDScrollView:
        id: scroll
        size_hint: (1, None)
        bar_width: 8
        size: (Window.width, (Window.height - topapp.height))
        scroll_type: ['content', 'bars']
         
        MDGridLayout:
            id: grid
            cols: 2
            pos_hint: {'top': 1}
            spacing: 20
            size_hint_y: None
            padding: 10
            adaptive_height: True
            
    MDNavigationDrawer:
        id: nav
        radius: [0, 15, 15, 0]
        bg_color: app.theme_cls.bg_normal
        text_color: app.theme_cls.text_color
        MDNavigationDrawerMenu:
            MDNavigationDrawerHeader:
                #source: 'database.png'
                title: "SQLite tutor"
                text: ""
                spacing: '4dp'
                padding: ('12dp', 0, 0, '56dp')
            MDNavigationDrawerLabel:
                markup: True
                text: "[color=000]Помощь[/color]" if app.theme_cls.theme_style=='Light' else "[color=fff]Помощь[/color]"
            MDNavigationDrawerItem:
                focus_color: '#DFDFDF' if app.theme_cls.theme_style=='Light' else '#393939'
                icon: 'weather-night' if app.theme_cls.theme_style=='Dark' else 'weather-sunny'
                text: 'Тема приложения'
                icon_color: app.theme_cls.text_color
                text_color: app.theme_cls.text_color
                selected_color: app.theme_cls.text_color
                on_release: app.change_theme()
                bg_color: 'white' if app.theme_cls.theme_style=='Light' else '#212121'
            MDNavigationDrawerItem:
                focus_color: '#DFDFDF' if app.theme_cls.theme_style=='Light' else '#393939'
                icon: "information"
                icon_color: app.theme_cls.text_color
                selected_color: app.theme_cls.text_color
                text: "Инструкция"
                on_release: root.info()
                bg_color: 'white' if app.theme_cls.theme_style=='Light' else '#212121'
                text_color: app.theme_cls.text_color
            MDNavigationDrawerItem:
                focus_color: '#DFDFDF' if app.theme_cls.theme_style=='Light' else '#393939'
                text: "О программе"
                icon: "information"
                on_release: root.oprog()
                icon_color: app.theme_cls.text_color
                selected_color: app.theme_cls.text_color
                text_color: app.theme_cls.text_color
                bg_color: 'white' if app.theme_cls.theme_style=='Light' else '#212121'
            MDNavigationDrawerDivider:
            MDNavigationDrawerItem:
                focus_color: '#DFDFDF' if app.theme_cls.theme_style=='Light' else '#393939'
                text: "Создать БД"
                icon: "plus"
                on_release: root.createDB()
                icon_color: app.theme_cls.text_color
                selected_color: app.theme_cls.text_color
                text_color: app.theme_cls.text_color
                bg_color: 'white' if app.theme_cls.theme_style=='Light' else '#212121'
            MDNavigationDrawerItem:
                focus_color: '#DFDFDF' if app.theme_cls.theme_style=='Light' else '#393939'
                text: "Открыть БД"
                icon: "folder"
                on_release: root.openDB()
                icon_color: app.theme_cls.text_color
                selected_color: app.theme_cls.text_color
                text_color: app.theme_cls.text_color
                bg_color: 'white' if app.theme_cls.theme_style=='Light' else '#212121'
            MDNavigationDrawerItem:
                id: mydb
                focus_color: '#DFDFDF' if app.theme_cls.theme_style=='Light' else '#393939'
                text: "Мои БД"
                icon: "database"
                on_release: setattr(app.screenManager, 'current', 'ScreenMyDB')
                icon_color: app.theme_cls.text_color
                selected_color: app.theme_cls.text_color
                text_color: app.theme_cls.text_color
                bg_color: 'white' if app.theme_cls.theme_style=='Light' else '#212121'
                
<ScreenLesson@MDScreen>:
    MDTopAppBar:
        id: topapp
        left_action_items: [['arrow-left', lambda x: setattr(app.screenManager, 'current', 'ScreenCards')]]
        pos_hint: {'top': 1}
        height: 20
        elevation: 0
    MDScrollView:
        id: scroll
        bar_width: 8
        size_hint: (1, None)
        size: (Window.width, (Window.height - topapp.height))
        scroll_type: ['content', 'bars']
        #pos_hint: {'top': 0.85}
        MDBoxLayout:
            id: box
            orientation: 'vertical'
            padding: 10
            spacing: 10
            adaptive_height: True
            size_hint_y: None
            pos_hint: {'top': 1}
            
<ScreenTerminal@MDScreen>:
    prevScreen: 'ScreenLesson'
    MDTopAppBar:
        id: topapp
        left_action_items: [['arrow-left', lambda x: setattr(app.screenManager, 'current', root.prevScreen)]]
        pos_hint: {'top': 1}
        elevation: 0
    MDScrollView:
        id: scroll
        size_hint: (1, None)
        bar_width: 8
        size: (Window.width, (Window.height - topapp.height))
        scroll_type: ['content', 'bars']
        MDBoxLayout:
            id: box
            orientation: 'vertical'
            padding: 10
            spacing: 10
            adaptive_height: True
            size_hint_y: None
            pos_hint: {'top': 1}
            
<ScreenMyDB>:
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            id: topapp
            left_action_items: [['arrow-left', lambda x: setattr(app.screenManager, 'current', 'ScreenCards')]]
            #pos_hint: {'top': 1}
            elevation: 0
        MDTabs:
            background_color: app.theme_cls.bg_normal
            indicator_color: app.theme_cls.primary_color
            text_color_normal: app.theme_cls.text_color
            text_color_active: app.theme_cls.text_color
            id: tabs
            on_tab_switch: root.tabSwitch(*args)
    MDScrollView:
        id: scroll
        size_hint: (1, None)
        bar_width: 8
        size: (Window.width, (Window.height - tabs.tab_bar_height - topapp.height))
        scroll_type: ['content', 'bars']
        MDBoxLayout:
            id: box
            orientation: 'vertical'
            padding: 30
            spacing: 30
            adaptive_height: True
            size_hint: 1, None
            pos_hint: {'top': 1}
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint: 1, 1
                adaptive_height: True
                MDTextField:
                    id: path
                    hint_text: "Путь"
                    mode: "rectangle"
                    size_hint_x: .9
                    readonly: True
                    line_color_normal: app.theme_cls.primary_color
                    text_color_normal: app.theme_cls.text_color
                MDIconButton:
                    id: deleteButton
                    icon: 'delete'
                    text: " "
                    height: path.height
                    theme_icon_color: "Custom"
                    size_hint_x: .1
                    icon_color: app.theme_cls.primary_color
                    pos_hint: {'right': 1}
            MDLabel:
                text: 'Таблицы:'
                color: app.theme_cls.text_color
            MDStackLayout:
                id: DBTables
                adaptive_height: True
                spacing: 5
                padding: 10
                line_color: app.theme_cls.primary_color
                line_width: 
                radius: 5
            MDLabel:
                text: 'Триггеры:'
                color: app.theme_cls.text_color
            MDStackLayout:
                id: DBTriggers
                adaptive_height: True
                spacing: 5
                padding: 10
                line_color: app.theme_cls.primary_color
                line_width: 
                radius: 5
            MDLabel:
                text: 'Представления:'
                color: app.theme_cls.text_color
            MDStackLayout:
                id: DBViews
                adaptive_height: True
                spacing: 5
                padding: 10
                line_color: app.theme_cls.primary_color
                line_width: 
                radius: 5
            MDLabel:
                text: 'Индексы:'
                color: app.theme_cls.text_color
            MDStackLayout:
                id: DBIndex
                adaptive_height: True
                spacing: 5
                padding: 10
                line_color: app.theme_cls.primary_color
                line_width: 
                radius: 5
            TextInp:
                id: term
                isKontrol: False
<ScreenMyDBObject@MDScreen>:
    MDTopAppBar:
        id: topapp
        left_action_items: [['arrow-left', lambda x: setattr(app.screenManager, 'current', 'ScreenMyDB')]]
        pos_hint: {'top': 1}
        elevation: 0
    MDScrollView:
        id: scroll
        size_hint: (1, None)
        bar_width: 8
        size: (Window.width, (Window.height - topapp.height))
        scroll_type: ['content', 'bars']
        MDBoxLayout:
            id: box
            orientation: 'vertical'
            padding: 10
            spacing: 40
            adaptive_height: True
            size_hint_y: None
            pos_hint: {'top': 1}
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint: 1, 1
                adaptive_height: True
                MDTextField:
                    id: nameObject
                    mode: "rectangle"
                    size_hint_x: .9
                    readonly: True
                    line_color_normal: app.theme_cls.primary_color
                    text_color_normal: app.theme_cls.text_color
                MDIconButton:
                    id: deleteButton
                    icon: 'delete'
                    text: " "
                    height: nameObject.height
                    theme_icon_color: "Custom"
                    size_hint_x: .1
                    icon_color: app.theme_cls.primary_color
                    pos_hint: {'right': 1}
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint: 1, 1
                adaptive_height: True
                MDTextField:
                    id: sqlObject
                    mode: "rectangle"
                    hint_text: "SQL"
                    size_hint_x: .9
                    readonly: True
                    line_color_normal: app.theme_cls.primary_color
                    text_color_normal: app.theme_cls.text_color
                    multiline: True
                MDIconButton:
                    id: copyButton
                    icon: "content-copy"
                    text: " "
                    height: nameObject.height
                    theme_icon_color: "Custom"
                    size_hint_x: .1
                    icon_color: app.theme_cls.primary_color
                    pos_hint: {'right': 1}
                    on_release: app.copyText(sqlObject.text)
            MDBoxLayout:
                id:content
                spacing: 40
                orientation: 'vertical'
                size_hint: 1, 1
                adaptive_height: True
            
<ScreenTest>:
    MDTopAppBar:
        id: topapp
        left_action_items: [['arrow-left', lambda x: setattr(app.screenManager, 'current', 'ScreenLesson')]]
        pos_hint: {'top': 1}
        elevation: 0  
    MDBoxLayout:
        id: box
        orientation: "vertical"
        size_hint: 1, None
        size: (Window.width, (Window.height - topapp.height))
<ScreenLoading@MDScreen>:
    AKSpinnerDoubleBounce:
        active: True
        pos_hint: {'center_x': .5, 'center_y': .5}
MDScreenManager:
    ScreenCards:
        name: 'ScreenCards'
    Onboarding:
        name: 'Onboarding'
    ScreenLesson:
        name: 'ScreenLesson'
    ScreenTerminal:
        name: 'ScreenTerminal'
    ScreenTest:
        name: 'ScreenTest'
    ScreenMyDB:
        name: 'ScreenMyDB'
    ScreenLoading:
        name: 'ScreenLoading'
    ScreenMyDBObject:
        name: 'ScreenMyDBObject'
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
        self.platform = platform
        self.dir = __file__.replace('main.py', '').replace('\\', '/')
        #self.on_resize('a', Window.size)
    
    def on_resize(self, obj, size):                                                             #Функция, реагирующая на изменение размеров окна
        if self.screenManager.current_screen.name == 'ScreenCards':
            grid = self.screenManager.current_screen.ids.grid
            if size[0] <= 630:
                grid.cols = 1
            elif size[0] > 630 and size[0] <= 1080:
                grid.cols = 2
            elif size[0] > 1080 and size[0] <= 1450:
                grid.cols = 3
            else:
                grid.cols = 4
        elif self.screenManager.current_screen.name == 'ScreenTest':
            box = self.screenManager.current_screen.ids.box
            box.size = (Window.width, (Window.height - self.screenManager.current_screen.ids.topapp.height))
            board = self.screenManager.current_screen.board
            board.size = (box.width, box.height)
            items = self.screenManager.current_screen.items
            for item in items:
                item.size = (box.width, box.height - board.ids.rounded_box.height)
                item.children[0].size = (box.width, box.height - board.ids.rounded_box.height)            
        
    def build(self):                                                                                #Функция, которая вызывается 1 раз при запуске программы
        global global_data
        Window.bind(size = self.on_resize)                                                          #привязка на изменение размеров окна
        obuch_passed = global_data['obuch_passed']
        self.theme_cls.theme_style = global_data['theme']
        
        self.screenManager = Builder.load_string(kv)
        #self.screenManager.transition = MDFadeSlideTransition()
        self.screenManager.duration = '.8'
        if not obuch_passed:                                                                 #Если первый запуск программы, то будет показано приветствующее окно
            #self.screen.add_widget(Onboarding())
            self.screenManager.current = 'Onboarding'
        else:
            self.screenManager.current = 'ScreenCards'
            self.screenManager.current_screen.ids.mydb.right_text = str(len(global_data['databases']))
            self.cards()
        return self.screenManager

    def cards(self):                                                                                #Функция, которая вызывается в случае, когда окно приветствия пройдено
        global global_data
        grid = self.screenManager.current_screen.ids.grid
        i = 1
        for key in global_data:
            if key != 'theme' and key != 'obuch_passed' and key != 'databases':
                val = 100/len(global_data[key].keys())
                passed = 0
                for vall in global_data[key]:
                    if global_data[key][vall]:
                        passed += val
                card = MD3Card(source = str(i) + ".png", value = passed)
                self.text = list(global_data[key].keys())[:-1]   #список уроков раздела key #-1 потому что последний элемент - Тест
                panel = MDExpansionPanel(
                    content = self.addItemsToCard(), 
                    panel_cls = MDExpansionPanelOneLine(text = key, theme_text_color = 'Custom', text_color = myapp.theme_cls.text_color))
                panel.opening_transition = 'out_sine'
                card.add_widget(panel)
                grid.add_widget(card)
                i += 1
        
    def addItemsToCard(self):                                                                               #Функция добавления уроков в раздел
        box = MDBoxLayout(orientation = 'vertical', padding = 10, spacing = 10,
                          adaptive_height = True)
        for i in range(len(self.text)):
            item = OneLineListItem(text = self.text[i], on_release = self.panel_open, theme_text_color = 'Custom', text_color = myapp.theme_cls.text_color)
            box.add_widget(item)
        return box
       
    def panel_open(self, item):                                                                     #Функция, которая вызывается на открытие раздела, открывает список уроков
        global global_data
        self.screenManager.current = 'ScreenLoading'
        self.cur_card = item.parent.parent.parent
        box = self.screenManager.get_screen('ScreenLesson').ids.box #Виджет, в который будет добавляться материал урока
        box.clear_widgets() #очищаем от предыдущего урока
        j, k = 0, 0
        for key in global_data:
            if key != 'theme' and key != 'obuch_passed' and key != 'databases':
                if item.text in list(global_data[key].keys()):
                    self.razdel = key
                    self.lesson = item.text
                    j = list(global_data[key].keys()).index(item.text)
                    if j == len(list(global_data[key].keys())) - 2:  #-2 потому что не берем Тест
                        self.test = True
                    else:
                        self.test = False
                    break
                k += 1
        self.razdel_num = k + 1
        self.lesson_num = j + 1
        lbl_header = MDLabel(text = item.text, bold = True, font_size = 10, font_style = 'H5', adaptive_height = True, halign = 'center')  ##заголовок
        box.add_widget(lbl_header)
        viewer =  AKImageViewer()
        try:
            tree = ET.parse(str(k + 1) + '/' + str(j + 1) + '.xml')
            root = tree.getroot()
            for elem in root.iter():
                if elem.tag == 'text':
                    lbl = MDLabel(text = elem.text, font_style = 'Body1', adaptive_height = True)
                    box.add_widget(lbl)
                elif elem.tag == 'title':
                    lbl = MDLabel(text = elem.text, bold = True, font_size = 10,
                                                   font_style = 'H5', adaptive_height = True, halign = 'center')
                    box.add_widget(lbl)
                elif elem.tag == 'subtitle':
                    lbl = MDLabel(text = elem.text, bold = True, font_size = 10,
                                                   font_style = 'Subtitle1', adaptive_height = True, halign = 'center', text_color = 'grey')
                    box.add_widget(lbl)
                elif elem.tag == 'picture':
                    #from create import create_schema
                    imgbox = MDBoxLayout(orientation = 'horizontal', size_hint_y = None)
                    lbl = FitImage(source = fr'{k + 1}/{elem.text}', size_hint_y = None)
                    viewer.add_widget(AKImageViewerItem(source = lbl.source))
                        
                    imgbox.add_widget(lbl)
                    imgbox.add_widget(MDIconButton(icon = 'loupe', on_release = lambda x: viewer.open(), theme_icon_color="Custom", icon_color=myapp.theme_cls.primary_color))
                    box.add_widget(imgbox)
                    #box.add_widget(create_schema())
                elif elem.tag == 'answer':
                    self.answer = elem.text
                elif elem.tag == 'URL':
                    lbl = Image(source = fr'{k + 1}\URL.jpeg', size_hint_y = None)
                    box.add_widget(lbl)
                elif elem.tag == 'code':
                    attrib = elem.attrib.get('type')
                    if elem.text == None:
                        elem.text = ''
                    if attrib == None:
                        inp = TextInp(text = elem.text, md_bg_color = [245,245,245,1], specific_text_color=myapp.theme_cls.text_color)
                        inp.isKontrol = False
                        inp.height = (elem.text.count('\n') + 2) * inp.ids.tex.line_height  # 18 = inp.ids.tex.line_height
                    elif attrib == 'answer':
                        inp = TextInp(text = elem.text, md_bg_color = [245,245,245,1], specific_text_color=myapp.theme_cls.text_color)
                        inp.isKontrol = True
                        inp.height = Window.height/2
                    else:
                        inp = TextInp(text = elem.text) #С результатом выполнения кода
                        inp.isKontrol = False
                        inp.height = (elem.text.count('\n') + 2) * inp.ids.tex.line_height
                    box.add_widget(inp)
                elif elem.tag == 'table':
                    data = []
                    cols = len(elem.attrib.get('cols').split(','))
                    cols_width = dp(Window.width/cols / 6)
                    for k in elem.attrib.get('cols').split(','):
                        data.append(((k, cols_width)))
                    table = MDDataTable(size_hint = (1, None), elevation = 1, column_data = data, use_pagination=True)
                    data = []
                    for k in elem.text.split('\n'):
                        if k == '':
                            pass
                        if len(data) < cols:
                            data.append(k)
                        else:
                            table.add_row(data)
                            data = [k]
                    table.height = Window.height/2
                    box.add_widget(table)
                #print(elem.tag)
        except Exception as e:
            print(e)
            box.add_widget(MDLabel(text = 'error: ' + str(e), font_style = 'Body1', adaptive_height = True))
        if self.test:
            box.add_widget(MDRectangleFlatButton(text = 'Пройти тест', on_release = self.open_test))
        self.screenManager.get_screen('ScreenLesson').ids.scroll.scroll_to(lbl_header, padding = 0) #возвращает на верх урока
        self.screenManager.current = 'ScreenLesson'
        
    def open_test(self, button):
        self.screenManager.current = 'ScreenLoading'
        self.screenManager.get_screen('ScreenTest').createTest()
        self.screenManager.current = 'ScreenTest'
        
    def term(self, InpText, InpIsKontrol):                                                                       #Функция перехода в терминал
        thisScreen = self.screenManager.current_screen.name
        self.screenManager.current = 'ScreenTerminal'
        self.screenManager.current_screen.prevScreen = thisScreen
        box = self.screenManager.current_screen.ids.box #Виджет, в который будет добавляться материал урока
        box.clear_widgets() #очищаем от предыдущего урока
        if not InpIsKontrol:
            box.add_widget(Terminal(text = InpText, text_label = '', obuch = ''))      
        else:
            for widget in self.screenManager.get_screen('ScreenLesson').ids.box.children:
                if isinstance(widget, MDLabel):
                    t = widget.text
                    break
            box.add_widget(Terminal(text = InpText, text_label = t, obuch = 'kontrol'))
        #return self.screen

    def copyText(self, text):
        Clipboard.copy(text)
        toast('Текст скопирован!')
        
    def change_theme(self):                                                                         #Функция смены цветовой гаммы окна
        myapp.theme_cls.theme_style = (
                'Dark' if myapp.theme_cls.theme_style == 'Light' else 'Light')
        global_data['theme'] = myapp.theme_cls.theme_style
        insertToJSON()
        if self.screenManager.current_screen.name == 'ScreenCards':
            for panel in self.screenManager.current_screen.ids.grid.children:
                panel.children[0].children[-1].text_color = myapp.theme_cls.text_color
                for listItem in panel.children[0].content.children:
                    listItem.text_color = myapp.theme_cls.text_color
            
class ScreenTest(MDScreen):
    def finish_callback(self):                                                                      #Функция выхода из окна приветствия
        global global_data
        
        def again(button): #пройти тест еще раз
            for item in self.items:
                for widget in item.children[0].children[0].children:
                    if isinstance(widget, MyCheckbox):
                        widget.children[1].state = 'normal'
            self.board.reset()
            dial.dismiss()
            
        answers = 0                                                                                 #количество правильных ответов
        for item in self.items:
            li = []
            for widget in item.children[0].children[0].children:
                if isinstance(widget, MyCheckbox):
                    if widget.children[1].state == 'down': #выбран правильный вариант
                        li.append(widget.correct)
                    else:
                        li.append(not widget.correct)
            if not False in li:
                answers += 1
        t = 'Ваш результат: ' + str(answers) + ' из ' + str(len(self.items))
        if answers >= len(self.items)/2:
            if not global_data[myapp.razdel]['Тест']:
                global_data[myapp.razdel]['Тест'] = True
                insertToJSON()
                myapp.cur_card.value += 100/len(global_data[myapp.razdel].keys())
            t += '\nВы успешно прошли тест!'
            dial = MyDialog(textBox = t, source = 'check-circle', color = 'green')
            dial.ids.box.add_widget(MDRectangleFlatButton(text = 'Вернуться к урокам', on_release = dial.openCards))
            dial.open()
        else:
            t += '\nК сожалению этого результата недостаточно, Вы можете пройти тест еще раз.'
            dial = MyDialog(textBox = t, source = 'close-circle', color = 'red')
            box = MDBoxLayout(orientation='horizontal', size_hint=(1, None), adaptive_height=True, spacing=10)
            box.add_widget(MDRectangleFlatButton(text = 'Вернуться к урокам', on_release = dial.openCards))
            box.add_widget(MDRectangleFlatButton(text = 'Пройти тест еще раз', on_release = again))
            dial.ids.box.add_widget(box)
            dial.open()
        
    def on_leave(self):
        try:
            self.board.reset()
        except: pass
        
    def createTest(self):
        global global_data
        try:
            box = self.ids.box
            box.clear_widgets()
            tree = ET.parse(str(myapp.razdel_num) + '/test.xml')
            root = tree.getroot()
            self.board = AKOnboarding(skip_button=True)
            self.board.on_finish=self.finish_callback  #привязка к функции обработки ответов
            self.board.ids.rounded_box.children[0].text = 'Завершить тест'
            self.board.size = (box.width, box.height)
            self.items = []
            for elem in root.iter('question'):
                count = 0
                variants = {}
                akitem = AKOnboardingItem(orientation = 'vertical', size = (box.width, box.height - self.board.ids.rounded_box.height), size_hint=(1, None))
                self.items.append(akitem)
                widget = MDBoxLayout(orientation = 'vertical', padding=10, adaptive_height=True, size_hint_y=None)
                for obj in elem.findall('text'):
                    lbl = MDLabel(text = obj.text, font_style = 'Body1', adaptive_height = True, size_hint_y=None)
                    widget.add_widget(lbl)
                for obj in elem.findall('variant'):
                    attrib = obj.attrib.get('correct')
                    if attrib == 'true':
                        count += 1
                        variants[obj.text] = True
                    else:
                        variants[obj.text] = False
                if count == 1:
                    #group = MDSegmentedControl(size_hint_max_x = 0.5)
                    #print(dir(group))
                    gro = lbl.text
                    for key, value in variants.items():
                        #item = ToggleButton(text = key, group = group)
                        item = MyCheckbox(text = key, correct = value)
                        item.children[1].group = gro #Добавление чекбоксов в группу создает радиокнопку  
                        #group.add_widget(item)
                        widget.add_widget(item)
                    #widget.add_widget(group)
                else:
                    for key, value in variants.items():
                        item = MyCheckbox(text = key, correct = value) #True/False
                        widget.add_widget(item)
                scroll = MDScrollView(bar_width=8, size_hint=(1, None), size=akitem.size, scroll_type=['content', 'bars'])
                scroll.add_widget(widget)
                akitem.add_widget(scroll)
                self.board.add_widget(akitem)
            box.add_widget(self.board)
        except Exception as e:
            MyDialog(textBox = 'Здесь еще нет теста', source='close-circle', color = 'blue').open()
    
class MyCheckbox(MDBoxLayout):
    correct = BooleanProperty()  #Свойство является ли чекбокс правильным ответом
    text = StringProperty()
    #group = StringProperty()
    
class ScreenMyDB(MDScreen):
    def on_enter(self):
        global global_data
        try:
            tabs = self.ids.tabs
            tabs.ids.layout.clear_widgets()
            for item in global_data['databases']:
                name = item.replace('\\', '/')
                name = name[:-3]
                if name.count('/') > 0:
                    name = name[name.rindex('/') + 1:]
                tabs.add_widget(Tab(title = name, path = item))
            #self.tabSwitch()
        except Exception as e:
            print(e)

    def tabSwitch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        global connection, cursor
        tab_name = tab_text
        path = instance_tab.path
        self.ids.path.text = path
        self.ids.DBTables.clear_widgets()
        self.ids.DBViews.clear_widgets()
        self.ids.DBTriggers.clear_widgets()
        self.ids.DBIndex.clear_widgets()
        connection = sqlite3.connect(path)                                                           #Соединение с базой данных
        cursor = connection.cursor()
        cursor.execute('select type, name, sql from sqlite_master;')                          #Команда для вывода всех таблиц из этой базы
        result = cursor.fetchall()
        for item in result:
            if item[0] == 'table':
                widget = self.ids.DBTables
            elif item[0] == 'view':
                widget = self.ids.DBViews
            elif item[0] == 'index':
                widget = self.ids.DBIndex
            else:
                widget = self.ids.DBTriggers
            widget.add_widget(MDChip(text = item[1], on_release = self.openDBObject))
        if len(self.ids.DBTriggers.children) == 0:
            self.ids.DBTriggers.add_widget(MDChip(text = 'Здесь пока пусто'))
        if len(self.ids.DBTables.children) == 0:
            self.ids.DBTables.add_widget(MDChip(text = 'Здесь пока пусто'))
        if len(self.ids.DBViews.children) == 0:
            self.ids.DBViews.add_widget(MDChip(text = 'Здесь пока пусто'))
        if len(self.ids.DBIndex.children) == 0:
            self.ids.DBIndex.add_widget(MDChip(text = 'Здесь пока пусто'))
        if path == myapp.dir + 'sq.db':
            self.ids.deleteButton.disabled = True
        else:
            self.ids.deleteButton.disabled = False
        self.ids.deleteButton.on_release = lambda: self.deleteDB(instance_tab)
             
    def openDBObject(self, chip):
        global connection, cursor
        myapp.screenManager.current = 'ScreenLoading'
        box = myapp.screenManager.get_screen('ScreenMyDBObject').ids.content                                #Виджет, в который будет добавляться информация об объекте БД
        box.clear_widgets()
        textinp = myapp.screenManager.get_screen('ScreenMyDBObject').ids.nameObject
        if chip.parent==self.ids.DBTables:
            textinp.hint_text = 'Таблица'
            box.add_widget(MDLabel(text = 'Структура:'))
            cursor.execute('pragma table_info("' + chip.text + '");')
            cols = [list(i[1:]) for i in cursor.fetchall()]                                               #считывание столбцов
            for i in cols:
                if i[2] == 1:
                    i[2] = ("checkbox-marked-circle", 'green', '')
                else:
                    i[2] = ("close-circle", 'red', '')
                if i[4] == 1:
                    i[4] = ("checkbox-marked-circle", 'green', '')
                else:
                    i[4] = ("close-circle", 'red', '')
            box.add_widget(MDDataTable(size_hint = (1, None), column_data = (('NAME', dp(30)), ('TYPE', dp(30)),
                                                                             ('NOT NULL', dp(30)), ('DEFAULT', dp(30)),
                                                                             ('PRIMARY KEY', dp(30))), row_data = cols, use_pagination=True, height=Window.height/3))
            box.add_widget(MDLabel(text = 'Данные:'))
            cursor.execute('select * from ' + chip.text)
            data = cursor.fetchall()
            cols = [[i[0]] for i in cursor.description]
            for k in cols:
                k.append(dp(30))
            box.add_widget(MDDataTable(size_hint = (1, None), column_data = cols, row_data = data, use_pagination=True, height=Window.height/3))
        elif chip.parent==self.ids.DBViews:
            textinp.hint_text = 'Представление'
            box.add_widget(MDLabel(text = 'Данные:'))
            cursor.execute('select * from ' + chip.text)
            data = cursor.fetchall()
            cols = [list(i[0]) for i in cursor.description]
            for k in cols:
                k.append(dp(30))
            box.add_widget(MDDataTable(size_hint = (1, None), column_data = cols, row_data = data, use_pagination=True, height=Window.height/3))
        elif chip.parent==self.ids.DBTriggers:
            textinp.hint_text = 'Триггер'
        else:
            textinp.hint_text = 'Индекс'
        textinp.text = chip.text
        cursor.execute('select sql from sqlite_master where name="' + chip.text + '"')
        sql = cursor.fetchone()[0]
        if sql != None:
            myapp.screenManager.get_screen('ScreenMyDBObject').ids.sqlObject.text = sql
        else:
            myapp.screenManager.get_screen('ScreenMyDBObject').ids.sqlObject.text = ''
        myapp.screenManager.get_screen('ScreenMyDBObject').ids.deleteButton.on_release = lambda: self.deleteObject(chip.text, textinp.hint_text)
        myapp.screenManager.current = 'ScreenMyDBObject'

    def deleteObject(self, name, typeObject):
        if typeObject == 'Таблица':
            cursor.execute('DROP TABLE ' + name)
            toast('Таблица ' + name + ' была удалена')
        elif typeObject == 'Представление':
            cursor.execute('DROP VIEW ' + name)
            toast('Представление ' + name + ' было удалено')
        elif typeObject == 'Триггер':
            cursor.execute('DROP TRIGGER ' + name)
            toast('Триггер ' + name + ' был удален')
        else:
            cursor.execute('DROP INDEX ' + name)
            toast('Индекс ' + name + ' был удален')
        myapp.screenManager.current = 'ScreenMyDB'
        
    def on_leave(self):
        global connection, cursor
        connection = sqlite3.connect('sq.db')                                                           #Соединение с базой данных
        cursor = connection.cursor()
        
    def deleteDB(self, tab):
        def handler():
            path = tab.path
            self.ids.tabs.remove_widget(tab)
            global_data['databases'].remove(path)
            insertToJSON()
            myapp.screenManager.get_screen('ScreenCards').ids.mydb.right_text = str(len(global_data['databases']))
            os.remove(path)
            dial.dismiss()
        dial = MyDialog(textBox = 'Вы уверены что хотите удалить данную БД?', source = 'help-circle', color = myapp.theme_cls.primary_color)
        box = MDBoxLayout(orientation='horizontal', size_hint=(1, None), adaptive_height=True, spacing=10)
        box.add_widget(MDRectangleFlatButton(text = 'Удалить', on_release = lambda x: handler()))
        box.add_widget(MDRectangleFlatButton(text = 'Отмена', on_release = lambda x: dial.dismiss()))
        dial.ids.box.add_widget(box)
        dial.open()
        
    
class ScreenCards(MDScreen):
    def info(self):                                                                           #Функция для вывода инструкции
        def instr(text):
            MyDialog(textBox = text, source = 'information', color = myapp.theme_cls.primary_color).open()
            dial.dismiss()
        dial = MyDialog(textBox = 'Инструкция. Выберите интересующий Вас вопрос:', source = 'information', color = myapp.theme_cls.primary_color)
        dial.ids.box.add_widget(MDRectangleFlatButton(text = 'Как проходить уроки?', on_release = lambda x: instr('Для начала Вам необходимо выбрать '+
'раздел команд SQL, интересующий Вас, затем выбрать урок по необходимой команде. После прочтения теоретического материала, содержащегося в каждом уроке, '+
'Вам предлагается пройти блок проверки, в котором будут задания на самостоятельное вписывание команд. При прохождении последнего урока '+
'раздела Вам предлагается пройти тест по всему разделу.')))
        dial.ids.box.add_widget(MDRectangleFlatButton(text = 'Как пользоваться терминалом?', on_release = lambda x: instr('Для того, чтобы открыть терминал, нажмите '+
'кнопку в форме треугольника. Кнопка справа копирует текст поля ввода. Введите текст в поле и нажмите кнопку "Готово". В зависимости от выполняемой команды результат '+
'будет разным. При правильном решении задачи в конце урока Ваш ответ будет сохранен, так что Вы всегда сможете к нему вернуться.')))
        dial.ids.box.add_widget(MDRectangleFlatButton(text = 'Как проходить тесты?', on_release = lambda x: instr('В конце раздела существует кнопка "Пройти тест", '+
'которая открывает тест. Для перемещения между вопросами перелистывайте влево и вправо. Для завершения теста нажмите кнопку "Завершить тест". Если более половины вопросов '+
'отвечено правильно, то тест засчитывается как пройденный, иначе - Вы не прошли тест. Тест всегда можно пройти повторно. Прохождение теста необходимо для завершения раздела.')))
        dial.ids.box.add_widget(MDRectangleFlatButton(text = 'Как открывать свои БД?', on_release = lambda x: instr('Перейдите к главному экрану, в меню слева выберите '+
'"Открыть БД". В файловом менеджере найдите свою БД. Ваша БД будет добавлена в список экрана "Мои БД". В дальнейшем Вы можете работать с добавленной БД. При изменении '+
'местоположения БД, выполните ее открытие снова.')))
        dial.ids.box.add_widget(MDRectangleFlatButton(text = 'Как создать новую БД?', on_release = lambda x: instr('Перейдите к главному экрану, в меню слева выберите '+
'"Создать БД". В файловом менеджере выбермите папку, в которой будет храниться Ваша БД. В конце нажмите на кнопку справа внизу в виде галочки. Далее назовите Вашу БД '+
'и нажмите кнопку "Создать БД". В разделе "Мои БД" появится созданная Вами БД, Вы сможете работать в ней.')))
        dial.ids.box.add_widget(MDRectangleFlatButton(text = 'Как управлять своими БД?', on_release = lambda x: instr('В разделе "Мои БД" хранятся добавленные Вами БД. '+
'Для перемещения между ними используйте вкладки сверху. Для удаления БД используйте кнопку в виде корзины, справа от пути БД. Вы можете просмотреть таблицы, триггеры и '+
'представления БД, при нажатии на них Вы увидите более подробную информацию. Внизу экрана находится терминал, в котором Вы можете выполнить команды к БД.')))
        dial.open()
        
    def oprog(self):                                                                          #Функция для вывода информации о программе
        MyDialog(textBox = 'Программный продукт был создан в рамках дипломного проекта курсантом 431 группы Хачатрян О. А. Дата создания системы - 14.06.2023', source = 'information', color = myapp.theme_cls.primary_color).open() 
        
    def createDB(self):
        self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path = self.select_path, show_hidden_files = False, selector='folder')
        if (platform == 'android'):
          try:
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            primary_ext_storage = primary_external_storage_path()
            self.file_manager.show(primary_ext_storage)
          except Exception as e:
            toast(e)
        try:
            self.file_manager.show_disks()  # output manager to the screen
        except Exception as e:
            toast(e)
            self.file_manager.show('/')
        
    def openDB(self):
        self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path = self.select_path, show_hidden_files = False, selector='file', ext = ['.db'])
        if ( platform == 'android' ):
          try:
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            primary_ext_storage = primary_external_storage_path()
            self.file_manager.show(primary_ext_storage)
          except Exception as e:
            toast(e)
        try:
            self.file_manager.show_disks()  # output manager to the screen
        except Exception as e:
            toast(e)
            self.file_manager.show('/')

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.file_manager.close()
        if path == '':
            path = myapp.dir
        path = path.replace('\\', '/')
        if self.file_manager.selector == 'folder':  #если создать бд (выбор папки)
            dial = MyDialog(textBox = 'Назовите вашу БД:', source = 'database-plus', color = myapp.theme_cls.primary_color)
            dial.ids.box.add_widget(MDTextField(hint_text="Путь", mode="rectangle", text = path, readonly=True))
            dial.ids.box.add_widget(MDTextField(hint_text="Имя БД", mode="rectangle"))
            dial.ids.box.add_widget(MDRectangleFlatButton(text = 'Создать БД', on_release = dial.createDB))
            dial.open()
        else:                                       #иначе открыть бд
            if not path in global_data['databases']:
                global_data['databases'].append(path)
                insertToJSON()
                dial = MyDialog(textBox = 'Выбранная БД была успешно добавлена!', source = 'check-circle', color = 'green')
                dial.ids.box.add_widget(MDRectangleFlatButton(text = 'Перейти в Мои БД', on_release = dial.openMyDB))
                myapp.screenManager.get_screen('ScreenCards').ids.mydb.right_text = str(len(global_data['databases']))
                dial.open()
            else:
                dial = MyDialog(textBox = 'Такая БД уже имеется в списке', source = 'check-circle', color = 'green')
                dial.ids.box.add_widget(MDRectangleFlatButton(text = 'Перейти в Мои БД', on_release = dial.openMyDB))
                dial.open()

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''
        self.file_manager.close()
        
class Onboarding(MDScreen):                                                                         #Класс приветствующего окна
    def finish_callback(self):                                                                      #Функция выхода из окна приветствия
        global global_data
        global_data['databases'][0] = myapp.dir + global_data['databases'][0]
        global_data['theme'] = myapp.theme_cls.theme_style
        global_data['obuch_passed'] = True
        insertToJSON()
        myapp.screenManager.current = 'ScreenCards'
        myapp.screenManager.current_screen.ids.mydb.right_text = str(len(global_data['databases']))
        myapp.cards()

class MD3Card(MDCard):                                                                              #Класс разделов с уроками
    source = StringProperty()
    value = NumericProperty()

    def on_release(self):  #На нажатие карточки раскрывается список
        panel = self.children[0]
        panel.check_open_panel(panel.panel_cls)
        
class TextInp(MDBoxLayout):                                                                         #Класс текстового поля ввода команд
    text = StringProperty()
    isKontrol = BooleanProperty()
        
class MyDialog(MDDialog):                                                                             #Класс информационного окна
    textBox = StringProperty()
    text = '\n\n\n\n\n\n\n\n'
    source = StringProperty()
    color = ColorProperty()

    def createDB(self, button):
        path = button.parent.children[2].text
        if path != '':
            path += '/'
        else:
            path = myapp.dir
        filename = button.parent.children[1].text
        if filename != '' and len(filename) > 3:
            if filename.casefold()[-3:] == '.db':
                filename = filename[:-2] + 'db'
        sqlite3.connect(path + filename).close()
        if path + filename not in global_data['databases']:
            global_data['databases'].append(path + filename)
            insertToJSON()
            myapp.screenManager.get_screen('ScreenCards').ids.mydb.right_text = str(len(global_data['databases']))
            self.dismiss()
        else:
            button.parent.children[1].helper_text = 'Такая БД уже имеется, выберите другое имя'
            button.parent.children[1].error = True

    def openMyDB(self, button):
        myapp.screenManager.current = 'ScreenMyDB'
        self.dismiss()
        
    def openCards(self, button):
        myapp.screenManager.current = 'ScreenCards'
        self.dismiss()
        
class Terminal(MDBoxLayout):                                                                        #Класс терминала
    text_label = StringProperty()
    text = StringProperty()
    obuch = StringProperty()

    def check(self, textinp, obuch):                                                           #Функция проверки введенного кода
        global global_data
        try:
            c = textinp.text.replace('\n', ' ').strip()
            cursor.execute(c)
            connection.commit()
            table_name = Parser(c).tables[0]
            select = False                                                                      #Выводить ли данные таблицы
            c_casefold = c.casefold()
            if c_casefold.count('create') == 1:
                '''
                #t = textinp.text.split()[2].split("(")[0]
                try:
                    #t = textinp.text.split("(")[0].split()[-1]
                    cursor.execute('select sql from sqlite_master where name = "' + table_name + '";')
                    myapp.answer = cursor.fetchone()[0]
                except Exception as e: print(e)'''
                cursor.execute('pragma table_info("' + table_name + '");')
                cols = [i[1] for i in cursor.fetchall()]                                               #считывание столбцов
                data = []
                for k in cols:
                    data.append(((k, dp(30))))
                #self.add_widget(Video(source='winner-7304198-5978814.mp4', options={'eos':'loop'}))
                self.add_widget(MDDataTable(size_hint = (1, None), column_data = data))
                #cursor.execute('drop table "' + t + '";')
                toast('Таблица ' + table_name + ' была создана')
                select = True
            elif c_casefold.count('drop') == 1:
                #table_name = re.split(' table ', c, flags=re.IGNORECASE)[1].split(' ')[0].strip()
                toast('Таблица ' + table_name + ' была удалена')
            elif c_casefold.count('alter') == 1:
                #table_name = re.split(' table ', c, flags=re.IGNORECASE)[1].split(' ')[0].strip()
                if c_casefold.count('rename') == 1:
                    t2 = re.split(' rename to ', c, flags=re.IGNORECASE)[1]
                    toast('Таблица ' + table_name + ' была переименована в ' + t2)
                else:
                    t2 = re.split(' add column ', c, flags=re.IGNORECASE)[1]
                    toast('В таблицу ' + table_name + ' был добавлен столбец ' + t2)
            elif c_casefold.count('insert') == 1:
                select = True
                #table_name = re.split(' into ', c, flags=re.IGNORECASE)[1].split(' ')[0].strip()
                toast('В таблицу ' + table_name + ' были добавлены строки')
            elif c_casefold.count('update'):
                #table_name = re.split(' set ', c, flags=re.IGNORECASE)[0].split(' ')[1].strip()
                select = True
            elif c_casefold.count('delete'):
                #table_name = re.split(' from ', c, flags=re.IGNORECASE)[1].split(' ')[0].strip()
                select = True
            else: #select
                #table_name = re.split(' from ', c, flags=re.IGNORECASE)[1].split(' ')[0].strip()
                select = True
            if isinstance(self.children[0], MDDataTable):
                self.remove_widget(self.children[0])
            if obuch == 'kontrol':
                print(c_casefold.replace(' ', ''))
                print(myapp.answer.casefold().replace(';', '').replace(' ', ''))
                if c_casefold.replace(' ', '').replace(';', '') == myapp.answer.casefold().replace(';', '').replace(' ', ''):
                    MyDialog(textBox = 'Верно', source = 'check-circle', color = 'green').open()
                    lesson = myapp.lesson
                    razdel = myapp.razdel
                    if not global_data[razdel][lesson]:
                        global_data[razdel][lesson] = True
                        insertToJSON()
                        myapp.cur_card.value += 100/len(global_data[razdel].keys())
                    tree = ET.parse(str(myapp.razdel_num) + '/' + str(myapp.lesson_num) + '.xml')
                    root = tree.getroot()
                    for elem in root.iter('code'):
                        if elem.attrib.get('type') == 'answer':
                            elem.text = textinp.text
                    tree.write(str(myapp.razdel_num) + '/' + str(myapp.lesson_num) + '.xml')
                else:
                    MyDialog(textBox = 'Неверно, попробуйте еще', source = 'close-circle', color = 'red').open()
                    return
            if select:
                if table_name[-1] == ';':  #убираем в конце ;
                    table_name = table_name[:-1]
                cursor.execute('select * from ' + table_name)
                data_col = []           #Столбцы
                data = cursor.fetchall()
                if len(data) == 0:
                    cursor.execute('pragma table_info("' + table_name + '");')
                    data = [i[1] for i in cursor.fetchall()]
                    for k in data:
                        data_col.append(((k, dp(30))))
                    data.clear()
                else:
                    for k in cursor.description:
                        data_col.append(((k[0], dp(30))))
                    data.pop(0)
                self.add_widget(MDDataTable(size_hint = (1, None), column_data = data_col, row_data = data, use_pagination=True, height=Window.height/2))
        except Exception as e:
            if str(e).endswith('already exists'):
                toast('Объект БД уже существует')
            elif str(e).startswith('there is already another table or index with this name'):
                toast('Объект БД с таким именем уже существует')
            elif str(e).startswith('no such table'):
                toast('Такой таблицы нет, создайте ее')
            elif str(e).startswith('duplicate column name'):
                toast('Поле с таким названием уже есть')
            else:
                MyDialog(textBox = 'Некорректный ввод, попробуйте еще\n' + str(e), source = 'close-circle', color = 'red').open()
            print(e)
            return
        
class Tab(MDFloatLayout, MDTabsBase):
    path = StringProperty()

def insertToJSON():
    global global_data
    with open('data.json', 'w', encoding = 'utf8') as f:
        json.dump(global_data, f)
        
if __name__ == '__main__':
    #titles, lessons, values = [], [], []
    connection = sqlite3.connect('sq.db')                                                           #Соединение с базой данных
    cursor = connection.cursor()
    cursor.execute("PRAGMA database_list;")
    curr_table = cursor.fetchall()

    with open('data.json', 'r', encoding = 'utf8') as f:
        global_data = json.load(f)
    #cursor.execute('select sql from sqlite_master where name = "DATA";')   
    myapp = MyApp()
    myapp.run()
    cursor.close()
    connection.close() 
