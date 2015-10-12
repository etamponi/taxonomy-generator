import cPickle
import csv
import sys

from deltaphi import shapes
from deltaphi.category_info import CategoryLayer
from deltaphi.experiments.assessment import Taxonomy, SearchTaxonomy, TaxonomyScore
from deltaphi.experiments.dataset_definitions import DATASET_DEFINITIONS
from deltaphi.metrics import LookAhead, CharacteristicTerms, DiscriminantTerms
from deltaphi.parent_layer_search import LayerGreedyMergeSearch
from deltaphi.raw_filter import RawFilter
from deltaphi.sources import CSVRawSource, CategoryInfoSource

__author__ = 'Emanuele'


DATASET_DIR = "datasets"
RESULT_DIR = "results"

CHARACTERISTIC_AREA = shapes.PSphere([1, 0], 0.6, 1)
DISCRIMINANT_AREA = shapes.PSphere([0, 1], 1.0, 1) | shapes.PSphere([0, -1], 1.0, 1)

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
SEARCHER_NAME = "characteristic_0.6_discriminant_1.0"


def main():
    csv.field_size_limit(sys.maxint)
    log_path = "{}/{}_log.txt".format(RESULT_DIR, SEARCHER_NAME)
    with open(log_path, "w") as f:
        log(f, "Testing {}", SEARCHER_NAME)
        for dataset_name in get_dataset_names():
            log(f, "Running experiment: {}", dataset_name)
            categories = get_categories(dataset_name, DATASET_DIR)
            reference, generated, score, layer_scores = run_experiment(SEARCHER, categories)
            log(f, "Reference taxonomy:")
            log_taxonomy(f, reference)
            log(f, "Generated taxonomy:")
            log_taxonomy(f, generated)
            log(f, "Scores:")
            log_scores(f, layer_scores, score)
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


def log_taxonomy(f, taxonomy):
    for i, layer in enumerate(taxonomy.layers):
        log(f, "{} = {}", i, layer)


def log_scores(f, layer_scores, total_score):
    log(f, "Layer scores: {}", layer_scores)
    log(f, "Total score: {}", total_score)


def save_results(searcher_name, dataset_name, results, result_dir):
    file_path = "{}/{}_{}.dat".format(result_dir, searcher_name, dataset_name)
    with open(file_path, "w") as f:
        cPickle.dump(results, f)


def log(f, fmt, *params):
    line = fmt.format(*params)
    f.write(line + "\n")
    print line


if __name__ == '__main__':
    main()
