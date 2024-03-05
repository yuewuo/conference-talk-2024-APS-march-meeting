from mwpf import HyperEdge, SolverInitializer, SolverSerialJointSingleHair, SyndromePattern

# Offline
vertex_num = 4
weighted_edges = [
    HyperEdge([0, 1], 100),  # [vertices], weight
    HyperEdge([1, 2], 100),
    HyperEdge([2, 3], 100),
    HyperEdge([0], 100),  # boundary vertex
    HyperEdge([0, 1, 2], 60),  # hyperedge
]
initializer = SolverInitializer(vertex_num, weighted_edges)
hyperion = SolverSerialJointSingleHair(initializer)

# Online
syndrome = [0, 1, 3]
hyperion.solve(SyndromePattern(syndrome))
hyperion_subgraph = hyperion.subgraph()
print(hyperion_subgraph)  # out: [2, 4]
_, bound = hyperion.subgraph_range()
print((bound.lower, bound.upper))  # out: (Fraction(160, 1), Fraction(160, 1))
