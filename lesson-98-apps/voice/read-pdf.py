import pyttsx3
import PyPDF2
filename = 'python_tutorial.pdf'
filename = 'GFG.pdf'

book = open(filename, 'rb')
pdfReader = PyPDF2.PdfFileReader(book)
pages = pdfReader.numPages

speaker = pyttsx3.init()
for num in range(0, pages):
    page = pdfReader.getPage(num)
    text = page.extractText()
    speaker.say(text)
    speaker.runAndWait()