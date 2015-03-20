from nltk.stem.wordnet import WordNetLemmatizer

__author__ = 'Emanuele Tamponi'


class TermProcessor(object):

    def __init__(self, min_length):
        self.min_length = min_length
        self.lemmatizer = WordNetLemmatizer()

    def filter(self, terms):
        return [self.lemmatizer.lemmatize(term, "v") for term in terms if len(term) >= self.min_length]
