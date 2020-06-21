#!/usr/bin/env python
# coding: utf-8

# In[12]:


import sys


# In[4]:


import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
# CountVectorizer will take care of converting strings to numerical vectors
from nltk.corpus import stopwords

stopwords_en = stopwords.words('english')

def clean_string(text):
    text = ''.join([ch for ch in text if ch not in string.punctuation])
    text = text.lower()
    text = ' '.join([w for w in text.split() if w not in stopwords_en])
    return text


# In[5]:


def cosim_strings(s1, s2):
    sentences = [s1, s2]
    cleaned = list(map(clean_string, sentences))
    vectorizer = CountVectorizer().fit_transform(cleaned)
    vectors = vectorizer.toarray()
    
    vec1 = vectors[0].reshape(1,-1)
    vec2 = vectors[1].reshape(1,-1)
    return cosine_similarity(vec1, vec2)[0][0]

# s1 = 'foo bar sentence'
# s2 = 'another string similar previous sent'
# cosim_strings(s1, s2)
# In[13]:


if __name__ == "__main__":
    if len(sys.argv) > 2:
        f1, f2 = sys.argv[1], sys.argv[2]
        with open(f1) as f:
            s1 = f.read()
        with open(f2) as f:
            s2 = f.read()
        print(cosim_strings(s1, s2))
        sys.exit(0)
    else:
        print(f"python {__file__} f1.txt f2.txt")
        sys.exit(1)





