import webbrowser

url = 'https://pythonexamples.org'

webbrowser.register('chrome',
	None,
	webbrowser.BackgroundBrowser("/usr/bin/google-chrome"))
webbrowser.get('chrome').open_new(url)
