import PySimpleGUI as sg

sg.change_look_and_feel('Dark Blue 8')

for i in range(10000):
    sg.OneLineProgressMeter('One Line Meter Example', i + 1, 1000, 'key')
