import csv
import re
import pymorphy2
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import pymysql as db


with open("/home/andrew/test_primer_1.csv", "r") as infile, open("/home/andrew/train_hse_data.vw", "ab") as outfile:
    reader = csv.reader(infile)
    i = 0
    try:
        for line in reader:
            i = i + 1

            #author processing
            author = str(line[0]).replace(" ", "_").lower()#.split(" ", "_")
            author_id = str('author_') + str(i)

            #title processing
            title_list_norm_form = []
            title = str(line[1]).replace('.', ' ').lower()
            tokenizer = RegexpTokenizer(r'\w+')
            title_list_split = tokenizer.tokenize(title)

            title_list_filter = list(filter(None, title_list_split))
            for word in title_list_filter:
                morph = pymorphy2.MorphAnalyzer()
                norm_word = morph.parse(word)[0].normal_form
                title_list_norm_form.append(norm_word)
            filtered_title_list = [word for word in title_list_norm_form if word not in stopwords.words('russian')]
            total_title = ' '.join(filtered_title_list)

            #text processing
            text_list_norm_form = []
            text = str(line[2]).replace('.', ' ').lower()
            tokenizer = RegexpTokenizer(r'\w+')
            text_list_split = tokenizer.tokenize(text)

            text_list_filter = list(filter(None, text_list_split))
            for word in text_list_filter:
                morph = pymorphy2.MorphAnalyzer()
                norm_word = morph.parse(word)[0].normal_form
                text_list_norm_form.append(norm_word)
            filtered_text_list = [word for word in text_list_norm_form if word not in stopwords.words('russian')]
            total_text = ' '.join(filtered_text_list)
            #print(total_text)

            #topics processing
            topics_list_norm_form = []
            topics = str(line[3]).replace(',', ' ').lower()
            tokenizer = RegexpTokenizer(r'\w+')
            topics_list_split = tokenizer.tokenize(topics)

            topics_list_filter = list(filter(None, topics_list_split))
            for word in topics_list_filter:
                morph = pymorphy2.MorphAnalyzer()
                norm_word = morph.parse(word)[0].normal_form
                topics_list_norm_form.append(norm_word)
            filtered_topics_list = [word for word in topics_list_norm_form if word not in stopwords.words('russian')]
            total_topics = ' '.join(filtered_topics_list)
            #print(total_topics)

            #keyword processing
            keyword_list_norm_form = []
            keyword = str(line[4]).replace(',', ' ').lower()
            tokenizer = RegexpTokenizer(r'\w+')
            keyword_list_split = tokenizer.tokenize(keyword)

            keyword_list_filter = list(filter(None, keyword_list_split))
            for word in keyword_list_filter:
                morph = pymorphy2.MorphAnalyzer()
                norm_word = morph.parse(word)[0].normal_form
                keyword_list_norm_form.append(norm_word)
            filtered_keyword_list = [word for word in keyword_list_norm_form if word not in stopwords.words('russian')]
            total_keyword = ' '.join(filtered_keyword_list)

            #WRITE IN DICTIONARY
            dict_info = {}
            dict_info['author'] = author
            dict_info['text'] = total_text
            dict_info['title'] = total_title
            dict_info['key_word_list'] = total_keyword
            dict_info['topics'] = total_topics

            #WRITE IN DATA BASE
            con = db.connect(host='localhost', user='root', passwd='admin', db='elib', use_unicode=True, charset='utf8')
            cur = con.cursor()
            cur.execute('SET NAMES `utf8`')
            cur.execute("""INSERT INTO hse_e VALUES (%s,%s,%s)""", (dict_info['author'], author_id, dict_info['title'] +" " + dict_info['text'] + " " + dict_info['key_word_list'] + " " + dict_info['topics']))

            ##WRITE IN FILE.VW
            #vw_line = ""
            #text_data = dict_info['title'] +" " + dict_info['text'] + " " + dict_info['key_word_list'] + " " + dict_info['topics']
            #vw_line = "title_" + str(i) + " " + "|@author"+" " + 'author_' + str(i) + " " +"|"
            #vw_line += "@text"+" " + text_data + " "
            #outfile.write(bytes(vw_line[:-1] + '\n', 'UTF-8'))
            #print(vw_line)

            print("String #", i)
    except:
        print("Error")