"""
Linear Extensions of Directed Acyclic Graphs.

A linear extension of a directed acyclic graph is a total (linear) ordering on
the vertices that is compatible with the graph in the following sense:
if there is a path from x to y in the graph, the x appears before y in the
linear extension.

The algorithm implemented in this module is from "Generating Linear Extensions
Fast" by Preusse and Ruskey, which can be found at
http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.52.3057 .  The algorithm
generates the extensions in constant amortized time (CAT) -- a constant amount
of time per extension generated, or linear in the number of extensions
generated.

EXAMPLES:

Here we generate the 5 linear extensions of the following directed
acyclic graph::

    sage: from sage.graphs.linearextensions import LinearExtensions
    sage: D = DiGraph({ 0:[1,2], 1:[3], 2:[3,4] })
    sage: D.is_directed_acyclic()
    True
    sage: sorted(LinearExtensions(D))
    [[0, 1, 2, 3, 4],
     [0, 1, 2, 4, 3],
     [0, 2, 1, 3, 4],
     [0, 2, 1, 4, 3],
     [0, 2, 4, 1, 3]]

Notice how all of the total orders are compatible with the ordering
induced from the graph.

We can also get at the linear extensions directly from the graph.  From
the graph, the linear extensions are known as topological sorts ::

    sage: sorted(D.topological_sort_generator())
    [[0, 1, 2, 3, 4],
     [0, 1, 2, 4, 3],
     [0, 2, 1, 3, 4],
     [0, 2, 1, 4, 3],
     [0, 2, 4, 1, 3]]


"""
#*****************************************************************************
#      Copyright (C) 2008 Mike Hansen <mhansen@gmail.com>
#
# Distributed  under  the  terms  of  the  GNU  General  Public  License (GPL)
#                         http://www.gnu.org/licenses/
#*****************************************************************************
from sage.structure.parent import Parent
from sage.categories.finite_enumerated_sets import FiniteEnumeratedSets

class LinearExtensions(Parent):
    def __init__(self, dag):
        r"""
        Creates an object representing the class of all linear extensions
        of the directed acyclic graph \code{dag}.

        EXAMPLES::

            sage: from sage.graphs.linearextensions import LinearExtensions
            sage: D = DiGraph({ 0:[1,2], 1:[3], 2:[3,4] })
            sage: l = LinearExtensions(D)
            sage: l == loads(dumps(l))
            True

        TESTS::

            sage: list(LinearExtensions(DiGraph({ })))
            [[]]

            sage: LinearExtensions(DiGraph({ 0:[1], 1:[0] }))
            Traceback (most recent call last):
            ...
            ValueError: The graph is not directed acyclic

        """
        from sage.combinat.posets.posets import Poset
        self._dag = Poset(dag) # this returns a copy
        Parent.__init__(self, category = FiniteEnumeratedSets())

    def _repr_(self):
        """
        TESTS::

            sage: from sage.graphs.linearextensions import LinearExtensions
            sage: D = DiGraph({ 0:[1,2], 1:[3], 2:[3,4] })
            sage: LinearExtensions(D)
            Linear extensions of Finite poset containing 5 elements

        """
        return "Linear extensions of %s"%self._dag

    def __iter__(self):
        """
        Iterate over the linear extensions of the directed acyclic graph.

        EXAMPLES::

            sage: from sage.graphs.linearextensions import LinearExtensions
            sage: D = DiGraph({ 0:[1,2], 1:[3], 2:[3,4] })
            sage: sorted(LinearExtensions(D))
            [[0, 1, 2, 3, 4],
             [0, 1, 2, 4, 3],
             [0, 2, 1, 3, 4],
             [0, 2, 1, 4, 3],
             [0, 2, 4, 1, 3]]

        TESTS::

            sage: D = DiGraph({ "a":["b","c"], "b":["d"], "c":["d","e"] })
            sage: sorted(LinearExtensions(D))
            [['a', 'b', 'c', 'd', 'e'],
             ['a', 'b', 'c', 'e', 'd'],
             ['a', 'c', 'b', 'd', 'e'],
             ['a', 'c', 'b', 'e', 'd'],
             ['a', 'c', 'e', 'b', 'd']]

            sage: D = DiGraph({ 4:[3,2], 3:[1], 2:[1,0] })
            sage: sorted(LinearExtensions(D))
            [[4, 2, 0, 3, 1],
             [4, 2, 3, 0, 1],
             [4, 2, 3, 1, 0],
             [4, 3, 2, 0, 1],
             [4, 3, 2, 1, 0]]

        """
        from sage.combinat.combinat_cython import linear_extension_iterator
        elts = list(self._dag)
        for e in linear_extension_iterator(self._dag._hasse_diagram):
            yield [elts[i] for i in e]
