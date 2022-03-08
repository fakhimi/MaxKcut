import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '..')

from max_k_cut import *
from networkx import *
import sys
import numpy as np

seed 			= int(sys.argv[1])
num_vertices 	= int(sys.argv[2])
num_partitions 	= int(sys.argv[3])
penalty_increase= float(sys.argv[4])
noise 			= float(sys.argv[5])

name 			= "seed" + str(seed) + "_band_test_" + ("naive" if penalty_increase > 1 else "tight")
graph 			= nx.Graph( )

# graph 			= nx.erdos_renyi_graph(num_vertices, .8, seed=seed, directed=False)


np.random.seed(seed) 
edges = [(i, j, 2*np.random.randint(0, 2) - 1) for i in np.arange(1, num_vertices, 1) for j in np.arange(i + 1, min(i+num_partitions+1, num_vertices) + 1, 1)]


graph.add_weighted_edges_from(edges)

problem			= Instance(graph, name_specifier=name)


problem.Params.Num_Partitions 			= num_partitions

problem.Params.Verbosity 				= 2

problem.Params.Peel 					= False
problem.Params.Fold 					= False
problem.Params.Decompose 				= False

problem.Params.Method 					= "R-QUBO" #R-QUBO BQO
problem.Params.Naive 					= (True if penalty_increase > 1 else False)

# problem.Params.Curvature_Type 			= "convex" 			#"concave"
# problem.Params.Curvature_Method 		= "power_iteration"

problem.Params.Gurobi_TimeLimit			= 3600
# problem.Params.Gurobi_LogToConsole 		= 1
# problem.Params.QAOA_Optimize 			= False

problem.Params.QAOA_Scipy_Optimizer 	= "brute" #Nelder-Mead brute
# problem.Params.Penalty_Increase 		= penalty_increase

# problem.Params.QAOA_Angles				= [0.26, 0.38] #[0.26, 0.38]
problem.Params.QAOA_Num_Levels			= 1
problem.Params.QAOA_Num_Shots			= 10000
problem.Params.QAOA_Brute_Num_Samples 	= 50
# problem.Params.QAOA_Gates_Noise			= noise

problem.solve()