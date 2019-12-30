from kivy.app import App
from kivy.uix.label import Label

class App01Label(App):
    def build(self):
        return Label(text="Hello Kivy!\n[u][color=ff0066][b]Welcome[/b][/color] To [i][color=ff9933]Like[/i]Geeks[/color][/u]", 
            font_size='60', 
            markup = True)

if __name__ == "__main__":
    App01Label().run()