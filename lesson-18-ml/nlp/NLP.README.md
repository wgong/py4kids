

## Setup
pip3 install -r requirements.txt

cd ~/projects/NLP/

virtualenv nlp

source nlp/bin/activate

cd ~/projects/NLP/nlp/bin

./python3 -m spacy download en_core_web_md
./python3 -m spacy download en_trf_bertbaseuncased_lg

./pip3 install jupyter notebook
./pip3 install sklearn nltk


./nlp/lib/python3.8/site-packages (from spacy<2.4.0,>=2.3.0-



## Natural Language Processing in Python 

### 10 Free Top Notch Natural Language Processing Courses
https://www.kdnuggets.com/2019/10/10-free-top-notch-courses-natural-language-processing.html

### Advanced NLP with spaCy
https://course.spacy.io/en/
https://github.com/ines/spacy-course

Notebook version:
https://github.com/cristianasp/spacy
git@github.com:wgong/spacy.git

pip install jieba

python3 -m spacy download en_core_news_sm
python3 -m spacy download en_core_web_sm
python3 -m spacy download zh_core_web_sm

### pycon2020 - KeithGalli

https://github.com/keithgalli/pycon2020

### nlp-in-python-tutorial
https://github.com/adashofdata/nlp-in-python-tutorial


### Complete Text Processing | End to End NLP Tutorial 

https://www.youtube.com/watch?v=VyDmQggfsZ0

### DataCamp

https://learn.datacamp.com/skill-tracks/natural-language-processing-in-python


### Topic Modeling

- Topic Modeling: An Introduction - https://monkeylearn.com/blog/introduction-to-topic-modeling/
- BERTopic : https://github.com/MaartenGr/BERTopic
    - NLP with BERT Transformers - EXPLAINED! : - https://www.youtube.com/watch?v=TLPmlVeEf1k
    - How to Use Bertopic for Topic Modeling and Content Analysis? - https://www.holisticseo.digital/python-seo/topic-modeling/
- Topic Modeling and Latent Dirichlet Allocation (LDA) using Gensim and Sklearn
    - Part 1 https://www.analyticsvidhya.com/blog/2021/06/topic-modeling-and-latent-dirichlet-allocationlda-using-gensim-and-sklearn-part-1/
    - Part 2: https://www.analyticsvidhya.com/blog/2021/06/part-2-topic-modeling-and-latent-dirichlet-allocation-lda-using-gensim-and-sklearn/
    - Part 3 https://www.analyticsvidhya.com/blog/2021/06/part-3-topic-modeling-and-latent-dirichlet-allocation-lda-using-gensim-and-sklearn/

- Beginners Guide to Topic Modeling in Python https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/


- Bert For Topic Modeling ( Bert vs LDA ) https://medium.com/analytics-vidhya/bert-for-topic-modeling-bert-vs-lda-8076e72c602b
    - https://github.com/mcelikkaya/medium_articles2/blob/main/bertlda_topic_modeling.ipynb

#### BERTopic
```
cd ~/projects/NLP
virtualenv bertopic
source bertopic/bin/activate
pip install numpy==1.20
pip install huggingface-hub==0.0.12
```