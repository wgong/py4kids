from os.path import dirname, join
from kivy.app import App
from kivy.uix.videoplayer import VideoPlayer

class VideoPlayerApp(App):

    def build(self):
        curdir = dirname(__file__)
        filename = join(curdir, 'cityCC0.mpg')
        return VideoPlayer(source=filename, state='play')


if __name__ == '__main__':
    VideoPlayerApp().run()
