from collections import OrderedDict
from nltk.corpus import stopwords
from os import listdir
from os.path import isfile, join, dirname
from src.phase1.task2 import inverted_indexer
from src.phase1 import Helper

OUTPUT_FILE = dirname(__file__) + "/Query Expansion/terms_for_expansion.txt"

INITIAL_INDEX_FOLDER = dirname(__file__) + "/inverted_indexes/"


class QueryExpander:

    def __init__(self):
        self.K = 10
        self.N = 8

    def get_inverted_index_from_file(self, file):
        f = open(file, 'r')
        inverted_index = dict()
        for line in f:
            (term, posting_list) = line.split('::')
            inverted_index[term] = eval(posting_list)
        return inverted_index

    def generate_term_frequency_table(self, inverted_index):
        term_frequency_table = dict()
        for ngram, posting_list in inverted_index.items():
            term_freq = 0
            for posting in posting_list:
                term_freq += posting[1]
            term_frequency_table[ngram] = term_freq
        return OrderedDict(sorted(term_frequency_table.items(), key=lambda item: item[1], reverse=True))

    def generate_document_frequency_table(self, inverted_index):
        document_frequency_table = dict()
        for ngram, posting_list in inverted_index.items():
            doc_ids = set()
            for posting in posting_list:
                doc_ids.add(posting[0])
            document_frequency_table[ngram] = [doc_ids, len(posting_list)]
        return OrderedDict(sorted(document_frequency_table.items(), key=lambda item: item[0]))

    def generate_corpus_statistics(self, f):
        inverted_index = self.get_inverted_index_from_file(f)
        query = f[:-4].split('_')[-1]
        # fetch query from queries.txt here
        h = Helper.Helper()
        queries = h.get_queries()
        query_text = queries[int(query)]
        document_frequency_table = self.generate_document_frequency_table(inverted_index)
        terms = self.find_candidate_expansion_terms(query_text, document_frequency_table)
        f_obj = open(OUTPUT_FILE, 'a')
        f_obj.write(str(query) + ' ' + query_text + " " + ' '.join(list(terms.keys())[:self.N])+ "\n")
        f_obj.close()

    def find_candidate_expansion_terms(self, query, doc_freq_table):
        print('finding expansion terms for query: ' + query)
        # maintain a dictionary to store the dice's coefficient for the terms in the index with the query terms
        dice_coefficients = dict()
        for q_term in query.lower().split():
            if q_term not in doc_freq_table:
                continue
            q_docs = doc_freq_table[q_term][0]
            for term, docs in doc_freq_table.items():
                if term in stopwords.words('english') or term in query.lower().split() or len(term) < 4:
                    continue
                # accumulate the dice's coefficients for the terms in the corpus for every term in the query
                if term not in dice_coefficients:
                    dice_coefficients[term] = 2*len(q_docs.intersection(docs[0])) / \
                                              (len(docs) + len(q_docs)) / len(query.split())
                else:
                    dice_coefficients[term] += 2*len(q_docs.intersection(docs[0])) / \
                                               (len(docs) + len(q_docs)) / len(query.split())
        return OrderedDict(sorted(dice_coefficients.items(), key=lambda item: item[1], reverse=True))


def main():
    # generate inverted index over all the documents in a file for a query   
    indexer = inverted_indexer.Indexer()
    query_expander = QueryExpander()
    indexer.generate_inverted_index(query_expander.K)
    # iterate through all files to find the candidate expansion terms for the corresponding query
    files = [f for f in listdir(INITIAL_INDEX_FOLDER) if isfile(join(INITIAL_INDEX_FOLDER, f))]
    for f in files:
        f = join(INITIAL_INDEX_FOLDER, f)
        query_expander.generate_corpus_statistics(f)


main()
