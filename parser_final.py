from bs4 import BeautifulSoup as bs
# import nltk
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import os
import sqlite3


conn = sqlite3.connect("forward2.db")
def forward_table(doc_id, address, header):
    
    

    # cursor to move around the database
    c = conn.cursor()

    sql = "INSERT INTO 'forward' (doc_id, address, heading) VALUES( ?, ?, ?)"
    try:
        c.execute(sql, (doc_id, address, header,))
    except:
        return
    


def store_words(doc_id, word_list):
    
    
    c = conn.cursor()
    for i_ in range(0, len(word_list), 1):
        sql = "INSERT INTO 'words' (doc_id, word, frequency) VALUES( ?, ?, ?)"
        try:
            c.execute(sql, (doc_id, word_list[i_][0], word_list[i_][1],))
            
        except:
            continue
        


def get_doc_id(word_):

   
    
    # cursor to move around the database
    c = conn.cursor()
    try:
        c.execute("SELECT doc_id FROM words WHERE words = ?", (word_,))
        rows = c.fetchall()
    except:
        return
    return rows


def get_frequency(word_, doc_id_):
    

    # cursor to move around the database
    c = conn.cursor()
    try:
        c.execute("SELECT frequency FROM words WHERE words = ? AND doc_id = ?", (word_, doc_id_))
        rows = c.fetchall()
    except:
        return
    return rows


def store_reverse_index(word_id, word, doc_id, frequency):
    

    # cursor to move around the database
    c = conn.cursor()
    try:
        sql = "INSERT INTO 'reverse' (word_id, word, doc_id, frequency) VALUES( ?, ?, ?, ?)"
        c.execute(sql, (word_id, word, doc_id, frequency))
    except:
        return
    


stop_words = set(stopwords.words('english'))  # sets stopwords

file = r"C:\articles"

doc_id = 0

# forward = {'doc': doc_id, 'word_list': for_index}
master_unique = []
start = time.time()
for root, dirnames, filenames in os.walk(file):
    for filename in filenames:
        if filename.endswith('.html'):
            fname = os.path.join(root, filename)
            with open(fname, encoding='utf-8') as handle:

                doc_id += 1
                print(doc_id)
                # opens file
                # file = open(r"Saturn.html", encoding="utf8")
                try:
                    soup = bs(handle, 'html.parser')
                    
                    # makes soup
                except:
                    continue
                # allows for only text
                for script in soup(["script", "style"]):
                    script.decompose()

                sentence = soup.get_text()  # parses soup
                sentence = sentence.lower()

                headers = soup.find_all('h1')
                h = [header.get_text() for header in headers]
                if h:
                    h = h[0]
                else:
                    doc_id -= 1
                    continue
                
                tokenizer = RegexpTokenizer(r'\w+')  # sets punctuation
                tokens = tokenizer.tokenize(sentence)  # separates string into list of words and removes punctuation
                
                filtered_sentence = []
                # lemmatized_list = []

                wnl = WordNetLemmatizer()

                # removes stopwords
                y = pos_tag(tokens)
                # lemmatized_list.append(y)

                for word, tag in pos_tag(tokens):
                    if word not in stop_words:
                        wntag = tag[0].lower()
                        if word.isdigit():
                            continue
                        wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
                        lemma = wnl.lemmatize(word, wntag) if wntag else word
                        filtered_sentence.append(lemma)
                    # print(filtered_sentence)

                unique = []
                forwardI = [[]]
                for i in range(0, len(filtered_sentence), 1):
                    cou = 0
                    if filtered_sentence[i] in unique:
                        continue
                    else:
                        unique.append(filtered_sentence[i])
                        for j in range(0, len(filtered_sentence), 1):
                            if filtered_sentence[i] == filtered_sentence[j]:
                                cou += 1
                        forwardI.append([filtered_sentence[i], cou])

                forwardI = forwardI[1:]
                

                store_words(doc_id, forwardI)
                forward_table(doc_id, fname, h)
                conn.commit()
        for i in range(0, len(unique), 1):
            if unique[0] not in master_unique:
                master_unique.append(unique[i])




# REVERSE INDEXER
word_id = 0
print("Reverse Indexing Started")
for i in range(0, len(master_unique), 1):
    word_id +=1
    print(word_id)
    doc_id_list = get_doc_id(master_unique[i])
    for j in range(0, len(doc_id_list), 1):
        frequency = get_frequency(word, doc_id_list[j])
        store_reverse_index(word_id, master_unique[i], doc_id_list[j], frequency)
    conn.commit()
end = time.time()
print(end - start, "secs")
