from os.path import join, dirname
import re
import os
import nltk


class Helper:

    def __init__(self):
        self.start_path = dirname(dirname(dirname(__file__))) + '/data/'
        self.clean_corpus_dir = self.start_path + 'clean_corpus/'
        self.queries_file = self.start_path + 'queries.txt'
        with open('top100/1.txt', 'r') as f1:
            lines = f1.read().splitlines()
        f1.close()
        self.files_arr = []
        for d in lines:
            d = d.split(' ')[2][:-5].lower() + '.txt'
            self.files_arr.append(d)
        self.STOP_WORDS_FILE = self.start_path + 'common_words.txt'
        self.queries = dict()
        self.stop_words = list()
        self.total_number_of_terms_corpus = 0
        # maintain a global inverted index
        self.inverted_index = dict()
        # maintain a map for document -> vocabulary count
        self.document_term_count = dict()
        self.generate_inverted_index()

    def generate_inverted_index(self):
        # iterate through the files
        for f in os.listdir(self.clean_corpus_dir):
            if f not in self.files_arr:
                continue
            doc_name = f[:-4]

            with open(join(self.clean_corpus_dir, f), 'rb') as clean_file:
                text = clean_file.read().decode('utf-8')
            clean_file.close()

            # maintain a document-wide frequency distribution map
            freq_dist = nltk.FreqDist()
            # update the frequency distribution with the frequency distribution of unigrams in this document
            freq_dist.update(text.split())  # for uni-grams
            for ngram, frequency in freq_dist.items():
                # add the ngram and a posting list for this document in the inverted index if not present
                if ngram not in self.inverted_index:
                    self.inverted_index[ngram] = [(doc_name, frequency)]
                else:
                    posting_list = self.inverted_index[ngram]
                    posting_list.append((doc_name, frequency))

            # update the document vocabulary for this document in the map
            number_of_terms = len(text.split())
            self.document_term_count[doc_name] = number_of_terms
            self.total_number_of_terms_corpus += number_of_terms

    def corpus_frequency(self):
        corpus_term_count = dict()
        for term, postings in self.inverted_index.items():
            corpus_term_count[term] = 0
            for posting in postings:
                corpus_term_count[term] += posting[1]
        return corpus_term_count

    def get_inverted_index(self):
        return self.inverted_index

    def get_queries(self):
        with open(self.queries_file, 'r') as f:
            raw_queries = f.read().splitlines()
        for q in raw_queries:
            (q_id, query) = q.split(' ', 1)
            self.queries[q_id] = query
        return self.queries

    def get_stop_words(self):
        with open(self.STOP_WORDS_FILE, 'r') as f:
            self.stop_words = f.read().splitlines()
        return self.stop_words


def clean_text(text):
    return re.sub(r"(?!\d)[.,;](?!\d)|(?!\d|\w)[-/$](?!\d|\w)|[(){}\"#~\[\]<>=:?!@&'|*]|(?!\w):(?!\w)", '', text)


# def main():
#     p = Helper()
#     p.get_inverted_index()
#
#
# main()
