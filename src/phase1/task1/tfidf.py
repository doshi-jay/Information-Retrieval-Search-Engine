from src.phase1 import Helper
from math import log
import collections
import os


class TFIDFRetriever:

    def __init__(self, inverted_index, document_term_count, queries):
        self.output_dir = 'TF_IDF_results/'
        self.inverted_index = inverted_index
        self.document_term_count = document_term_count
        self.queries = queries

    def get_tf_idf_score(self, tf, df, D, N):
        idf = log(N/df+1) + 1
        tf = tf/D
        return tf * idf

    def get_score_for_query(self, query):
        final_score = dict()
        terms = query.split()
        for term in terms:
            if term in self.inverted_index:
                for doc in self.inverted_index[term]:
                    tf = doc[1]
                    df = len(self.inverted_index[term])
                    D = self.document_term_count[doc[0]]
                    N = len(self.document_term_count)
                    score = self.get_tf_idf_score(tf, df, D, N)
                    final_score[doc[0]] = score if doc[0] not in final_score.keys() else final_score[doc[0]] + score
        return final_score

    def run(self):
        for query_id, query in self.queries.items():
            # the variable c denotes rank
            raw_scores = self.get_score_for_query(query)
            ordered_scores = collections.OrderedDict(
                sorted(raw_scores.items(), key=lambda item: item[1], reverse=True)[:100])
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            with open(self.output_dir + str(query_id) + '.txt', 'w') as output:
                count = 1
                for doc in ordered_scores:
                    doc_name = doc.upper() + '.html'
                    output.write(str(query_id) + " Q0 " + doc_name + " " + str(count)
                                 + " " + str(ordered_scores[doc]) + " TF_IDF\n")
                    count += 1
            output.close()


def main():
    h = Helper.Helper()

    inverted_index = h.get_inverted_index()
    document_term_count = h.document_term_count
    queries = h.get_queries()

    tfidf = TFIDFRetriever(inverted_index, document_term_count, queries)
    tfidf.run()


main()
