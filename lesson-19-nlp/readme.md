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
$ conda install -c conda-forge gensim  # took long time 30mins: cancel
$ pip install gensim

Successfully built gensim smart-open
Installing collected packages: scipy, boto, chardet, urllib3, idna, requests, jmespath, docutils, botocore, s3transfer, boto3, smart-open, gensim
Successfully installed boto-2.49.0 boto3-1.11.0 botocore-1.14.0 chardet-3.0.4 docutils-0.15.2 gensim-3.8.1 idna-2.8 jmespath-0.9.4 requests-2.22.0 s3transfer-0.3.0 scipy-1.4.1 smart-open-1.9.0 urllib3-1.25.7


```
