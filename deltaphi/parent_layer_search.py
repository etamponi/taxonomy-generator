import itertools

__author__ = 'Emanuele Tamponi'


class ParentLayerSearch(object):

    def perform(self, layer):
        pass


class GreedyMergeSearch(ParentLayerSearch):

    def __init__(self, scorer):
        self.scorer = scorer

    def perform(self, layer):
        if all(len(group) > 1 for group in layer.groups):
            return [layer.build_parent()]
        best_score = 0
        best_pair = None
        for a, b in itertools.combinations(layer.groups, 2):
            score = self.scorer.evaluate(a + b)
            if score > best_score:
                best_score = score
                best_pair = (a, b)
        if best_pair is None:
            return [layer.build_parent()]
        else:
            return self.perform(layer.merge_groups(best_pair[0], best_pair[1]))
