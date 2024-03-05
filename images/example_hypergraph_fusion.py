from fusion_blossom import SolverInitializer, SolverSerial, SyndromePattern

# Offline
vertex_num = 5
weighted_edges = [(0, 4, 100), (0, 1, 100), (1, 2, 100), (2, 3, 100)]
virtual_vertices = [4]
initializer = SolverInitializer(vertex_num, weighted_edges, virtual_vertices)
fusion = SolverSerial(initializer)

# Online
syndrome = [0, 1, 3]
fusion.solve(SyndromePattern(syndrome))
fusion_subgraph = fusion.subgraph()
print(fusion_subgraph)  # out: [0, 2, 3]
