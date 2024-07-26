import numpy as np
import networkx as nx
import random
import pandas as pd


def purchase_probability(Nt, Bt, h):
    if h == 0:
        return Bt/Nt
    return (h*Bt)/(1000*Nt)


def create_graph(file):
    G = nx.read_edgelist(file, delimiter=",")
    G.edges(data=True)
    return G


def probability(G, u, v, probabilities):
    n = len(list(nx.common_neighbors(G, u, v)))
    if n in probabilities:
        return probabilities[n]
    else:
        return 0


def sim_graph(G, probabilities):
    new_G = G.copy()
    for edge in nx.non_edges(G):
        edge_probability = probability(G, *edge, probabilities)
        if random.random() <= edge_probability:
            new_G.add_edge(*edge)
    return new_G


def find_probability(G_1, G0):
    number_of_common_true = {}
    number_of_common_false = {}
    for non_edge in nx.non_edges(G_1):
        if non_edge in G0.edges():
            common_n = list(nx.common_neighbors(G_1, *non_edge))
            if len(common_n) in number_of_common_true:
                number_of_common_true[len(common_n)] = number_of_common_true[len(common_n)] + 1
            else:
                number_of_common_true[len(common_n)] = 1
        if non_edge not in G0.edges():
            common_n = list(nx.common_neighbors(G_1, *non_edge))
            if len(common_n) in number_of_common_false:
                number_of_common_false[len(common_n)] = number_of_common_false[len(common_n)] + 1
            else:
                number_of_common_false[len(common_n)] = 1
    for key, value in number_of_common_false.items():
        if key in number_of_common_true:
            number_of_common_true[key] = number_of_common_true[key] / (number_of_common_true[key] + value)
    return number_of_common_true


def buyers_neighbors(G, u):
    neighbors = list(G.neighbors(u))
    buyers = 0
    for node in neighbors:
        if G.nodes[node]['color'] == 'black':
            buyers += 1
    return buyers


def create_plays_dict():
    spotifly_df = pd.read_csv('spotifly.csv')
    spotifly = {}
    for key, val1, val2 in spotifly_df.values:
        if key in spotifly.keys():
            spotifly[key].append((val1, val2))
        else:
            spotifly[key] = [(val1, val2)]
    return spotifly


def num_of_plays(spotifly, user, artist):
    for artistID, plays in spotifly[int(user)]:
        if artistID == artist:
            return plays
        else:
            continue
    return 0


def degree_centrality_measure(G, j):
    if j == 0:
        print("influencers:")
    for i in range(5):
        top_node = (sorted(nx.degree_centrality(G).items(), key=lambda x: x[1], reverse=True)[i][0])
        if j == 0:
            print(top_node)
        nx.set_node_attributes(G, {top_node: 'black'}, 'color')


def eigenvector_centrality_measure(G):
    for i in range(5):
        top_node = (sorted(nx.eigenvector_centrality(G).items(), key=lambda x: x[1], reverse=True)[i][0])
        nx.set_node_attributes(G, {top_node: 'black'}, 'color')


def closeness_centrality_measure(G, j):
    if j == 0:
        print("influencers:")
    for i in range(5):
        top_node = (sorted(nx.closeness_centrality(G).items(), key=lambda x: x[1], reverse=True)[i][0])
        if j == 0:
            print(top_node)
        nx.set_node_attributes(G, {top_node: 'black'}, 'color')


def betweenness_centrality_measure(G, j):
    if j == 0:
        print("influencers:")
    for i in range(5):
        top_node = (sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)[i][0])
        if j == 0:
            print(top_node)
        nx.set_node_attributes(G, {top_node: 'black'}, 'color')


def load_centrality_measure(G):
    for i in range(5):
        top_node = (sorted(nx.load_centrality(G).items(), key=lambda x: x[1], reverse=True)[i][0])
        nx.set_node_attributes(G, {top_node: 'black'}, 'color')


def subgraph_centrality_measure(G):
    for i in range(5):
        top_node = (sorted(nx.subgraph_centrality(G).items(), key=lambda x: x[1], reverse=True)[i][0])
        nx.set_node_attributes(G, {top_node: 'black'}, 'color')


def harmonic_centrality_measure(G, j):
    if j == 0:
        print("influencers:")
    for i in range(5):
        top_node = (sorted(nx.harmonic_centrality(G).items(), key=lambda x: x[1], reverse=True)[i][0])
        if j == 0:
            print(top_node)
        nx.set_node_attributes(G, {top_node: 'black'}, 'color')


