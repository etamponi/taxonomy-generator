from nltk.stem.wordnet import WordNetLemmatizer

__author__ = 'Emanuele Tamponi'


class TermProcessor(object):

    def __init__(self, min_length):
        self.min_length = min_length
        self.lemmatizer = WordNetLemmatizer()

    def filter(self, terms):
        ret = []
        for term in terms:
            term = self.transform(term)
            if term is not None:
                ret.append(term)
        return ret

    def transform(self, term):
        return self.lemmatizer.lemmatize(term, "v") if len(term) >= self.min_length else None
