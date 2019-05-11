from os.path import dirname
import re


class Helper:

    def __init__(self):
        self.start_path = dirname(dirname(dirname(__file__))) + '/data/'
        self.QUERIES_FILE = self.start_path + 'queries.txt'
        self.STOP_WORDS_FILE = self.start_path + 'common_words.txt'
        self.queries = dict()
        self.stop_words = list()

    def get_queries(self):
        with open(self.QUERIES_FILE, 'r') as f:
            raw_queries = f.read().splitlines()
        for q in raw_queries:
            (q_id, query) = q.split(' ', 1)
            self.queries[q_id] = query
        return self.queries

    def get_stop_words(self):
        with open(self.STOP_WORDS_FILE, 'r') as f:
            self.stop_words = f.read().splitlines()
        return self.stop_words

    @staticmethod
    def clean_text(text):
        return re.sub(r"(?!\d)[.,;](?!\d)|(?!\d|\w)[-/$](?!\d|\w)|[(){}\"#~\[\]<>=:?!@&'|*]|(?!\w):(?!\w)", '', text)
