from os import listdir
from os.path import isfile, join, dirname
import nltk


class Indexer:
    def __init__(self):
        self.INITIAL_DOCUMENTS_FOLDER = dirname(dirname(__file__))+"/task1/lucene_results/"
        self.START_PATH = dirname(dirname(dirname(dirname(__file__)))) + '/data/'
        self.CLEAN_CORPUS_DIR = self.START_PATH + 'clean_corpus/'
        self.index = dict()

    def generate_inverted_index(self, K):
        # fetch all file names
        files = [f for f in listdir(self.INITIAL_DOCUMENTS_FOLDER) if isfile(join(self.INITIAL_DOCUMENTS_FOLDER, f))]
        
        # iterate through the files
        for f in files:
            print('fetching first ' + str(K) + ' documents in file: ' + f + ' for creating an index')
            # fetch the query
            query = f[:-4]

            # maintain a index for the documents relevant to the query
            inverted_index = dict()
            f_obj = open(join(self.INITIAL_DOCUMENTS_FOLDER, f), 'rb')
            count = 0
            while count <= K:
                # maintain a document-wide frequency distribution map        
                freq_dist = nltk.FreqDist()
                document_name = f_obj.readline().decode('utf-8').rstrip().split()[2]
                document_name = document_name.replace('html', 'txt').lower()
                doc_id = document_name[:-4].lower()
                document_file_obj = open(self.CLEAN_CORPUS_DIR+document_name, 'rb')
                text = document_file_obj.read().decode('utf-8')
                # update the frequency distribution with the frequency distribution of ngrams in this document
                # uncomment the appropriate statement for uni-grams, bi-grams, and tri-grams
                freq_dist.update(text.split())  # for uni-grams
                for ngram, frequency in freq_dist.items():
                    # add the ngram and a posting list for this document in the inverted index if not present
                    if ngram not in inverted_index:
                        inverted_index[ngram] = [(doc_id, frequency)]
                    # if ngram already present in the inverted index update the posting list with
                    # a posting for this document
                    else:
                        posting_list = inverted_index[ngram]
                        posting_list.append((doc_id, frequency))
                count += 1
            self.index = inverted_index
            # for uni-grams
            out_put_file = open(dirname(__file__)+'/inverted_indexes/unigrams_inverted_index_for_'
                                + query + '.txt', 'w')
            # write the inverted index into the output file
            for k, v in inverted_index.items():
                out_put_file.write(str(k) + "::" + str(v) + "\n")
