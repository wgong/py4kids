from kivy.app import App
 
from kivy.uix.button import  Button
 
from kivy.uix.textinput import TextInput
 
from kivy.uix.boxlayout import BoxLayout
 
class ClearApp(App):
 
    def build(self):
 
        self.box = BoxLayout(orientation='vertical', spacing=20)
 
        self.txt = TextInput(hint_text='Write here', size_hint=(1.0,0.5))
 
        self.btn = Button(text='Clear All', on_press=self.clearText, size_hint=(.5,.1))
 
        self.box.add_widget(self.txt)
 
        self.box.add_widget(self.btn)
 
        return self.box
 
    def clearText(self, instance):
 
        self.txt.text = ''
 
ClearApp().run()