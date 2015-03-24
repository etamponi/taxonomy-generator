import unicodedata

from deltaphi.category_info import RawCategoryInfo


__author__ = 'Emanuele Tamponi'


class Filter(object):

    def __init__(self, min_length=1, normalization="NFKC", lemmatizer=None, stopwords=None):
        self.min_length = min_length
        self.normalization = normalization
        self.lemmatizer = lemmatizer
        self.stopwords = stopwords if stopwords is not None else {}

    def apply(self, rci):
        processed = RawCategoryInfo(rci.category, rci.documents, {})
        for term, frequency in rci.term_frequencies.iteritems():
            term = self._transform(term)
            if term is not None:
                processed.term_frequencies[term] += frequency
        return processed

    def _transform(self, term):
        term = self._normalize(term)
        if self.lemmatizer is not None:
            term = self.lemmatizer.lemmatize(term, "v")
        return term if self._should_include(term) else None

    def _should_include(self, term):
        return len(term) >= self.min_length and term not in self.stopwords

    def _normalize(self, term):
        term = term if isinstance(term, unicode) else unicode(term, "utf-8")
        return unicodedata.normalize(self.normalization, term)
