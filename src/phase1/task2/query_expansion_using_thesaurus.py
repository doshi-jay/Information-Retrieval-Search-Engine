# We have referred https://pythonprogramming.net/wordnet-nltk-tutorial/ for this task

import string
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.phase1 import Helper
import os

additional_query_terms = 8

h = Helper.Helper()
queries = list(h.get_queries().values())

newpath = "Query Expansion/"
if not os.path.exists(newpath):
    os.makedirs(newpath)

fout = open(newpath + "query_expanded_thesaurus.txt", "w", encoding="utf-8")
stop_words = set(stopwords.words("english"))

i = 1

for query in queries:
    query = query.lower()
    query = query.translate(str.maketrans('', '', string.punctuation))
    query_tokens = word_tokenize(query)
    filtered_query = [w for w in query_tokens if w not in stop_words]

    synonyms = []
    count = 0
    for word in filtered_query:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                # choose only 3 unique lemmas to get three synonyms for every term
                if count < 3:
                    if lemma.name() not in synonyms:
                        synonyms.append(lemma.name())
                        count += 1

        count = 0

    expanded_query = ' '.join(synonyms[:additional_query_terms] + filtered_query)
    fout.write(str(i) + " " + expanded_query + '\n')
    i += 1

fout.close()

