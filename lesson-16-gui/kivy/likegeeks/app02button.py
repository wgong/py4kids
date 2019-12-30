from kivy.app import App
from kivy.uix.button import Button

class App02Button(App):
    def build(self):
        return Button(text="Hello Kivy!", 
            background_color=(1,0,0,1),
            pos=(100,100), 
            size_hint = (.2, .2))

if __name__ == "__main__":
    App02Button().run()