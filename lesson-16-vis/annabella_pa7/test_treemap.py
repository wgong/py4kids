'''
Tests for treemaps
'''

import json
import pytest
import operator
import glob
import treemap
import tree as tr
from itertools import permutations

# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg= invalid-name, missing-docstring, too-many-arguments, line-too-long
# pylint: disable-msg= missing-docstring, too-many-locals, unused-argument, broad-except
# pylint: disable-msg= assignment-from-none

TREE_TEST_PARAMS=[]
for data in ("small", "full"):
    for i in range(1, 4):
        for levels in permutations(["company", "race", "gender", "job_category"], i):
            param = pytest.param(data, levels, id="{}-{}".format(data, ",".join(levels)))
            TREE_TEST_PARAMS.append(param)


PRUNE_TEST_PARAMS=['data/pruned-tree-small-1_company.json',
                   'data/pruned-tree-small-2_company-gender.json',
                   'data/pruned-tree-small-3_company-gender.json',
                   'data/pruned-tree-small-4_company-gender.json',
                   'data/pruned-tree-small-5_company-race-gender.json',
                   'data/pruned-tree-small-6_company-race-gender.json',
                   'data/pruned-tree-full-1_company.json',
                   'data/pruned-tree-full-2_company-gender.json',
                   'data/pruned-tree-full-3_company-gender.json',
                   'data/pruned-tree-full-4_company-gender.json',
                   'data/pruned-tree-full-5_company-race-gender.json',
                   'data/pruned-tree-full-6_company-race-gender.json',
                   'data/pruned-tree-full-7_job_category-race-gender.json',
                   'data/pruned-tree-full-8_company-race-gender.json',
                   'data/pruned-tree-full-9_company-gender-race.json']


@pytest.fixture(scope="session")
def datasets():
    """
    Fixture for loading the datasets
    """
    d = {}

    d["small"] = treemap.load_diversity_data("data/diversity-small.csv")
    d["data/diversity-small.csv"] = d["small"]
    d["full"] = treemap.load_diversity_data("data/diversity.csv")
    d["data/diversity.csv"] = d["full"]

    # Make sure the test files are there
    task1_files = glob.glob("data/tree-*.json")
    if len(task1_files) == 0:
        pytest.fail("Could not find the test files for Task 1. Did you remember to run get_files.sh?")

    task2_files = glob.glob("data/pruned-*.json")
    if len(task2_files) == 0:
        pytest.fail("Could not find the test files for Task 2. Did you remember to run get_files.sh?")

    task3_files = glob.glob("data/rectangles-*.json")
    if len(task3_files) == 0:
        pytest.fail("Could not find the test files for Task 3. Did you remember to run get_files.sh?")

    return d


def compare_trees(tree, expected_tree, error_prefix, compare_counts=False, compare_verbose_labels=False):
    if tree.verbose_label is None:
        vl = "None"
    else:
        vl = "'{}'".format(tree.verbose_label)

    node_error_prefix = error_prefix + "Checking a node with label='{}', count={}, verbose_label={}\n".format(tree.label, tree.count, vl)

    if compare_counts:
        assert tree.count == expected_tree["count"], \
            node_error_prefix + "Node has incorrect count." \
                                "Got {}, expected {}".format(tree.count, expected_tree["count"])

    if compare_verbose_labels:
        assert tree.verbose_label == expected_tree["verbose_label"], \
            node_error_prefix + "Node has incorrect verbose label." \
                                "Got {}, expected '{}'".format(vl, expected_tree["verbose_label"])


    children = tree.children
    expected_children = expected_tree["children"]

    if expected_children is None:
        assert children is None or children == [], node_error_prefix + "Expected node to have no children, but it has children."
    else:
        for c in children:
            assert isinstance(c, tr.Tree), node_error_prefix + "Node has a child that is not a Tree: {}".format(c)

        sorted_children = sorted(children, key=operator.attrgetter("label"))
        sorted_expected_children = sorted(expected_children, key=operator.itemgetter("label"))
        labels = [c.label for c in sorted_children]
        expected_labels = [c["label"] for c in sorted_expected_children]


        assert labels == expected_labels, node_error_prefix + "Expected node to have children with labels {} " \
                                                              "but the children's labels are {}".format(expected_labels, labels)

        for child, expected_child in zip(sorted_children, sorted_expected_children):
            compare_trees(child, expected_child, error_prefix, compare_counts, compare_verbose_labels)


