
from kivy.app import App
 
from kivy.lang import Builder
 
from kivy.uix.boxlayout import BoxLayout
 
kvWidget = """
 
MyWidget:
 
    orientation: 'vertical'
    
    canvas:
    
        Rectangle:
        
            size: self.size
            
            pos: self.pos
            
            source: 'kivy-6os.png'
            
"""
 
class MyWidget(BoxLayout):
 
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
 
class CanvasApp(App):
 
    def build(self):
        
        return Builder.load_string(kvWidget)
 
CanvasApp().run()