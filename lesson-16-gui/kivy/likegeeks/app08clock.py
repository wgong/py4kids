
2
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
from kivy.app import App
 
from kivy.uix.button import  Button
 
from kivy.clock import Clock
 
class ClockExample(App):
 
    i=0
 
    def build(self):
 
        self.mybtn = Button(text='Number of Calls')
 
        Clock.schedule_interval(self.clock_callback, 2)
 
        return self.mybtn
 
    def clock_callback(self, dt):
 
        self.i+= 1
 
        self.mybtn.text = "Call = %d" % self.i
 
ClockExample().run()