import requests

def sum_list(num_list):
    return sum(num_list)

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())
