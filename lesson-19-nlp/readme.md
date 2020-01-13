## Courses
[Stanford CS224n: Natural Language Processing with Deep Learning](http://web.stanford.edu/class/cs224n/index.html)

## Tutorials

[NLP in python Tutorial by Alice Zhao @ pyOhio](https://youtu.be/xvqsFTUsOmc),  
[GitHub](https://github.com/adashofdata/nlp-in-python-tutorial)
covers: 
* sentiment analysis
* topic modeling
* text generation

### Setup
```
$ conda create --name nlp
$ conda activate nlp
$ sudo apt install python-pip
$ export PATH="/home/gong/.local/bin:$PATH"
$ pip install spacy  (pip install -U spaCy)
$ pip install ipython

# download en model
$ python -m spacy download en

# to load en model
import spacy
spacy.load('en') 
# or spacy.load('en_core_web_sm')

$ conda install -c conda-forge wordcloud

$ conda install -c conda-forge textblob

# topic modeling
$ conda install -c conda-forge gensim  # took long time 30mins

```