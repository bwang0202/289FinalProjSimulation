import simpy
import random
import matplotlib.pyplot as plt
import numpy as np

# Simpy Params
UNIT_TIME = 1
WK = 1
MN = 2
BM = 3
BW = 4
SW = 5
FW = 6
MAX_TYPE = 6

RUNTIME = 50

# K and N
NODE_COUNT = 10000
EDGE_COUNT = 80000

# Adjustable Params
START_W = 0.5
R = 0.8
M = 0.1
P = 0.8
Q = 0.2
N = 0.7
X = 0.1
Y = 0.8
T = 0.3
V = 0.3

assert(P + Q <= 1)
assert(X + Y <= 1)

class Node:
    def __init__(self, idx, tp):
        self.idx = idx
        self.type = tp

    def set_type(self, tp):
        self.type = tp
    def get_type(self):
        return self.type

    def evolve(self, env, network):
        while True:
            yield env.timeout(UNIT_TIME)
            # Rules of node changing goes here


class Edge:
    def __init__(self, a, b):
        self.idx_a = a
        self.idx_b = b

    def evolve(self, env, network):
        while True:
            yield env.timeout(UNIT_TIME)
            # Rules of edge changing goes here


class Network:
    def __init__(self, K, N):
        self.K = K
        self.N = N
        self.adj_matrix = np.zeros((N, N))
        self.nodes = []

    def get_node_type(self, idx):
        return self.nodes[idx].get_type()

    def set_node_type(self, idx, tp):
        self.nodes[idx].set_type(tp)

    def output_node_counts(self):
        result = np.zeros(MAX_TYPE)
        for i in range(self.N):
            result[self.nodes[i].get_type() - 1] += 1
        return result

    def init_env(self, env):
        # Assign node types, only start with WorKers/MaNagers
        for i in range(self.N):
            if random.random() < START_W:
                self.nodes.append(Node(i, WK))
            else:
                self.nodes.append(Node(i, MN))
            env.process(self.nodes[-1].evolve(env, self))

        # Random ER Graph
        edge_count = 0
        p = 2 * self.K / (self.N * (self.N - 1))
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if random.random() <= p:
                    # link them!
                    edge_count += 1
                    self.adj_matrix[i,j] = 1
                    self.adj_matrix[j,i] = 1
                    env.process(Edge(i, j).evolve(env, self))
        return edge_count

# Global Statistics
class Counter:
    def __init__(self):
        self.records = []

    def plot(self):
        data = np.array(self.records)
        colors = ['r--', 'b--', 'c--', 'y--', 'k--', 'm--']
        typestr = ['Worker', 'Manager', 'Busy Manager', 'Busy Worker', 'Success Worker', 'Failed Worker']

        for i in range(MAX_TYPE):
            #plot with legend
            plt.plot(data[:,i], colors[i], label=typestr[i])

        plt.legend()
        plt.grid()
        plt.show()

    def count(self, env, network):
        # count number of nodes every unit time
        while True:
            yield env.timeout(UNIT_TIME)
            self.records.append(network.output_node_counts())




##### MAIN Function ############
my_counter = Counter()

env = simpy.Environment()
mynetwork = Network(NODE_COUNT, EDGE_COUNT)
mynetwork.init_env(env)
env.process(my_counter.count(env, mynetwork))

env.run(until=RUNTIME)

my_counter.plot()
