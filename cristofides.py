from heapq import heapify, heappop, heappush
import numpy as np
import random

class CRIST:
    
    def __init__(self, dist: list[list[int]]):
        self.dist = dist
        self.n = len(dist)

    def ans(self):
        mst = self.prim() #minimum spanning tree
        d = self.degree(mst) #degree of each node
        sub = self.sub_graph(d) #graph of odd-degree-nodes
        matching = self.match(sub, d) #minimum matching
        euler_graph = self.unite(mst, matching) #sub + matching has euler circuit
        euler_circuit = self.circuit(euler_graph) #make circuit
        hamilton = self.skip(euler_circuit) #make trail
                
        print('route: ' + str(hamilton[1]))
        print('weight: ' + str(hamilton[0]))

    def ans2(self):
        mst = self.prim()
        tmp = mst
        for i in range(len(tmp)):
            mst.append( (tmp[i][0], (tmp[i][1][1], tmp[i][1][0])) )
        
        circuit = self.circuit(mst)
        hamilton = self.skip(circuit)
        
        print('route: ' + str(hamilton[1]))
        print('weight: ' + str(hamilton[0]))

    def prim(self):
        tree = [] #answer
        heap = [] #heap
        marked = [False for _ in range(self.n)] #marked?
        new_node = 0 #new node marked lately
        marked[new_node] = True #marked first node
        count = 1 #the number of marked node
        weight = 0 #total weight
        while count < self.n:
            for i in range(self.n):
                if marked[i] == True: #skip
                    continue
                heappush(heap, (self.dist[new_node][i], (new_node, i))) #push all neighbor of current tree

            for i in heap:
                line = heappop(heap) #check whether addable to tree
                if marked[line[1][1]] == False:
                    break
            
            #new_vertex
            weight += line[0]
            marked[line[1][1]] = True
            count += 1
            new_node = line[1][1]
            tree.append(line)

        tree.sort()
        return tree
    
    def degree(self, mst):
        deg = [0 for _ in range(self.n)]
        for i in range(len(mst)):
            deg[mst[i][1][0]] += 1
            deg[mst[i][1][1]] += 1

        return deg
    
    def sub_graph(self, deg):
        sub = []
        for i in range(self.n):
            for j in range(i, self.n):
                if deg[i] % 2 == 0 or deg[j] % 2 == 0 or i == j:
                    continue
                sub.append( (self.dist[i][j], (i, j)) )

        sub.sort()
        return sub
    
    def match(self, sub, deg): #greedy
        matching = []
        for e in sub:
            if deg[e[1][0]] % 2 == 1 and deg[e[1][1]] % 2 == 1:
                matching.append(e)
                #heappush(matching, e)
                deg[e[1][0]] += 1
                deg[e[1][1]] += 1

        return matching

    def unite(self, mst, matching):
        euler = mst
        euler.extend(matching)
        euler.sort()

        return euler

    def circuit(self, euler_graph):
        deg = [0 for _ in range(self.n)]
        for i in euler_graph:
            deg[i[1][0]] += 1
            deg[i[1][1]] += 1

        ans = []
        stack = []
        list = euler_graph
        current_node = list[0][1][0]

        while deg[current_node]>0 or stack != []:
            if deg[current_node] == 0:
                ans.append(current_node)
                current_node = stack.pop()
            else:
                stack.append(current_node)
                for neighbor in list:
                    if neighbor[1][0] == current_node:
                        deg[current_node] -= 1
                        deg[neighbor[1][1]] -= 1
                        current_node = neighbor[1][1]
                        list.remove(neighbor)
                        break
                    elif neighbor[1][1] == current_node:
                        deg[current_node] -= 1
                        deg[neighbor[1][0]] -= 1
                        current_node = neighbor[1][0]
                        list.remove(neighbor)
                        break

        return ans

    def skip(self, circuit):
        weight = 0
        order = []
        cir = circuit
        visited = [0 for _ in range(self.n)]
        c = cir.pop(0)
        first = c
        while len(cir)>=0:
            visited[c] = True
            if cir == []:
                order.append(c)
                order.append(first)
                weight += self.dist[c][first]
                break
            elif visited[cir[0]] == True:
                cir.pop(0)
            else:
                order.append(c)
                cc = cir.pop(0)
                weight += self.dist[c][cc]
                #w.append(self.dist[c][cc])
                c = cc
        return (weight, order)


def main():
    #random sample data
    num = 100
    data = [[random.randint(0, 100) for _ in range(num)] for _ in range(num)]
    
    c = CRIST(data)
    c.ans()


if __name__ == "__main__":
    main()