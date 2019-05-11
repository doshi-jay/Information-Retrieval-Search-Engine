import math
from collections import OrderedDict
from src.extracredit import Helper


class KLRetriever:

    def __init__(self):
        self.output_folder = 'top100/'
        self.helper = Helper.Helper()
        # choose a high value of lambda as the queries are longer
        self.lambda_value = 0.75
        self.stop_words = self.helper.get_stop_words()
        self.inverted_index = self.helper.get_inverted_index()
        self.term_frequency_in_corpus = self.helper.corpus_frequency()
        self.score_list = OrderedDict()

    def retrieve_scores(self, query):
        score_list = dict()
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
        self.score_list = OrderedDict(sorted(score_list.items(), key=lambda item: item[1], reverse=True)[:50])

    def calculate_PwR(self):
        pwr = dict()
        # pwd = dict()
        sum_pwr = 0
        for word, posting_list in self.inverted_index.items():
            if word in self.stop_words:
                continue
            sum_docs = 0
            for doc_id, score in self.score_list.items():
                for posting in posting_list:
                    if doc_id.lower() == posting[0]:
                        # pwd[(word, doc_id)] = float(posting[1]) / float(self.helper.document_term_count[doc_id])
                        sum_docs += (float(posting[1]) / float(self.helper.document_term_count[doc_id])) \
                                    * self.score_list.get(doc_id)
                    # else:
                        # pwd[(word, doc_id)] = 0.0
            pwr[word] = sum_docs
            sum_pwr += sum_docs
        for word in pwr.keys():
            pwr[word] = float(pwr[word])/float(sum_pwr)
        return pwr

    def calculate_PwD(self, query_terms):
        pwd = dict()
        documents = self.fetch_all_docs_for_terms(query_terms)
        for word, posting_list in self.inverted_index.items():
            if word in self.stop_words:
                continue
            for doc_id in documents:
                for posting in posting_list:
                    if doc_id.lower() == posting[0]:
                        x = self.helper.document_term_count[doc_id]
                        pwd[(word, doc_id)] = float(posting[1]) / float(x)
                    else:
                        pwd[(word, doc_id)] = 0.0
        return pwd

    def KL_divergence_score(self, query_terms):
        pwr = self.calculate_PwR()
        sorted_pwr = OrderedDict(sorted(pwr.items(), key=lambda item: item[1], reverse=True)[:20])
        pwd = self.calculate_PwD(query_terms)
        kl_scores = dict()
        documents = self.fetch_all_docs_for_terms(query_terms)
        for doc_id in documents:
            for word in sorted_pwr.keys():
                if pwd[(word, doc_id)] == 0.0:
                    kl_scores[doc_id] = 0.0
                else:
                    if doc_id in kl_scores.keys():
                        kl_scores[doc_id] += pwr[word] * math.log(pwd[(word, doc_id)])
                    else:
                        kl_scores[doc_id] = pwr[word] * math.log(pwd[(word, doc_id)])
        return OrderedDict(sorted(kl_scores.items(), key=lambda item: item[1], reverse=True)[:100])

    def fetch_all_docs_for_terms(self, query_terms):
        #   maintain a list of documents that contain at least one of the query terms.
        #   NOTE: we consider only these documents as the documents which contain none of the query terms will all have
        #   the same score which is equal to the left over probabilities of the query terms occurring in the corpus
        documents = set()
        for term in query_terms:
            if term in self.inverted_index.keys():
                posting_list = self.inverted_index[term]
                for posting in posting_list:
                    doc_id = posting[0]
                    documents.add(doc_id)

        return list(documents)

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
        score = lm_probability + cm_probability
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
            if int(query_id) > 1:
                break
            self.retrieve_scores(query)
            kl_scores = self.KL_divergence_score(query.split())
            print(kl_scores)


def main():
    j = KLRetriever()
    j.start()


main()
