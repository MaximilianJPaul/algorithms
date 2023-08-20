from vertex import Vertex
from edge import Edge


class Graph():
    def __init__(self):
        self.vertices = []  # list of vertices in the graph
        self.edges = []  # list of edges in the graph
        self.num_vertices = 0
        self.num_edges = 0
        self.undirected_graph = True

    def get_number_of_vertices(self):
        """
        :return: the number of vertices in the graph
        """
        return self.num_vertices

    def get_number_of_edges(self):
        """
        :return: the number of edges in the graph
        """
        return self.num_edges

    def get_vertices(self):
        """
        :return: list of length get_number_of_vertices() with the vertices of the graph
        """
        return self.vertices

    def get_edges(self):
        """
        :return: list of length get_number_of_edges() with the edges of the graph
        """
        return self.edges

    def insert_vertex(self, vertex_name):
        """
        Inserts a new vertex with the given name into the graph.
        Returns None if the graph already contains a vertex with the same name.
        The newly added vertex should store the index at which it has been added.

        :param vertex_name: The name of vertex to be inserted
        :return: The newly added vertex, or None if the vertex was already part of the graph
        :raises: ValueError if vertex_name is None
        """
        if vertex_name is None:
            raise ValueError("Undefined argument!")

        if self.find_vertex(vertex_name):
            return None
        else:
            new_vertex = Vertex(self.get_number_of_vertices(), vertex_name)
            self.vertices.append(new_vertex)
            self.num_vertices += 1
            return new_vertex


    def find_vertex(self, vertex_name):
        """
        Returns the respective vertex for a given name, or None if no matching vertex is found.
        :param vertex_name: the name of the vertex to find
        :return: the found vertex, or None if no matching vertex has been found.
        :raises: ValueError if vertex_name is None.
        """
        if vertex_name is None:
            raise ValueError("Undefined argument!")

        for v in self.get_vertices():
            if v.name == vertex_name:
                return v
        
        return None

    def insert_edge_by_vertex_names(self, v1_name, v2_name, weight: int):
        """
        Inserts an edge between two vertices with the names v1_name and v2_name and returns the newly added edge.
        None is returned if the edge already existed, or if at least one of the vertices is not found in the graph.
        A ValueError shall be thrown if v1 equals v2 (=loop).
        :param v1_name: name (string) of vertex 1
        :param v2_name: name (string) of vertex 2
        :param weight: weight of the edge
        :return: Returns None if the edge already exists or at least one of the two given vertices is not part of the
                 graph, otherwise returns the newly added edge.
        :raises: ValueError if v1 is equal to v2 or if v1 or v2 is None.
        """
        if v1_name == v2_name or v1_name is None or v2_name is None:
            raise ValueError("Given arguments are equal or undefined!") 

        v1 = self.find_vertex(v1_name)
        v2 = self.find_vertex(v2_name)

        if v1 is None or v2 is None or self.find_edge(v1, v2):
            return None
        else:
            edge = Edge(v1, v2, weight)
            self.edges.append(edge)
            self.num_edges += 1

            return edge
        

    def insert_edge(self, v1: Vertex, v2: Vertex, weight: int):
        """
        Inserts an edge between two vertices v1 and v2 and returns the newly added edge.
        None is returned if the edge already existed, or if at least one of the vertices is not found in the graph.
        A ValueError shall be thrown if v1 equals v2 (=loop).
        :param v1: vertex 1
        :param v2: vertex 2
        :param weight: weight of the edge
        :return: Returns None if the edge already exists or at least one of the two given vertices is not part of the
                 graph, otherwise returns the newly added edge.
        :raises: ValueError if v1 is equal to v2 or if v1 or v2 is None.
        """
        if v1 == v2 or v1 is None or v2 is None:
            raise ValueError("Given arguments are equal or undefined!")
        
        v1 = self.find_vertex(v1.name)
        v2 = self.find_vertex(v2.name)

        if v1 is None or v2 is None or self.find_edge(v1, v2):
            return None
        else:
            edge = Edge(v1, v2, weight)
            self.edges.append(edge)
            self.num_edges += 1
            return edge

    def find_edge_by_vertex_names(self, v1_name, v2_name):
        """
        Returns the edge if there is an edge between the vertices with the name v1_name and v2_name, otherwise None.
        In case both names are identical a ValueError shall be raised.
        :param v1_name: name (string) of vertex 1
        :param v2_name: name (string) of vertex 2
        :return: Returns the found edge or None if there is no edge.
        :raises: ValueError if v1_name equals v2_name or if v1_name or v2_name is None.
        """
        if v1_name == v2_name or not v1_name or not v2_name:
            raise ValueError("Given arguments are equal or undefined!")

        for e in self.edges:
            if (e.first_vertex.name == v1_name and e.second_vertex.name == v2_name) or (e.first_vertex.name == v2_name and e.second_vertex == v1_name):
                return e

        return None

    def find_edge(self, v1: Vertex, v2: Vertex):
        """
        Returns the edge if there is an edge between the vertices v1 and v2, otherwise None.
        In case v1 equals v2 a ValueError shall be raised.
        :param v1: vertex 1
        :param v2: vertex 2
        :return: Returns the found edge or None if there is no edge.
        :raises: ValueError if v1 equals v2 or if v1 or v2 are None.
        """
        if v1 == v2 or v1 is None or v2 is None:
            raise ValueError("Given arguments are equal or undefined!")

        for e in self.edges:
            if (e.first_vertex == v1 and e.second_vertex == v2) or (e.first_vertex == v2 and e.second_vertex == v1):
                return e

        return None

    def get_adjacency_matrix(self):
        """
        Returns the NxN adjacency matrix for the graph, where N = get_number_of_vertices().
        The matrix contains the edge weight if there is an edge at the corresponding index position, otherwise -1.
        :return: adjacency matrix
        """
        matrix = []

        for v1 in self.get_vertices():
            adj_list = []

            for v2 in self.get_vertices():
                if v1 == v2 or self.find_edge(v1, v2) is None:
                    adj_list.append(-1)
                else:
                    edge = self.find_edge(v1, v2)
                    adj_list.append(edge.weight)
            
            matrix.append(adj_list)

        return matrix


    def get_adjacent_vertices_by_vertex_name(self, vertex_name):
        """
        Returns a list of vertices which are adjacent to the vertex with name vertex_name based on the ordering in which
        they occur in the adjacency matrix.
        :param vertex_name: The name of the vertex to which adjacent vertices are searched.
        :return: list of vertices that are adjacent to the vertex with name vertex_name.
        :raises: ValueError if vertex_name is None
        """
        if vertex_name is None:
            raise ValueError("Undefined argument!")

        adj_vertices = []
        matrix = self.get_adjacency_matrix()

        index = self.find_vertex(vertex_name).idx
        
        for v in range(self.get_number_of_vertices()):
            if matrix[index][v] != -1:
                adj_vertices.append(self.vertices[v])

        return adj_vertices

    def get_adjacent_vertices(self, vertex: Vertex):
        """
        Returns a list of vertices which are adjacent to the given vertex based on the ordering in which
        they occur in the adjacency matrix.
        :param vertex: The vertex to which adjacent vertices are searched.
        :return: list of vertices that are adjacent to the vertex.
        :raises: ValueError if vertex is None
        """
        if vertex is None:
            raise ValueError("Undefined argument!")

        adj_vertices = []
        matrix = self.get_adjacency_matrix()

        index = self.find_vertex(vertex.name).idx
        
        for v in range(self.get_number_of_vertices()):
            if matrix[index][v] != -1:
                adj_vertices.append(self.vertices[v])

        return adj_vertices
