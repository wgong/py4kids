3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
from kivy.base import runTouchApp
 
from kivy.lang import Builder
 
root = Builder.load_string(r'''
 
ScrollView:
 
    Label:
    
        text: 'Scrollview Example' * 100
        
        font_size: 30
        
        size_hint_x: 1.0
        
        size_hint_y: None
        
        text_size: self.width, None
        
        height: self.texture_size[1]
        
''')
 
runTouchApp(root)