from bs4 import BeautifulSoup
from urllib.request import urlopen
import pymorphy2
import nltk
import string
from nltk.corpus import stopwords
from collections import Counter
import math
from nltk.tokenize import RegexpTokenizer
import os
import pymysql as db


def parser(file_w):
    try:

        html_doc = urlopen('http://localhost/pase/' + str(file_w)).read()
        soup = BeautifulSoup(html_doc)
        corpus_list = []

        # text processing
        text_list_norm_form = []
        text = soup.p.string.replace('.', ' ').lower()
        tokenizer = RegexpTokenizer(r'\w+')
        text_list_split = tokenizer.tokenize(text)

        # text_list_split = text.split(' ')
        text_list_filter = list(filter(None, text_list_split))
        for word in text_list_filter:
            morph = pymorphy2.MorphAnalyzer()
            norm_word = morph.parse(word)[0].normal_form
            text_list_norm_form.append(norm_word)
        filtered_text_list = [word for word in text_list_norm_form if word not in stopwords.words('russian')]
        total_text = ' '.join(filtered_text_list)
        corpus_list.append(filtered_text_list)

        # title processing
        title_list_norm_form = []
        title = soup.find('span', style='font-size: 9pt; color: #000000').text.rstrip().lstrip().lower()
        title_list = title.split(' ')
        for t_word in title_list:
            t_word_norm = morph.parse(t_word)[0].normal_form
            title_list_norm_form.append(t_word_norm)
        filtered_title_list = [t_word for t_word in title_list_norm_form if t_word not in stopwords.words('russian')]
        # corpus_list.append(filtered_title_list)
        total_title = ' '.join(filtered_title_list)


        # keyword processing
        key_word_list = []
        dict_info = {}
        for link in soup.find_all('td', width=504):
            for link1 in link.find_all('a'):
                key_word = link1.string
                key_word_list.append(key_word)
        key_word_list = list(filter(None, key_word_list))
        key_word_list_lower = []
        for kwl in key_word_list:
            key_word_list_lower.append(str(kwl).lower())
        filtered_keyword_list = [kwl for kwl in key_word_list_lower if kwl not in stopwords.words('english')]
        corpus_list.append(filtered_keyword_list)
        key_word_string = ' '.join(filtered_keyword_list)

        # author processing
        for tag in soup.find_all('span', style='white-space: nowrap', ):
            for mail in tag.find_all('a', href=True):
                # print(mail['href'])
                author = mail['href']

        dict_info['author'] = author[7:]
        dict_info['text'] = total_text
        dict_info['title'] = total_title
        dict_info['key_word_list'] = key_word_string

        con = db.connect(host='localhost', user='root', passwd='admin', db='elib', use_unicode=True, charset='utf8')
        cur = con.cursor()
        cur.execute('SET NAMES `utf8`')
        cur.execute("""INSERT INTO kate VALUES (%s,%s)""", (dict_info['author'], dict_info['title'] +" " + dict_info['text'] + " "+ dict_info['key_word_list']))
        con.commit()
    except:
        print("Файл с ошибкой")

if __name__ == "__main__":
    # file_w = 'test.html'
    # parser(file_w)
    directory = '/var/www/html/pase/'
    path = os.listdir(directory)
    print(path)
    i = 0
    for p in path:
        directory_next = '/var/www/html/pase/' + str(p)
        files = os.listdir(directory_next)
        for file_name in files:
            i += 1
            file_w = str(p) + '/' + file_name
            print(file_w, i)
            parser(file_w)
