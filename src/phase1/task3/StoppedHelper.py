from os.path import join, dirname
import re
import os
import nltk


class StoppedHelper:

    def __init__(self):
        self.start_path = dirname(dirname(dirname(dirname(__file__)))) + '/data/'
        self.clean_corpus_dir = self.start_path + 'clean_corpus/'
        self.term_count_file = self.start_path + 'terms_in_document.txt'
        self.QUERIES_FILE = self.start_path + 'queries.txt'
        self.STOP_WORDS = self.start_path + 'common_words.txt'

        self.queries = dict()
        self.get_queries()
        self.stop_words = self.read_stop_words()
        self.total_number_of_terms_corpus = 0
        # maintain a global inverted index
        self.inverted_index = dict()
        # maintain a map for document -> vocabulary count
        self.document_term_count = dict()
        self.generate_inverted_index()

    def read_stop_words(self):
        with open(self.STOP_WORDS, 'r') as f:
            stop_list = f.read().splitlines()
        f.close()
        return stop_list

    def generate_inverted_index(self):
        # iterate through the files
        for f in os.listdir(self.clean_corpus_dir):
            doc_name = f[:-4]

            with open(join(self.clean_corpus_dir, f), 'rb') as clean_file:
                file_data = clean_file.read().decode('utf-8')
            clean_file.close()

            text = [word for word in file_data.split() if word not in self.stop_words]
            # maintain a document-wide frequency distribution map
            freq_dist = nltk.FreqDist()
            # update the frequency distribution with the frequency distribution of unigrams in this document
            freq_dist.update(text)  # for uni-grams
            for ngram, frequency in freq_dist.items():
                # add the ngram and a posting list for this document in the inverted index if not present
                if ngram not in self.inverted_index:
                    self.inverted_index[ngram] = [(doc_name, frequency)]
                else:
                    posting_list = self.inverted_index[ngram]
                    posting_list.append((doc_name, frequency))

            # update the document vocabulary for this document in the map
            number_of_terms = len(text)
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
        with open(self.QUERIES_FILE, 'r') as f:
            raw_queries = f.read().splitlines()
        for q in raw_queries:
            (q_id, query) = q.split(' ', 1)
            self.queries[q_id] = query
        return self.queries


def clean_text(text):
    return re.sub(r"(?!\d)[.,;](?!\d)|(?!\d|\w)[-/$](?!\d|\w)|[(){}\"#~\[\]<>=:?!@&'|*]|(?!\w):(?!\w)", '', text)


# def main():
#     sh = StoppedHelper()
#     print(sh.queries)
#
#
# main()