if __name__ == '__main__':
    G_1 = create_graph('instaglam_1.csv')
    G0 = create_graph('instaglam0.csv')
    G0.remove_node('userID')
    G0.remove_node('friendID')
    G_1.remove_node('userID')
    G_1.remove_node('friendID')
    spotifly = create_plays_dict()
    probabilities = find_probability(G_1, G0)
    print(probabilities)
    artists = [989, 16326, 144882, 194647]
    for artist in artists:
        print("artist " + str(artist) + ":")

        print("degree measure:")
        degree_results = []
        for i in range(5):
            G0 = create_graph('instaglam0.csv')
            G0.remove_node('userID')
            G0.remove_node('friendID')
            nx.set_node_attributes(G0, 'white', 'color')
            degree_centrality_measure(G0, i)
            for j in range(6):
                new_G = sim_graph(G0, probabilities)
                buyers = []
                for u in new_G.nodes:
                    if u == 'userID' or u == 'friendID':
                        continue
                    if random.random() <= purchase_probability(new_G.degree(u), buyers_neighbors(new_G, u),
                                                               num_of_plays(spotifly, u, artist)):
                        buyers.append(u)
                for node in buyers:
                    nx.set_node_attributes(new_G, {node: 'black'}, 'color')
                num_of_buyers = 0
                for node in new_G.nodes:
                    if new_G.nodes[node]['color'] == 'black':
                        num_of_buyers += 1
                G0 = new_G
            degree_results.append(num_of_buyers)
        print("results:")
        print(degree_results)
        print("mean:")
        print(np.mean(degree_results))
        print("variance:")
        print(np.var(degree_results))

        print("harmonic measure:")
        harmonic_results = []
        for i in range(5):
            G0 = create_graph('instaglam0.csv')
            G0.remove_node('userID')
            G0.remove_node('friendID')
            nx.set_node_attributes(G0, 'white', 'color')
            harmonic_centrality_measure(G0, i)
            for j in range(6):
                new_G = sim_graph(G0, probabilities)
                buyers = []
                for u in new_G.nodes:
                    if u == 'userID' or u == 'friendID':
                        continue
                    if random.random() <= purchase_probability(new_G.degree(u), buyers_neighbors(new_G, u),
                                                               num_of_plays(spotifly, u, artist)):
                        buyers.append(u)
                for node in buyers:
                    nx.set_node_attributes(new_G, {node: 'black'}, 'color')
                num_of_buyers = 0
                for node in new_G.nodes:
                    if new_G.nodes[node]['color'] == 'black':
                        num_of_buyers += 1
                G0 = new_G
            harmonic_results.append(num_of_buyers)
        print("results:")
        print(harmonic_results)
        print("mean:")
        print(np.mean(harmonic_results))
        print("variance:")
        print(np.var(harmonic_results))

        print("closeness results:")
        closeness_results = []
        for i in range(5):
            G0 = create_graph('instaglam0.csv')
            G0.remove_node('userID')
            G0.remove_node('friendID')
            nx.set_node_attributes(G0, 'white', 'color')
            closeness_centrality_measure(G0, i)
            for j in range(6):
                new_G = sim_graph(G0, probabilities)
                buyers = []
                for u in new_G.nodes:
                    if u == 'userID' or u == 'friendID':
                        continue
                    if random.random() <= purchase_probability(new_G.degree(u), buyers_neighbors(new_G, u),
                                                               num_of_plays(spotifly, u, artist)):
                        buyers.append(u)
                for node in buyers:
                    nx.set_node_attributes(new_G, {node: 'black'}, 'color')
                num_of_buyers = 0
                for node in new_G.nodes:
                    if new_G.nodes[node]['color'] == 'black':
                        num_of_buyers += 1
                G0 = new_G
            closeness_results.append(num_of_buyers)
        print("results:")
        print(closeness_results)
        print("mean:")
        print(np.mean(closeness_results))
        print("variance:")
        print(np.var(closeness_results))

        print("betweenness results:")
        betweenness_results = []
        for i in range(5):
            G0 = create_graph('instaglam0.csv')
            G0.remove_node('userID')
            G0.remove_node('friendID')
            nx.set_node_attributes(G0, 'white', 'color')
            betweenness_centrality_measure(G0, i)
            for j in range(6):
                new_G = sim_graph(G0, probabilities)
                buyers = []
                for u in new_G.nodes:
                    if u == 'userID' or u == 'friendID':
                        continue
                    if random.random() <= purchase_probability(new_G.degree(u), buyers_neighbors(new_G, u),
                                                               num_of_plays(spotifly, u, artist)):
                        buyers.append(u)
                for node in buyers:
                    nx.set_node_attributes(new_G, {node: 'black'}, 'color')
                num_of_buyers = 0
                for node in new_G.nodes:
                    if new_G.nodes[node]['color'] == 'black':
                        num_of_buyers += 1
                G0 = new_G
            betweenness_results.append(num_of_buyers)
        print("results:")
        print(betweenness_results)
        print("mean:")
        print(np.mean(betweenness_results))
        print("variance:")
        print(np.var(betweenness_results))
        print("")
