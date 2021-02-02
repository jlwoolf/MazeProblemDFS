import sys  # only used to get the argument data
import graphviz  # used to produce the graph png

# hex color codes dictionary for coloring the
# nodes on the png
colors = {
    'B': '#53618D',
    'G': '#739639',
    'R': '#E42839',
    'Y': '#F0C402',
    'O': '#FA9327',
    '0': '#000000',
    'W': '#FFFFFF'
}


# Simple node class to store information about each
# node in the graph
class Node:
    def __init__(self, num=-1, color=''):
        self.num = num
        self.color = color
        self.adj = set()
        self.start = False

    def add_adj(self, node, color):
        self.adj.add((node, color))


# function that reads the file and formats it into a
# model for future use. The format is a dictionary called
# nodes that maps each nodes numerical value to a node
# class instance. This was my work around for python's
# lack of pointers
def readFile():
    nodes = {}
    fin = open(sys.argv[1])

    n, m = fin.readline().split()

    i = 1
    for color in fin.readline().split():
        nodes[i] = Node(i, color)
        i += 1
    nodes[i] = Node(i, 'O')

    x, y = fin.readline().split()
    nodes[int(x)].start = True
    nodes[int(y)].start = True

    for line in fin:
        try:
            i, j, color = line.split()
        except ValueError:
            break

        nodes[int(i)].add_adj(int(j), color)

    return int(x), int(y), nodes


# function that takes in the node dictionary and converts
# it into a graphviz graph that produces a pretty good looking
# visual of the graph
def createImage(nodes):
    graph = graphviz.Digraph(comment='Graph!', format='png')
    starts = []
    for node in nodes:
        if nodes[node].start:
            starts.append(node)

        graph.node(str(nodes[node].num), style='filled', color=colors[nodes[node].color], fontsize='128', width='4',
                   height='4')
        for edge in nodes[node].adj:
            graph.edge(str(nodes[node].num), str(nodes[edge[0]].num), penwidth='28', color=colors[edge[1]],
                       arrowhead='open', arrowsize='4')

    for start in starts:
        graph.node('s' + str(nodes[start].num), label='Start!', shape='rect', color=colors['O'], style='filled',
                   fontsize='128', width='4',
                   height='4')
        graph.edge('s' + str(nodes[start].num), str(nodes[start].num), penwidth='28', color=colors['0'],
                   arrowhead='open', arrowsize='4')

    graph.render('graph')


# class that handles all of the pathfinding
# decided to make a class dfs with the necessary functions for
# a dfs as there were some global variables like color, parents
# and time that each recursion calls and python is different
# with how it handles variables. A little less control than with
# c++ (prefered language)
class DFS:
    def __init__(self, s1, s2, nodes):
        self.s1 = s1
        self.s2 = s2
        self.nodes = nodes

        self.c = None
        self.p = None
        self.d = None
        self.time = None
        self.end = None

    # run a dfs on the graph with recursive calls of
    # dfs_visit. Colors, time, and parent data was stored
    # as a matrix of size N x N where N is the number of nodes.
    # Each cell represents a possible graph state. For instance,
    # when R was in 5 and L was in 7, d[5,7] will tell you the
    # both discovery and finish times
    def dfs(self):
        self.c = [["WHITE" for i in range(len(nodes))] for i in range(len(nodes))]
        self.p = [[[] for i in range(len(nodes))] for i in range(len(nodes))]
        self.d = [[[] for i in range(len(nodes))] for i in range(len(nodes))]
        self.time = 0

        self.dfs_visit(s1, s2)
        return self.d, self.p, self.end

    # this is almost a carbon copy of the dfs_visit function
    # from the slides, however, there exist 2 for loops when
    # looking at adjacent nodes, unlike the 1 from the slides.
    # the reason is that the first for loop looks at opportunities
    # to move Rocket, while the second tries to move Lucky. That
    # way, all possible game states are found, and a path can
    # be made
    def dfs_visit(self, l1, l2):
        if l1 == len(nodes) or l2 == len(nodes):
            self.end = [l1, l2]

        self.c[l1 - 1][l2 - 1] = "GREY"
        self.time += 1
        self.d[l1 - 1][l2 - 1].append(self.time)
        for adj in self.nodes[l1].adj:
            if adj[1] == self.nodes[l2].color and self.c[adj[0] - 1][l2 - 1] == "WHITE":
                self.p[adj[0] - 1][l2 - 1] = [l1, l2]
                self.dfs_visit(adj[0], l2)
        for adj in self.nodes[l2].adj:
            if adj[1] == self.nodes[l1].color and self.c[l1 - 1][adj[0] - 1] == "WHITE":
                self.p[l1 - 1][adj[0] - 1] = [l1, l2]
                self.dfs_visit(l1, adj[0])
        self.c[l1 - 1][l2 - 1] = "BLACK"
        self.time += 1
        self.d[l1 - 1][l2 - 1].append(self.time)

    # takes the data produced from the dfs algorithm and converts
    # it into a readable output. This is done by starting at the finishing
    # states parent data and following up until the start state.
    # as each state is read, it is pushed into a stack. When the start is
    # reached, each element is removed from the stack.
    def printSoln(self):
        soln = []
        end = self.end
        while end != [self.s1, self.s2]:
            parent = self.p[end[0] - 1][end[1] - 1]
            if parent[0] == end[0]:
                soln.insert(0, "L " + str(end[1]))
            else:
                soln.insert(0, "R " + str(end[0]))
            end = parent

        for line in soln:
            print(line)


# main function to run it all
if __name__ == '__main__':
    s1, s2, nodes = readFile()
    createImage(nodes)

    dFS = DFS(s1, s2, nodes)
    dFS.dfs()
    dFS.printSoln()
