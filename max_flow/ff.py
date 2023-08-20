# Ford-Fulkerson algorith in Python

class Graph:

    def __init__(self, graph):
        self.graph = graph  # original graph
        self.residual_graph = [[cell for cell in row] for row in graph]  # cloned graph
        self.latest_augmenting_path = [[0 for cell in row] for row in
                                       graph]  # empty graph with same dimension as graph
        self.current_flow = [[0 for cell in row] for row in graph]  # empty graph with same dimension as graph


    def ff_step(self, source, sink):
        """
        Perform a single flow augmenting iteration from source to sink
        Update the latest augmenting path, the residual graph and the current flow by the maximum possible amount according to your chosen path.
        The path must be chosen based on BFS.
        @param source the source's vertex id
        @param sink the sink's vertex id
        @return the amount by which the flow has increased.
        """
        # TO DO
        augmenting_path = [[0 for cell in row] for row in self.graph]

        path_exists, parent = self.bfs(source, sink)
        min_flow = float("Inf")
        path = []

        if path_exists:
            s = sink
            while s != source:
                min_flow = min(min_flow, self.residual_graph[parent[s]][s])
                path.append(s)
                s = parent[s]
            path.append(s)
            path.reverse()
            
            for i in range(len(path) - 1):
                augmenting_path[path[i]][path[i + 1]] = min_flow
            
            self.latest_augmenting_path = augmenting_path

            v = sink
            while v != source:
                u = parent[v]
                self.residual_graph[u][v] -= min_flow
                self.residual_graph[v][u] += min_flow
                if self.graph[u][v] == 0:
                    self.current_flow[v][u] -= min_flow
                else:
                    self.current_flow[u][v] += min_flow
                v = parent[v]

            return min_flow
        
        return 0


    def ford_fulkerson(self, source, sink):
        """
        Execute the ford-fulkerson algorithm (i.e., repeated calls of ff_step())
        @param source the source's vertex id
        @param sink the sink's vertex id
        @return the max flow from source to sink
        """
        # TO DO
        max_flow = 0
        path_exists, _ = self.bfs(source, sink)

        while path_exists:
            max_flow += self.ff_step(source, sink)
            path_exists, _ = self.bfs(source, sink)

        return max_flow

    def bfs(self, source, sink):
        parent = [-1] * len(self.graph)

        visited = [False] * len(self.graph)
        queue = []

        queue.append(source)
        visited[source] = True

        while queue:
            u = queue.pop(0)

            for index, value in enumerate(self.residual_graph[u]):
                if visited[index] == False and value > 0:
                    queue.append(index)
                    visited[index] = True
                    parent[index] = u

        result = (visited[sink], parent)
        return result