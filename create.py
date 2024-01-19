from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.screen import MDScreen
from kivymd import images_path
from kivymd.uix.widget import MDWidget
from kivymd.uix.floatlayout import MDFloatLayout

def create_schema():
    self = MDFloatLayout()
    self.size_hint = (1, None)
    self.size = (100, 100)
    self.add_widget(MDRoundFlatButton(text = "CREATE", pos_hint = {'x': 0, 'y': 0.5}))
    self.add_widget(MDRoundFlatButton(text = "TEMP\nTEMPORARY", pos_hint = {'x': 0.2, 'y': 0.5}))
    return self
      

