import os
import copy
import random
import argparse
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from scipy  import special as sc
from typing import List, Dict, Tuple
from abc    import ABC, abstractmethod

from networkx.convert_matrix import from_numpy_matrix
from networkx.linalg.graphmatrix import adjacency_matrix
from networkx.generators.random_graphs import erdos_renyi_graph
from networkx.algorithms.shortest_paths.generic import has_path
from networkx.algorithms.traversal.breadth_first_search import bfs_tree
from networkx.algorithms.traversal.depth_first_search import dfs_edges, dfs_tree

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

class State(ABC):
    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def is_solution(self):
        pass

    @abstractmethod
    def expand(self):
        pass
