from kivymd_extensions.akivymd.uix.onboarding import *  #для красивых переходов и множества красивых виджетов
from kivymd.uix.screen import MDScreen
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
                source: 'desk.png'
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
                        source: 'dark2light.png'
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
                            text: 'Выберите тему приложения'
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
                              
            
<MD3Card>
    padding: 4
    size_hint: None, None
    size: "200dp", "100dp"

    MDRelativeLayout:
    
        MDIconButton:
            icon: "arrow-right-thick"
            pos_hint: {"top": 1, "right": 1}
            on_release: root.change_widget()

        MDLabel:
            id: label
            text: root.text
            adaptive_size: True
            color: "grey"
            pos: "12dp", "12dp"
            bold: True


""")
        
