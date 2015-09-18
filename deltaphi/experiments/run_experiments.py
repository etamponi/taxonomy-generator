import cPickle
import csv
import sys

from deltaphi.category_info import CategoryLayer
from deltaphi.experiments.assessment import Taxonomy, SearchTaxonomy, TaxonomyScore
from deltaphi.experiments.dataset_definitions import DATASET_DEFINITIONS
from deltaphi.metrics import LookAhead, CharacteristicTerms, DiscriminantTerms, Cohesion, Separability
from deltaphi.parent_layer_search import LayerGreedyMergeSearch
from deltaphi.raw_filter import RawFilter
from deltaphi.sources import CSVRawSource, CategoryInfoSource

__author__ = 'Emanuele'


DATASET_DIR = "datasets"
RESULT_DIR = "results"

CHARACTERISTIC_AREA = Cohesion.DEFAULT_AREA
DISCRIMINANT_AREA = Separability.DEFAULT_AREA

SEARCHER = SearchTaxonomy(
    parent_layer_search=LayerGreedyMergeSearch(
        layer_score=LookAhead(
            characteristic_terms=CharacteristicTerms(
                characteristic_area=CHARACTERISTIC_AREA
            ),
            discriminant_terms=DiscriminantTerms(
                discriminant_area=DISCRIMINANT_AREA
            )
        )
    )
)
SEARCHER_NAME = "default"


def main():
    csv.field_size_limit(sys.maxint)
    print "Testing", SEARCHER_NAME
    for dataset_name in get_dataset_names():
        print "Running experiment:", dataset_name
        categories = get_categories(dataset_name, DATASET_DIR)
        reference, generated, score, layer_scores = run_experiment(SEARCHER, categories)
        print "Reference taxonomy:"
        print_taxonomy(reference)
        print "Generated taxonomy:"
        print_taxonomy(generated)
        print "Scores:"
        print_scores(layer_scores, score)
        save_results(SEARCHER_NAME, dataset_name, [reference, generated, score, layer_scores], RESULT_DIR)


def get_dataset_names():
    return [definition[0] for definition in DATASET_DEFINITIONS]


def get_categories(dataset_name, dataset_dir):
    file_path = "{}/{}.csv".format(dataset_dir, dataset_name)
    source = CategoryInfoSource(
        CSVRawSource(file_path),
        raw_filter=RawFilter(
            min_length=3
        )
    )
    source.open()
    return list(source.iterate())


def run_experiment(searcher, categories):
    reference = Taxonomy.build_from_category_names(categories)
    leaf_layer = CategoryLayer.build_closed_layer(categories)
    generated = searcher.build_taxonomy(leaf_layer)
    score, layer_scores = TaxonomyScore(reference=reference).evaluate(generated)
    return reference, generated, score, layer_scores


def print_taxonomy(taxonomy):
    for i, layer in enumerate(taxonomy.layers):
        print i, "=", layer


def print_scores(layer_scores, total_score):
    print "Layer scores:", layer_scores
    print "Total score: ", total_score


def save_results(searcher_name, dataset_name, results, result_dir):
    file_path = "{}/{}_{}.dat".format(result_dir, searcher_name, dataset_name)
    with open(file_path, "w") as f:
        cPickle.dump(results, f)


if __name__ == '__main__':
    main()
