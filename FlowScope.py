import spartan as st
from sklearn.metrics import roc_auc_score, average_precision_score
import pandas as pd

def flowscope_synthetic(string_name):
    # load graph data
    transaction_data = pd.read_csv('inputData/synthetic/raw/edge_data_synthetic.csv')
    fs1_tensor_data = st.loadTensor(path = "./inputData/synthetic/processed/edge_data_"+string_name+".csv", header=None)
    fs2_tensor_data = st.loadTensor(path = "./inputData/synthetic/processed/edge_data_"+string_name+".csv", header=None)

    fs1_stensor = fs1_tensor_data.toSTensor(hasvalue=True)
    fs2_stensor = fs2_tensor_data.toSTensor(hasvalue=True)

    maxshape = max(fs1_stensor.shape[1], fs2_stensor.shape[0])
    fs1_stensor.shape = (fs1_stensor.shape[0], maxshape)
    fs2_stensor.shape = (maxshape, fs2_stensor.shape[1])

    graph_1 = st.Graph(fs1_stensor, bipartite=True, weighted=True, modet=None)
    graph_2 = st.Graph(fs2_stensor, bipartite=True, weighted=True, modet=None)

    step2list = []
    step2list.append(graph_1)
    step2list.append(graph_2)

    fs = st.FlowScope(step2list)
    res = fs.run(k=3, alpha=4,maxsize=(10,10,10))

    num_nodes = max(set(transaction_data.source).union(set(transaction_data.target)))+1

    laundering = []
    number_list = []

    keys_list = [i for i in range(num_nodes)]
    values_list = [0]*len(keys_list)
    map_scores = dict(zip(keys_list, values_list))

    for i in range(len(res)):
        r = res[i][0]
        for d in r:
            d_list = list(d)
            for j in range(len(d_list)):
                map_scores[d_list[j]]= (3-i)/3
            laundering+=d_list
            number_list.append(i)

    label_data = pd.read_csv('./inputData/synthetic/raw/label_data_'+string_name+'.csv')
    label_data['node'] = label_data.index
    label_data['score'] = label_data['node'].map(map_scores)
    label_data['score'] = label_data['score'].fillna(0)

    # Calculate the AUC-ROC and AUC-PR
    AUC_ROC = roc_auc_score(label_data['laundering'], label_data['score'])
    AUC_PR = average_precision_score(label_data['laundering'], label_data['score'])
    return AUC_ROC, AUC_PR

## Run the FlowScope algorithm on the synthetic data

n_nodes_list = [100, 10000, 100000] # Number of nodes in the graph
m_edges_list = [1, 2, 5] # Number of edges to attach from a new node to existing nodes
p_edges_list = [0.001, 0.01] # Probability of adding an edge between two nodes
generation_method_list = [
    'Barabasi-Albert', 
    'Erdos-Renyi', 
    'Watts-Strogatz'
    ] # Generation method for the graph
n_patterns_list = [3, 5] # Number of smurfing patterns to add

results_all = dict()

for n_nodes in n_nodes_list:
    for n_patterns in n_patterns_list:
        if n_patterns <= 0.06*n_nodes:
            for generation_method in generation_method_list:
                if generation_method == 'Barabasi-Albert':
                    p_edges = 0
                    for m_edges in m_edges_list:
                        string_name = 'synthetic_' + generation_method + '_'  + str(n_nodes) + '_' + str(m_edges) + '_' + str(p_edges) + '_' + str(n_patterns)
                        print("====", string_name, "====")
                        result_int = flowscope_synthetic(string_name)
                        results_all[string_name] = result_int

                if generation_method == 'Erdos-Renyi':
                    m_edges = 0
                    for p_edges in p_edges_list:
                        string_name = 'synthetic_' + generation_method + '_'  + str(n_nodes) + '_' + str(m_edges) + '_' + str(p_edges) + '_' + str(n_patterns)
                        print("====", string_name, "====")
                        result_int = flowscope_synthetic(string_name)
                        results_all[string_name] = result_int

                if generation_method == 'Watts-Strogatz':
                    for m_edges in m_edges_list:
                        for p_edges in p_edges_list:
                            string_name = 'synthetic_' + generation_method + '_'  + str(n_nodes) + '_' + str(m_edges) + '_' + str(p_edges) + '_' + str(n_patterns)
                            print("====", string_name, "====")
                            result_int = flowscope_synthetic(string_name)
                            results_all[string_name] = result_int

results_df = pd.DataFrame(results_all)
results_df.to_csv("synthetic_flowscope_"+str_supervised+"_"+str_directed+"_combined.csv")