import itertools

__author__ = 'Emanuele Tamponi'


class ParentLayerSearch(object):

    def perform(self, layer):
        pass


class GreedyMergeSearch(ParentLayerSearch):

    def __init__(self, group_score):
        self.group_score = group_score

    def perform(self, layer):
        if all(len(group) > 1 for group in layer.groups):
            return [layer.build_parent()]
        best_score = 0
        best_pair = None
        for a, b in itertools.combinations(layer.groups, 2):
            score = self.group_score.evaluate(a + b)
            if score > best_score:
                best_score = score
                best_pair = (a, b)
        if best_pair is None:
            return [layer.build_parent()]
        else:
            return self.perform(layer.merge_groups(best_pair[0], best_pair[1]))


class LayerGreedyMergeSearch(ParentLayerSearch):

    def __init__(self, layer_score):
        self.layer_score = layer_score

    def perform(self, layer):
        print "Evaluating:", layer
        if all(len(group) > 1 for group in layer.groups):
            return [layer.build_parent()]
        best_score = 0
        best_layer = None
        for a, b in itertools.combinations(layer.groups, 2):
            new_layer = layer.merge_groups(a, b)
            score = self.layer_score.evaluate(new_layer.build_parent())
            if score > best_score:
                best_score = score
                best_layer = new_layer
        if best_layer is None:
            return [layer.build_parent()]
        else:
            return self.perform(best_layer)
