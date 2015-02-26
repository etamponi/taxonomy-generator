from collections import Counter

__author__ = 'Emanuele Tamponi'


class InvalidParameters(Exception):
    pass


class CategoryInfo(object):

    def __init__(self, category, n_observations, predictors, frequencies):
        """
        Create a Category Info starting from the fields in a Doc Set row
        :param category: The name of the category
        :param n_observations: The number of documents in the category
        :param predictors: The names of the predictors that are "on" for the category (e.g.: terms in the documents)
        :param frequencies: How many times each predictor is "on" in the category
        """
        try:
            self.category = category
            self.n_observations = int(n_observations)
            predictors = predictors.split(" ")
            frequencies = map(int, frequencies.split(" "))
            if len(predictors) != len(frequencies):
                raise InvalidParameters()
            self.predictors = Counter(dict(zip(predictors, frequencies)))
            self.children = {}
        except ValueError:
            raise InvalidParameters()

    @classmethod
    def merge(cls, *infos):
        categories = sorted(info.category for info in infos)
        merged_category = "(" + "+".join(categories) + ")"
        merged_n_observations = sum(info.n_observations for info in infos)
        merged_predictors = sum((info.predictors for info in infos), Counter())
        merged_predictor_keys = " ".join(merged_predictors.keys())
        merged_predictor_values = " ".join(map(str, merged_predictors.values()))
        ci = CategoryInfo(merged_category, merged_n_observations, merged_predictor_keys, merged_predictor_values)
        ci.children = set(infos)
        return ci