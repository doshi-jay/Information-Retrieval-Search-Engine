from src.phase2.Helper import Helper
from os.path import dirname
from bs4 import BeautifulSoup
from nltk import sent_tokenize


class SnippetGenerator:
    def __init__(self):
        self.results_dir = dirname(dirname(dirname(__file__))) + '/src/phase1/task1/lucene_results/'
        self.output_dir = 'snippet_results/'
        self.helper = Helper()

    def read_top_results(self, query_id):
        file_sentences = dict()
        with open(self.results_dir + str(query_id) + '.txt', 'r') as f:
            top_results = f.read().splitlines()
        f.close()
        for file in top_results:
            line = file.split()
            filename = line[2].lower()

            with open('../../data/cacm/' + filename, 'r') as f:
                # file_text = f.read()
                bs_object = BeautifulSoup(f.read(), "html.parser")
                content_block = bs_object.find('pre')
                file_text = content_block.get_text().lower()
            f.close()

            # retrieve the content from the pre tags in the files
            words = []
            for word in file_text.split():
                if word == "pm" or word == "am":
                    words.append(word)
                    break
                words.append(word)
            words = [word for word in words if word not in self.helper.get_stop_words()]
            sentences = sent_tokenize(' '.join(words))
            file_sentences[filename] = sentences
        return file_sentences

    def get_snippets_for_query(self, query_id, query_terms):
        text_from_results = self.read_top_results(query_id)
        file_snippets = dict()
        for doc_id, doc_data in text_from_results.items():
            file_snippets[doc_id] = self.get_top_sentence(doc_data, query_terms)
        return file_snippets

    def get_top_sentence(self, doc_data, query_terms):
        max_score = 0
        best_sentence = ''
        for sentence in doc_data:
            score = self.get_score_for_sentence(sentence, query_terms)
            if score > max_score:
                max_score = score
                best_sentence = sentence
        if best_sentence is '':
            return doc_data[0]
        return self.helper.clean_text(best_sentence)

    def get_score_for_sentence(self, sentence, query_terms):
        clean_sentence = self.helper.clean_text(sentence)
        words = clean_sentence.split(' ')
        text_spans = []
        ts = []
        seen = False
        count = 0
        for w in words:
            if w in query_terms:
                seen = True
                ts.append(w)
            else:
                if seen:
                    if count <= 4:
                        ts.append(w)
                        count += 1
                    else:
                        text_spans.append(ts)
                        count = 0
                        seen = False
                        ts = []
        return self.get_max_score_for_ts(text_spans, query_terms)

    @staticmethod
    def get_max_score_for_ts(text_spans, query_terms):
        max_score = 0
        for ts in text_spans:
            count = 0
            for word in ts:
                if word in query_terms:
                    count += 1
            score = float(count * count) / (len(ts))
            max_score = max(score, max_score)
        return max_score

    @staticmethod
    def embolden(snippet, query_terms):
        output = []
        for word in snippet.split():
            if word in query_terms:
                output.append('<b>' + word + '</b>')
            else:
                output.append(word)
        return ' '.join(output)

    def write_snippets_for_query(self, query_id, query_terms):
        snippets = self.get_snippets_for_query(query_id, query_terms)
        filename = self.output_dir + query_id + '.txt'
        for file, snippet in snippets.items():
            with open(filename, 'a') as f:
                f.write(file + ': ' + self.embolden(snippet, query_terms) + '\n')
            f.close()


def main():
    helper = Helper()
    queries = helper.get_queries()
    for query_id, query in queries.items():
        query_terms = query.split()
        sg = SnippetGenerator()
        sg.write_snippets_for_query(query_id, query_terms)


main()
