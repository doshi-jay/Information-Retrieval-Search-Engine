from os.path import dirname, join
from collections import defaultdict
import re
import os
import nltk


class StemmedParser:
    def __init__(self):
        self.start_path = dirname(dirname(dirname(dirname(__file__)))) + '/data/'
        self.stemmed_file = self.start_path + 'cacm_stem.txt'
        self.stemmed_corpus_dir = self.start_path + 'stemmed_corpus/'
        self.inverted_index = dict()

    def parse_stemmed_file(self):
        with open(self.stemmed_file, 'r') as f:
            stemmed_data = f.read().split('#')
        f.close()
        stemmed_data = stemmed_data[1:]

        for file_data in stemmed_data:
            lines = file_data.split()
            file_number = lines.pop(0).strip()
            words = []

            for word in lines:
                if word == "pm" or word == "am":
                    words.append(word)
                    break
                word = re.sub(r"(?!\d)[.,;](?!\d)|(?!\d|\w)[-/$](?!\d|\w)|[(){}\"#~\[\]<>=?!@&'|*]|(?!\w):(?!\w)",
                              '', word)
                words.append(word)
            filtered_text = " ".join(words)
            file_number = file_number.zfill(4)
            file_name = self.stemmed_corpus_dir + 'cacm-' + file_number + '.txt'
            output_file = open(file_name, 'w')
            output_file.write(filtered_text)
            output_file.close()

    def run(self):
        self.parse_stemmed_file()


class Helper:

    def __init__(self):
        self.start_path = dirname(dirname(dirname(dirname(__file__)))) + '/data/'
        self.clean_corpus_dir = self.start_path + 'stemmed_corpus/'
        self.raw_queries_file = self.start_path + 'cacm_stem.query.txt'
        self.parsed_queries_file = self.start_path + 'queries.txt'

        self.queries = dict()
        # maintain a global inverted index
        self.inverted_index = dict()
        # maintain a map for document -> vocabulary count
        self.document_term_count = dict()
        self.parse_queries()
        self.generate_inverted_index()

    def generate_inverted_index(self):
        # iterate through the files
        for f in os.listdir(self.clean_corpus_dir):
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

    def parse_queries(self):
        queries = defaultdict()
        with open(self.raw_queries_file, 'r') as f:
            lines = f.readlines()
            query_id = 1
            for line in lines:
                # line_list = line.replace("\n", '').split()
                # query = ' '.join(line_list)
                queries[query_id] = line.rstrip()
                query_id += 1
        self.queries = queries

    def get_inverted_index(self):
        return self.inverted_index

    def get_queries(self):
        return self.queries
