import heapq
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
            print "Merged", best_pair
            return self.perform(layer.merge_groups(best_pair[0], best_pair[1]))


class LayerGreedyMergeSearch(ParentLayerSearch):

    def __init__(self, layer_score):
        self.layer_score = layer_score

    def perform(self, layer):
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


class GreedyQueueMergeSearch(ParentLayerSearch):

    def __init__(self, layer_score, size, iterations):
        self.layer_score = layer_score
        self.size = size
        self.iterations = iterations

    def perform(self, layer):
        candidates = [(0, layer)]
        for i in range(self.iterations):
            print "Running iteration", i+1
            heap = []
            for score, layer in candidates:
                for a, b in itertools.combinations(layer.groups, 2):
                    if len(a) + len(b) > 2:
                        continue
                    new_layer = layer.merge_groups(a, b)
                    new_score = self.layer_score.evaluate(new_layer.build_parent())
                    if (new_score, new_layer) not in heap:
                        heapq.heappush(heap, (new_score, new_layer))
            candidates += heap
            candidates = sorted(candidates)[-self.size:]
        for score, layer in candidates:
            print score, layer
        return [layer.build_parent() for _, layer in candidates]
