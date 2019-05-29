import simpy
import random
import matplotlib.pyplot as plt

# Simpy Params
UNIT_TIME = 1
NODE_W = 1
NODE_M = 2

# K and N
NODE_COUNT = 10000
EDGE_COUNT = 20000

# Adjustable Params
START_W = 0.5
P = 0.1
Q = 0.5

# Global Statistics
class Counter:
    def __init__(self):
        self.W_counts = []
        self.M_counts = []
        self.W = 0
        self.M = 0

    def increment_W(self):
        self.W += 1

    def increment_M(self):
        self.M += 1

    def plot(self):
        l = len(self.W_counts)
        plt.plot(range(l), self.W_counts, 'r--', range(l), self.M_counts, 'b--')
        plt.show()

    def update(self, plus_w):
        if plus_w:
            self.W += 1
            self.M -= 1
        else:
            self.W -= 1
            self.M += 1

    def count(self, env):
        # count number of nodes every unit time
        while True:
            yield env.timeout(UNIT_TIME)
            self.W_counts.append(self.W)
            self.M_counts.append(self.M)


## Individual node ##

def node(env, counter, node_type):
    while True:
        yield env.timeout(UNIT_TIME)
        if node_type == NODE_W:
            if random.random() < P:
                # W --> M
                counter.update(False)
        if node_type == NODE_M:
            if random.random() < Q:
                # M --> W
                counter.update(True)




##### MAIN Function ############
my_counter = Counter()

env = simpy.Environment()
env.process(my_counter.count(env))
for i in range(NODE_COUNT):
    if i < NODE_COUNT * START_W:
        my_counter.increment_W()
        env.process(node(env, my_counter, NODE_W))
    else:
        my_counter.increment_M()
        env.process(node(env, my_counter, NODE_M))
env.run(until=1000)

my_counter.plot()
