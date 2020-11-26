import pyttsx3
# book = open('of-human-bondage.txt')
# text = book.read()

speaker = pyttsx3.init()

speaker.say("hello world from Wen")
speaker.runAndWait()