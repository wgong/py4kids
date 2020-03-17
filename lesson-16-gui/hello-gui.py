# http://www.blog.pythonlibrary.org/2019/10/23/a-brief-intro-to-pysimplegui/

import PySimpleGUI as sg


# Create some elements
layout = [
    [sg.Text("What's your name?"), sg.InputText(key='K_INPUT')],
    [sg.Button('OK'), sg.Button('Cancel')],
    [sg.Output(key='K_DEBUG', size=(80, 10))],
]
 
# Create the Window
window = sg.Window('Hello PySimpleGUI', layout)

el_output = window.Element('K_DEBUG')

# Create the event loop
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        # User closed the Window or hit the Cancel button
        break
    el_output.Update('')
    print(f'Event: {event}')
    print(str(values['K_INPUT']))
 
window.close()