from django.conf import settings
import os, json, csv
from djangotanach.books import TANACH_BOOKS
from collections import defaultdict

PATTERN = 'abgdefzhjiklmnxopsqrct'
HEBREW_UNICODE = "אבגדהוזחטיכלמנסעפצקרשת"
KOREN = "ABGDHWZX+YKLMNSOPCQR$T"

HEBREW_EXTRA = 'ךםןףץ'
KOREN_EXTRA = 'KMNPC'
# 'ךכ': 14070,	    כ, k
# 'םמ': 41451,	    מ, m
# 'ןנ': 15299, 	    נ, n
# 'ףפ': 2562,  	    פ, p
# 'ץצ': 3290, 		צ, c

JSON_FOLDER = os.path.join(settings.BASE_DIR, 'djangotanach', 'json','all')
EN_FOLDER = os.path.join(settings.BASE_DIR, 'djangotanach', 'json','eng')
CSV_FOLDER = os.path.join(settings.BASE_DIR, 'djangotanach', 'csv')

def save_file(fname, datas, is_csv=True):
    csvfile=open(f'{CSV_FOLDER}/{fname}','w')
    if is_csv:
        cwriter = csv.writer(csvfile)
        cwriter.writerows(datas)
    else:
        for line in datas:csvfile.write(f"{line}\n")
                     
def a():
    not_found=defaultdict(lambda: 0)
    koren_data=[]
    counts = []
    for bkcount,book in enumerate(TANACH_BOOKS):        
        fname = book["book"].replace(' ','_')
        data = json.loads(open(f'{JSON_FOLDER}/{fname}.json').read())
        print(bkcount+1,':', book)
        print('chapters:',len(data['text']))
        vcount = 0
        counts.append([len(c) for c in data['text']])
        for chapter in data['text']:
            
            vcount += len(chapter)
            # lines in genesis chapter x
            for line in chapter:
                koren_line=[]
                for word in line.split():
                    koren = ''
                    for letter in word:
                        if letter == '\u200d': continue
                        if letter in '[]<br>smal/־': continue
                        if letter in HEBREW_EXTRA: 
                            koren+=KOREN_EXTRA[HEBREW_EXTRA.index(letter)]
                        else:
                            koren+=KOREN[HEBREW_UNICODE.index(letter)]
                        # except ValueError:                            
                        #     not_found[letter]+=1
                        
                    koren_line.append(koren)
                koren_data.append(koren_line)
        print('verses:',vcount)
        print('-'*10)
    print(not_found)
    save_file('words.csv',koren_data)
    save_file('counts.csv',counts)
    # {'ם': 41451, 'ץ': 3290, 'ך': 14070, 'ן': 15299, 'ף': 2562, '\u200d': 79, '־': 418})

def b():
    en_data=[]
    counts = []
    
    for bkcount,book in enumerate(TANACH_BOOKS):  
        data = json.loads(open(f'{EN_FOLDER}/en{bkcount+1}.json').read())
        print(bkcount+1,':', book)
        print('chapters:',len(data['text']))
        vcount = 0
        counts.append([len(c) for c in data['text']])
        for chapter in data['text']:            
            vcount += len(chapter)
            for line in chapter: en_data.append(line)
        print('verses:',vcount)
        print('-'*10)
    save_file('en_words.csv',en_data,is_csv=False)
    save_file('en_counts.csv',counts)

b()