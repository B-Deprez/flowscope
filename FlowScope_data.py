import pandas as pd

import pandas as pd

def process_data(string_name):
    transaction_data = pd.read_csv('inputData/synthetic/raw/edge_data_'+string_name+'.csv')
    transaction_data['money'] = 1
    transaction_data.to_csv('inputData/synthetic/processed/edge_data_'+string_name+'.csv', index=False, header=False)

n_nodes_list = [200]#[100, 10000, 100000] # Number of nodes in the graph
m_edges_list = [2]#[1, 2, 5] # Number of edges to attach from a new node to existing nodes
p_edges_list = [0.01]#[0.001, 0.01] # Probability of adding an edge between two nodes
generation_method_list = [
    'Barabasi-Albert', 
    'Erdos-Renyi', 
    'Watts-Strogatz'
    ] # Generation method for the graph
n_patterns_list = [3]#[3, 5] # Number of smurfing patterns to add

for n_nodes in n_nodes_list:
    for n_patterns in n_patterns_list:
        if n_patterns <= 0.06*n_nodes:
            for generation_method in generation_method_list:
                if generation_method == 'Barabasi-Albert':
                    p_edges = 0
                    for m_edges in m_edges_list:
                        string_name = 'synthetic_' + generation_method + '_'  + str(n_nodes) + '_' + str(m_edges) + '_' + str(p_edges) + '_' + str(n_patterns)
                        process_data(string_name)

                if generation_method == 'Erdos-Renyi':
                    m_edges = 0
                    for p_edges in p_edges_list:
                        string_name = 'synthetic_' + generation_method + '_'  + str(n_nodes) + '_' + str(m_edges) + '_' + str(p_edges) + '_' + str(n_patterns)
                        process_data(string_name)

                if generation_method == 'Watts-Strogatz':
                    for m_edges in m_edges_list:
                        for p_edges in p_edges_list:
                            string_name = 'synthetic_' + generation_method + '_'  + str(n_nodes) + '_' + str(m_edges) + '_' + str(p_edges) + '_' + str(n_patterns)
                            process_data(string_name)