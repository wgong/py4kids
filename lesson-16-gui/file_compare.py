# https://towardsdatascience.com/learn-how-to-quickly-create-uis-in-python-a97ae1394d5

import PySimpleGUI as sg
import re
import hashlib


def hash(fname, algo):
    if algo == 'MD5':
        hash = hashlib.md5()
    elif algo == 'SHA1':
        hash = hashlib.sha1()
    elif algo == 'SHA256':
        hash = hashlib.sha256()
    with open(fname) as handle: #opening the file one line at a time for memory considerations
        for line in handle:
            hash.update(line.encode(encoding = 'utf-8'))
    return(hash.hexdigest())

layout = [
    [sg.Text('File 1'), sg.InputText(), sg.FileBrowse(),
     sg.Checkbox('MD5'), sg.Checkbox('SHA1')
     ],
    [sg.Text('File 2'), sg.InputText(), sg.FileBrowse(),
     sg.Checkbox('SHA256')
     ],
    [sg.Output(size=(88, 20))],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('File Compare', layout)

while True:                             # The Event Loop
    print("*"*80)
    event, values = window.read()
    print(event, values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Submit':
        file1 = file2 = isitago = None
        # print(values[0],values[3])
        if values[0] and values[3]:
            # for Windows
            # file1 = re.findall('.+:\/.+\.+.', values[0])
            # file2 = re.findall('.+:\/.+\.+.', values[3])

            file1 = values[0]
            file2 = values[3]
            isitago = 1
            if not file1 and file1 is not None:
                print('Error: File 1 path not valid.')
                isitago = 0
            elif not file2 and file2 is not None:
                print('Error: File 2 path not valid.')
                isitago = 0
            elif (int(values[1]) + int(values[2]) + int(values[4])) < 1:
                print('Error: Choose at least one type of Encryption Algorithm')
            elif isitago == 1:
                print('Info: Filepaths correctly defined.')
                algos = [] #algos to compare
                if values[1]: 
                    algos.append('MD5')
                if values[2]: 
                    algos.append('SHA1')
                if values[4]: 
                    algos.append('SHA256')

                filepaths = [] #files
                filepaths.append(values[0])
                filepaths.append(values[3])
                print('Info: File Comparison using:', algos)
                for algo in algos:
                    print(algo, ':')
                    digest1 = hash(filepaths[0], algo)
                    digest2 = hash(filepaths[1], algo)
                    print(filepaths[0], ':', digest1)
                    print(filepaths[1], ':', digest2)
                    if digest1 != digest2:
                        print('Files do NOT match for ', algo)
                    else:
                        print('Files match for ', algo)
        else:
            print('Please choose 2 files.')

window.close()
