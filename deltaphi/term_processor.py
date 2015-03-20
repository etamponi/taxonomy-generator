from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

__author__ = 'Emanuele Tamponi'


class TermProcessor(object):

    def __init__(self, min_length):
        self.min_length = min_length
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = stopwords.words("english")

    def filter(self, terms):
        ret = []
        for term in terms:
            term = self.transform(term)
            if term is not None:
                ret.append(term)
        return ret

    def transform(self, term):
        term = self.lemmatizer.lemmatize(term, "v")
        return term if self._should_include(term) else None

    def _should_include(self, term):
        return len(term) >= self.min_length and term not in self.stopwords
