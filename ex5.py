# -*- coding: utf-8 -*-
import numpy as np
import copy
import pprint


class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

        if parent:
            self.parent.children.append(self)


def print_tree(current_node, childattr='children', nameattr='name', indent='', last='updown'):

    if hasattr(current_node, nameattr):
        name = lambda node: getattr(node, nameattr)
    else:
        name = lambda node: str(node)

    children = lambda node: getattr(node, childattr)
    nb_children = lambda node: sum(nb_children(child) for child in children(node)) + 1
    size_branch = {child: nb_children(child) for child in children(current_node)}

    """ Creation of balanced lists for "up" branch and "down" branch. """
    up = sorted(children(current_node), key=lambda node: nb_children(node))
    down = []
    while up and sum(size_branch[node] for node in down) < sum(size_branch[node] for node in up):
        down.append(up.pop())

    """ Printing of "up" branch. """
    for child in up:
        next_last = 'up' if up.index(child) is 0 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', ' ' * len(name(current_node)))
        print_tree(child, childattr, nameattr, next_indent, next_last)

    """ Printing of current node. """
    if last == 'up': start_shape = '┌'
    elif last == 'down': start_shape = '└'
    elif last == 'updown': start_shape = ' '
    else: start_shape = '├'

    if up: end_shape = '┤'
    elif down: end_shape = '┐'
    else: end_shape = ''

    print('{0}{1}{2}{3}'.format(indent, start_shape, name(current_node), end_shape))

    """ Printing of "down" branch. """
    for child in down:
        next_last = 'down' if down.index(child) is len(down) - 1 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', ' ' * len(name(current_node)))
        print_tree(child, childattr, nameattr, next_indent, next_last)

#parsing file into list of samples, where 0-no 1-yes 2-unanswered 0-democrat 1-republican
def parseSampleFile(f):
    with open(f) as file:
        content = file.readlines()
    content = [line.strip().split(" ") for line in content]
    for s in content:
        for i in range(len(s)):
            if s[i] == "n":
                s[i] = 0
            elif s[i] == "y":
                s[i] = 1
            elif s[i] == "u":
                s[i] = 2
            elif s[i] == "republican.":
                s[i] = 1
            else:
                s[i] = 0
    return [(parts[0:-1], parts[-1]) for parts in content]

def ratio_labeled_1(sample):
    return len([s for s in sample if s[1] == 1])/float(len(sample))

def sample_by_feature_value(sample, feature, value):
    return [s for s in sample if s[0][feature] == value]


def entropy_err(p):
    if p==0 or p==1:
        return 0
    p = float(p)
    return -p*np.log2(p) - (1-p)*np.log2(1-p)

def gain(sample, feature, err_f):
    feature_split = [sample_by_feature_value(sample, feature, i) for i in range(3)]
    feature_ratios = [len(s)/float(len(sample)) for s in feature_split]
    error_terms_to_sum = [feature_ratios[i] * err_f(ratio_labeled_1(feature_split[i])) for i in range(3)]
    prev_error = err_f(ratio_labeled_1(sample))
    return prev_error - sum(error_terms_to_sum)

def id3(samples, attributes, max_depth=9999):
    return

def main():
    validation = parseSampleFile("validation.txt")
    print(gain(validation, 6, entropy_err))

if __name__ == "__main__":
    main()
