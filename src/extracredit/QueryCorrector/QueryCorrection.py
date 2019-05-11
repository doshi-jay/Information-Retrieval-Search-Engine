# Referred https://stackoverflow.com/questions/43410332/how-to-modify-peter-norvig-spell-checker-to-get-more-number-of-suggestions-per-w
# code for using edit distance for suggesting correct query terms.
# Changed the utilized dataset in the code to use the unigram index for the CACM dataset
# instead of the English vocabulary.
# This affects the suggestions to be very dependant on the given CACM dataset.

from os.path import dirname


class QueryCorrection:
    def __init__(self, input_query):
        self.index_file = (dirname(dirname(dirname(dirname(__file__))))) + '/data/unigrams_inverted_index.txt'
        self.words = dict()
        self.get_words()
        self.query = input_query
        self.suggestions = self.get_candidates(self.query.split(' '))

    def get_words(self):
        with open(self.index_file, 'r', encoding="utf8", errors='ignore') as f:
            lines = f.read().splitlines()
        f.close()
        for line in lines:
            (term, posting_list) = line.split('::')
            pl = eval(posting_list)
            count = 0
            for posting in pl:
                count += posting[1]
            self.words[term] = count

    def get_suggestions(self):
        return self.suggestions

    def get_candidates(self, query_terms):
        all_candidates = []
        max_count = 1
        for qt in query_terms:
            if qt in self.words.keys():
                all_candidates.append(qt)
                continue
            c = list(self.candidates(qt))[:6]
            all_candidates.append(c)
            max_count = max(max_count, len(c))
        return self.format_candidates(all_candidates, max_count)

    @staticmethod
    def format_candidates(all_candidates, max_count):
        rep_candidates = []
        for c in all_candidates:
            if isinstance(c, str):
                rep_candidates.append([c] * max_count)
            elif isinstance(c, list):
                c.extend([c[0]] * (max_count - len(c)))
                rep_candidates.append(c)
        candidates = []
        for i in range(max_count):
            suggestion = ''
            for c in rep_candidates:
                    suggestion += c[i] + ' '
            candidates.append(suggestion)
        return candidates

    def get_probability(self, word):
        return float(self.words[word]) / float(sum(self.words.values()))

    def correction(self, word):
        return max(self.candidates(word), key=self.get_probability)

    def candidates(self, word):
        return self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word]

    def known(self, given_words):
        return set(w for w in given_words if w in self.words)

    @staticmethod
    def edits1(word):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        split = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        no_of_deletes = [L + R[1:] for L, R in split if R]
        no_of_transposes = [L + R[1] + R[0] + R[2:] for L, R in split if len(R) > 1]
        no_of_replaces = [L + c + R[1:] for L, R in split if R for c in alphabet]
        no_of_inserts = [L + c + R for L, R in split for c in alphabet]
        return set(no_of_deletes + no_of_transposes + no_of_replaces + no_of_inserts)

    def edits2(self, word):
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))


def main():
    while True:
        input_query = input("Enter the query you want to correct: ")
        if input_query == 'q':
            break
        qc = QueryCorrection(input_query)
        suggestions = qc.get_suggestions()
        if len(suggestions) > 0:
            print('The corrected queries are:')
            for s in suggestions:
                print(s)
        else:
            print('Your query has no incorrect words, try another query.')


main()
