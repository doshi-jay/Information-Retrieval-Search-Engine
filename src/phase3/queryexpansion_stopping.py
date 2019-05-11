from collections import OrderedDict
from os import listdir
from os.path import isfile, join, dirname
from src.phase3 import inverted_indexer


class InvertedIndexHelper:
    def __init__(self):
        self.START_PATH = dirname(dirname(dirname(__file__))) + '/data/'
        self.QUERIES_FILE = self.START_PATH + 'queries.txt'

        self.queries = dict()
        self.inverted_index = dict()
        self.term_frequency_table = dict()
        self.doc_frequency_table = dict()

    def get_inverted_index_from_file(self, file):
        f = open(file, 'r')
        inverted_index = dict()
        for line in f:
            (term, posting_list) = line.split('::')
            inverted_index[term] = eval(posting_list)
        self.inverted_index = inverted_index
        return inverted_index

    def generate_term_frequency_table(self, inverted_index):
        raw_tf_table = dict()
        for ngram, posting_list in inverted_index.items():
            term_freq = 0
            for posting in posting_list:
                term_freq += posting[1]
            raw_tf_table[ngram] = term_freq
        self.term_frequency_table = OrderedDict(sorted(raw_tf_table.items(),
                                                       key=lambda item: item[1], reverse=True))
        return self.term_frequency_table

    def generate_document_frequency_table(self, inverted_index):
        document_frequency_table = dict()
        for ngram, posting_list in inverted_index.items():
            doc_ids = set()
            for posting in posting_list:
                doc_ids.add(posting[0])
            document_frequency_table[ngram] = [doc_ids, len(posting_list)]
        self.doc_frequency_table = OrderedDict(sorted(document_frequency_table.items(),
                                                      key=lambda item: item[0]))
        return self.doc_frequency_table

    def get_queries(self):
        with open(self.QUERIES_FILE, 'r') as f:
            raw_queries = f.read().splitlines()
        for q in raw_queries:
            (q_id, query) = q.split(' ', 1)
            self.queries[q_id] = query
        return self.queries


class QueryExpander:

    def __init__(self):
        self.output_file = dirname(__file__) + "/expanded_queries.txt"

        self.K = 10
        self.N = 8
        self.index_helper = InvertedIndexHelper()
        self.queries = self.index_helper.get_queries()

    def generate_corpus_statistics(self, f):
        inverted_index = self.index_helper.get_inverted_index_from_file(f)
        query_id = f[:-4].split('_')[-1]

        query = self.queries.get(query_id)
        document_frequency_table = self.index_helper.generate_document_frequency_table(inverted_index)
        terms = self.find_candidate_expansion_terms(query, document_frequency_table)
        with open(self.output_file, 'a') as f_obj:
            f_obj.write(query_id + ' ' + query + ' ' + ' '.join(list(terms.keys())[:self.N]) + '\n')
        f_obj.close()

    def find_candidate_expansion_terms(self, query, doc_freq_table):
        # maintain a dictionary to store the dice's coefficient for the terms in the index with the query terms
        dice_coefficients = dict()
        for q_term in query.lower().split():
            if q_term not in doc_freq_table:
                continue
            q_docs = doc_freq_table[q_term][0]
            for term, docs in doc_freq_table.items():
                if term in query.lower().split():
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
    temp_index_dir = dirname(__file__) + "/inverted_indexes/"

    indexer = inverted_indexer.Indexer()
    query_expander = QueryExpander()
    indexer.generate_inverted_index(query_expander.K)
    # iterate through all files to find the candidate expansion terms for the corresponding query
    files = [f for f in listdir(temp_index_dir) if isfile(join(temp_index_dir, f))]
    for f in files:
        f = join(temp_index_dir, f)
        query_expander.generate_corpus_statistics(f)


main()