def fcompare(prefix, rect, expected_rect, attr):
    got = getattr(rect, attr)
    expected = expected_rect[attr]
    assert got == pytest.approx(expected), prefix +  "Rectangle '{}' has incorrect {} " \
                                                     "(got {}, expected {})".format(rect.verbose_label, attr, got, expected)


def compare_rectangles(rects, expected_rects, error_prefix):
    assert len(rects) == len(expected_rects), "Expected {} rectangles, but got {} instead".format(len(expected_rects), len(rects))

    sorted_rects = sorted(rects, key=operator.attrgetter("verbose_label"))
    sorted_expected_rects = sorted(expected_rects, key=operator.itemgetter("verbose_label"))

    labels = [r.verbose_label for r in sorted_rects]
    expected_labels = [r["verbose_label"] for r in sorted_expected_rects]

    assert labels == expected_labels, error_prefix + "Expected rectangles with labels {} " \
                                                     "but the labels are {}".format(expected_labels, labels)

    for rect, expected_rect in zip(sorted_rects, sorted_expected_rects):
        for attr in ("x","y","width","height"):
            fcompare(error_prefix, rect, expected_rect, attr)


@pytest.mark.parametrize("d,levels", TREE_TEST_PARAMS)
def test_compute_internal_counts(datasets, d, levels):
    test_file = "data/tree-" + d + "_" + "-".join(levels) + ".json"
    error_prefix = "Error when testing {}\n".format(test_file)

    test_data = json.load(open(test_file))
    tree = tr.data_to_tree(datasets[d], levels)

    total_count = treemap.compute_internal_counts(tree)

    assert total_count == test_data["total_count"], \
        error_prefix + "Incorrect compute_internal_counts return value. " \
                       "Got {}, expected {}".format(total_count, test_data["total_count"])

    assert tree.label == "", "Root node does not have empty string label"
    assert tree.count == test_data["tree"]["count"], \
        error_prefix + "Root node has incorrect count." \
        "Got {}, expected {}".format(tree.count, test_data["tree"]["count"])

    compare_trees(tree, test_data["tree"], error_prefix, compare_counts=True)


@pytest.mark.parametrize("d,levels", TREE_TEST_PARAMS)
def test_compute_verbose_labels(datasets, d, levels):
    test_file = "data/tree-" + d + "_" + "-".join(levels) + ".json"
    error_prefix = "Error when testing {}\n".format(test_file)

    test_data = json.load(open(test_file))
    tree = tr.data_to_tree(datasets[d], levels)

    treemap.compute_verbose_labels(tree)

    compare_trees(tree, test_data["tree"], error_prefix, compare_verbose_labels=True)


@pytest.mark.parametrize("test_file", PRUNE_TEST_PARAMS)
def test_prune_tree(datasets, test_file):
    error_prefix = "Error when testing {}\n".format(test_file)

    test_data = json.load(open(test_file))

    tree = tr.data_to_tree(datasets[test_data["dataset"]], test_data["levels"])
    pruned_tree = treemap.prune_tree(tree, test_data["prune"])

    compare_trees(pruned_tree, test_data["tree"], error_prefix, compare_counts=True)


@pytest.mark.parametrize("d,levels", TREE_TEST_PARAMS)
def test_compute_rectangles(datasets, d, levels):
    test_file = "data/rectangles-" + d + "_" + "-".join(levels) + ".json"
    error_prefix = "Error when testing {}\n".format(test_file)

    expected_rects = json.load(open(test_file))
    tree = tr.data_to_tree(datasets[d], levels)

    rects = treemap.compute_rectangles(tree)

    compare_rectangles(rects, expected_rects["rectangles"], error_prefix)