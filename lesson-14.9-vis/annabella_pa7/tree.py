#!/usr/bin/python
# -*- coding: utf-8 -*-
# CS121: Treemap assignment
#
# Class for representing tree nodes
#
#####################################
# DO NOT MODIFY THE CODE IN THIS FILE
#####################################

import textwrap
import numpy as np


class Tree(object):

    def __init__(self, label, count=None, children=None):
        '''
        Construct a Tree

        Inputs:
            label: (string) a label that identifies the root node
            count: (float) an application specific weight
            children: (list of Tree) child nodes, or None if no children
        '''
        self.label = label
        self.count = count
        if children is None:
            self.children = []
        else:
            self.children = children
        self.verbose_label = None

    def num_children(self):
        '''
        Returns the number of children in the tree
        '''
        return len(self.children)

    def add_child(self, other_tree):
        """
        Adds an existing tree as a child of the tree.

        Parameter:
        - other_tree: Tree to add as a subtree
        """
        if not isinstance(other_tree, Tree):
            raise ValueError("Parameter to add_child must be a Tree object")

        self.children.append(other_tree)

    def __print_r(self, prefix, last, kformat, vformat, maxdepth, verbose):
        ''' Recursive helper method for print() '''
        if maxdepth is not None:
            if maxdepth == 0:
                return
            else:
                maxdepth -= 1

        if len(prefix) > 0:
            if last:
                lprefix1 = prefix[:-3] + u"  └──"
            else:
                lprefix1 = prefix[:-3] + u"  ├──"
        else:
            lprefix1 = u""

        if len(prefix) > 0:
            lprefix2 = prefix[:-3] + u"  │"
        else:
            lprefix2 = u""

        if last:
            lprefix3 = lprefix2[:-1] + "   "
        else:
            lprefix3 = lprefix2 + "  "

        if verbose:
            label = self.verbose_label
        else:
            label = self.label

        if self.count is None:
            ltext = (kformat).format(label)
        else:
            ltext = (kformat + ": " + vformat).format(label, self.count)

        ltextlines = textwrap.wrap(ltext, 80, initial_indent=lprefix1,
                                   subsequent_indent=lprefix3)

        print(lprefix2)
        print(u"\n".join(ltextlines))

        if self.children is None:
            return
        else:
            for i, st in enumerate(self.children):
                if i == len(self.children) - 1:
                    newprefix = prefix + u"   "
                    newlast = True
                else:
                    newprefix = prefix + u"  │"
                    newlast = False

                st.__print_r(newprefix, newlast, kformat, vformat, maxdepth, verbose)

    def print(self, kformat="{}", vformat="{}", maxdepth=None, verbose=False):
        '''
        Inputs: self: (the tree object)
                kformat: (format string) specifying format for label
                vformat: (format string) specifying format for label and count
                maxdepth: (integer) indicating number of levels to print.
                          None sets no limit
                verbose: (boolean) Prints verbose labels if True

        Returns:  no return value, but a tree is printed to screen
        '''
        self.__print_r(u"", False, kformat, vformat, maxdepth, verbose)


def create_st(relevant_rows, hierarchy, hierarchy_labels, level_label):
    '''
    Recursively creates subtrees

    '''
    if len(hierarchy) == 0:
        # Return leaf node with count of relevant rows
        return Tree(level_label,
                                 count=np.asscalar(relevant_rows["count"].sum()))
    else:
        curr_children = []
        curr_level = hierarchy[0]
        hierarchy = list(hierarchy[1:])
        for level_value in hierarchy_labels[curr_level]:
            curr_rows = relevant_rows[relevant_rows[curr_level] == level_value]
            curr_children.append(create_st(curr_rows, hierarchy,
                                 hierarchy_labels, level_value))
        return Tree(level_label, children=curr_children)


def data_to_tree(data, hierarchy):
    '''
    Converts a pandas DataFrame to a tree (using Tree) following a
    specified hierarchy

    Inputs:
        data: (pandas.DataFrame) the data to be represented as a tree
        hierarchy: (list of strings) a list of column names to be used as
                   the levels of the tree in the order given. Note that all
                   strings in the hierarchy must correspond to column names
                   in data

    Returns: a tree (using the Tree class) representation of data
    '''
    if hierarchy is None or len(hierarchy) == 0:
        raise ValueError("Hierarchy must be a non-empty list of column names")
    # create dictionary of possible values for each level of the hierarchy
    hierarchy_labels = {}
    for level in hierarchy:
        if level not in data.columns:
            raise ValueError("Column " + str(level) + " included in the \
                  hierarchy, but does not exist in data", data.columns)
        else:
            hierarchy_labels[level] = data[level].unique()
    return create_st(data, hierarchy, hierarchy_labels, "")
