from src.phase1 import Helper
from collections import OrderedDict
import math
import nltk
import os


class BM25Retriever:
    def __init__(self):
        # CONSTANTS (given in the assignment description)
        self.output_dir = 'Additional_results/'
        self.k1 = 1.2
        self.b = 0.75
        self.k2 = 100

    def average_length_of_docs(self, docs):
        sum = 0
        for v in docs.values():
            sum += v
        return sum / len(docs)

    def get_BM25_score(self, N, ni, K, fi, qfi):
        # N : total number of documents in the corpus
        # ni: total number of documents in which this term occurs
        # dl: the document length of the document under consideration
        # K : the value found for every document using formula  K = k1 * ((1 - b) + b * (dl/avdl))
        # fi: term frequency of the term under consideration in the document under consideration
        # qfi: frequency of the term in the query
        # ri = R = 0 as no relevance information is assumed
        # score = log (ri + 0.5)/(R − ri + 0.5)/(ni − ri + 0.5)/(N − ni − R + ri + 0.5)
        # * (k1 + 1)fi / K + fi
        # * (k2 + 1)qfi / k2 + qfi (source: Text book, Search Engines, information retrieval in practice)
        partial_score = math.log(1 / ((ni - 0.5) / (N - ni - 0.5)))\
                        * (self.k1 + 1) * fi * (1 / (K + fi)) * (self.k2 + 1) * qfi\
                        * (1 / (self.k2 + qfi))
        return partial_score

    def get_top_100_relevant_documents(self, inverted_index, document_term_count, query, avdl):
        # maintain a score list
        score_list = dict()

        N = len(document_term_count)
        for term, freq in nltk.FreqDist(query.split()).items():
            # for each term in the query fetch and traverse the inverted list
            if term not in inverted_index:
                continue
            inv_list = inverted_index[term]
            for posting in inv_list:
                dl = document_term_count[posting[0]]
                # calculate the value of K for this document
                K = self.k1 * ((1 - self.b) + self.b * (dl / avdl))
                # calculate the score for a document for that term
                score = self.get_BM25_score(N, len(inv_list), K, posting[1], freq)
                # update the score in the score list for every document in the inverted list
                # for the corresponding term in the query
                if posting[0] in score_list:
                    score_list[posting[0]] += score
                else:
                    score_list[posting[0]] = score
        # 100 for top-100 results only
        return OrderedDict(
            sorted(score_list.items(), key=lambda item: item[1], reverse=True)[:100])

    def process_query(self, query_id, query, inverted_index, avdl, document_term_count):
        # fetch top relevant results
        results = self.get_top_100_relevant_documents(inverted_index, document_term_count, query, avdl)
        # write the results to a file
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        f_obj = open(self.output_dir + str(query_id) + '.txt', 'w', encoding='utf-8')
        rank = 1
        for doc_id, score in results.items():
            doc_name = doc_id.upper() + '.html'
            f_obj.write(str(query_id) + " Q0 " + doc_name + " " + str(rank) + " " + str(score) + " BM25" + '\n')
            rank += 1
        f_obj.close()


def main():
    expanded_queries_file = os.path.dirname(__file__) + "/expanded_queries.txt"

    h = Helper.Helper()
    # generate index and the vocab counts
    inverted_index = h.get_inverted_index()
    document_term_count = h.document_term_count
    queries = dict()
    with open(expanded_queries_file, 'r') as f:
        raw_queries = f.read().splitlines()
    for q in raw_queries:
        (q_id, query) = q.split(' ', 1)
        queries[int(q_id)] = query

    bm25 = BM25Retriever()
    # find the average length of docs in the index across the corpus.
    avdl = bm25.average_length_of_docs(document_term_count)
    # read queries
    for query_id, query in queries.items():
        bm25.process_query(query_id, query, inverted_index, avdl, document_term_count)


main()
