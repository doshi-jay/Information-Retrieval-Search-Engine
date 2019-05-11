import math
from src.phase1 import Helper


class JMQLMRetriever:

    def __init__(self):
        self.output_folder = 'JM_QLM_results/'
        self.helper = Helper.Helper()
        # choose a high value of lambda as the queries are longer
        self.lambda_value = 0.75
        self.inverted_index = self.helper.get_inverted_index()
        self.max_docs = 100
        self.term_frequency_in_corpus = self.helper.corpus_frequency()

    def retrieve_scores(self, query, query_id):
        score_list= dict()
        query = Helper.clean_text(query)
        query_terms = query.split()
        documents = self.fetch_all_docs_for_terms(query_terms)
        for term in query_terms:
            if term in self.inverted_index.keys():
                for doc_id in documents:
                    if doc_id not in score_list:
                        score_list[doc_id] = self.get_query_likelihood_jm_score(doc_id, term)
                    else:
                        score_list[doc_id] += self.get_query_likelihood_jm_score(doc_id, term)
        scores = sorted(score_list.items(), key=lambda item: item[1])
        self.write_results_to_file(query_id, scores)

    def fetch_all_docs_for_terms(self, query_terms):
        #   maintain a list of documents that contain at least one of the query terms.
        #   NOTE: we consider only these documents as the documents which contain none of the query terms will all have
        #   the same score which is equal to the left over probabilities of the query terms occurring in the corpus
        documents = []
        for term in query_terms:
            if term in self.inverted_index.keys():
                posting_list = self.inverted_index[term]
                for posting in posting_list:
                    doc_id = posting[0]
                    documents.append(doc_id)

        return documents

    def write_results_to_file(self, query_id, scored_docs):
        file_name = self.output_folder + str(query_id) + '.txt'
        with open(file_name, 'w') as f:
            rank = 1
            for doc in scored_docs:
                doc_name = doc[0].upper() + '.html'
                if rank > self.max_docs:
                    break
                f.write(str(query_id) + " Q0 " + doc_name + " " + str(rank) + " " + str(doc[1]) +
                        " JM_Smoothed_Query_Likelihood_Model\n")
                rank += 1

    def get_query_likelihood_jm_score(self, doc_id, term):
        # fqi,D = frequency of the term in the document
        # |D| = total term count in document D (length_of_document)
        # Cqi = frequency of the terms in the Collection C (corpus)
        # |C| = the total number of word occurrences in the collection (length_of_collection)
        # p(qi | D) = (1 − λ)(fqi,D / | D |) + λ * (cqi / | C |) # adopted from the text book Search Engines:
        # Information retrieval in practice
        fqid = self.get_frequency_of_term_in_doc(term, doc_id)
        length_of_document = float(self.helper.document_term_count[doc_id])
        cqi = self.term_frequency_in_corpus[term] * 1.0
        length_of_collection = float(self.helper.total_number_of_terms_corpus)
        # probability of seeing the term in the document
        lm_probability = ((1 - self.lambda_value) * (fqid / length_of_document))
        # probability of not seeing the term in the document
        cm_probability = (self.lambda_value * (cqi / length_of_collection))
        score = math.log(lm_probability + cm_probability)
        return score

    def get_frequency_of_term_in_doc(self, term, doc_id):
        posting_list = self.inverted_index[term]
        for posting in posting_list:
            if doc_id == posting[0]:
                return float(posting[1])
        # if term not present in the document
        return 0.0

    def start(self):
        queries = self.helper.get_queries()
        for query_id, query in queries.items():
            self.retrieve_scores(query, query_id)


def main():
    j = JMQLMRetriever()
    j.start()


main()
