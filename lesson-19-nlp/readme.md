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

# visualize top words
$ conda install -c conda-forge wordcloud

# sentiment analysis
$ conda install -c conda-forge textblob

# topic modeling
$ conda install -c conda-forge gensim  # took long time 30mins: cancel
$ pip install gensim

Successfully built gensim smart-open
Installing collected packages: scipy, boto, chardet, urllib3, idna, requests, jmespath, docutils, botocore, s3transfer, boto3, smart-open, gensim
Successfully installed boto-2.49.0 boto3-1.11.0 botocore-1.14.0 chardet-3.0.4 docutils-0.15.2 gensim-3.8.1 idna-2.8 jmespath-0.9.4 requests-2.22.0 s3transfer-0.3.0 scipy-1.4.1 smart-open-1.9.0 urllib3-1.25.7

$ pip install jupyter

Successfully installed MarkupSafe-1.1.1 Send2Trash-1.5.0 attrs-19.3.0 backcall-0.1.0 bleach-3.1.0 decorator-4.4.1 defusedxml-0.6.0 entrypoints-0.3 ipykernel-5.1.3 ipython-7.11.1 ipython-genutils-0.2.0 ipywidgets-7.5.1 jedi-0.15.2 jinja2-2.10.3 jsonschema-3.2.0 jupyter-1.0.0 jupyter-client-5.3.4 jupyter-console-6.0.0 jupyter-core-4.6.1 mistune-0.8.4 nbconvert-5.6.1 nbformat-5.0.3 notebook-6.0.2 pandocfilters-1.4.2 parso-0.5.2 pexpect-4.7.0 pickleshare-0.7.5 prometheus-client-0.7.1 prompt-toolkit-2.0.10 ptyprocess-0.6.0 pygments-2.5.2 pyrsistent-0.15.7 pyzmq-18.1.1 qtconsole-4.6.0 terminado-0.8.3 testpath-0.4.4 traitlets-4.3.3 wcwidth-0.1.8 webencodings-0.5.1 widgetsnbextension-3.5.1

$ pip install bs4
$ pip install pandas
$ pip install sklearn


```

for 4-Topic-Modeling.ipynb, nltk resources to download
```
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
```
