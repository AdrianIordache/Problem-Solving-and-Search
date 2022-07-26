from utils import *

def generate_network_matrix(
    nodes: int = 10,   edge_probability: float = 0.5, 
    seed:  int = SEED, view_graph: bool = True
    ) -> np.array:

    graph  = erdos_renyi_graph(nodes, edge_probability, seed = seed)
    
    for (u, v, w) in graph.edges(data = True):
        w['weight'] = random.randint(0, 10)

    matrix = np.array(adjacency_matrix(graph).todense())

    if view_graph:
        plt.figure(figsize = (5, 5))
        plt.title("Network Graph")
        nx.draw(
            from_numpy_matrix(matrix), 
            with_labels = True
        )
        plt.show()

    return matrix # np.where(matrix == 0, np.inf, matrix)

class User:
    global_id = -1
    def __init__(self, connections_and_costs: Dict[int, int] = {}):
        User.global_id += 1
        self.uid = User.global_id
        self.connections_and_costs = connections_and_costs

    def __str__(self):
        return f"[User {self.uid}], Connections: {list(self.connections_and_costs.keys())}, Costs: {list(self.connections_and_costs.values())}"

class Network:
    def __init__(self, network_matrix: np.array = None):
        self.network_matrix = network_matrix

        self.users = []
        for uid, costs in enumerate(self.network_matrix):
            connections = np.where(costs != 0)[0]
            self.users.append(
                User(connections_and_costs = 
                    {connection : cost for (connection, cost) in zip(connections, costs[connections])}
                )
            )

    def __str__(self):
        network = ""
        for uid, user in enumerate(self.users): 
            network += str(user) 
            if uid != len(self.users) - 1: network += '\n'

        return network

    def depth_first_search(self, start_id: int, finish_id: int):
        def _depth_search(self, node_id: int, finish_id: int, visited: List[int]):
            if node_id == finish_id: 
                visited.append(finish_id)
                return True, visited

            if node_id not in visited:
                visited.append(node_id)
                for connection_id in self.users[node_id].connections_and_costs.keys():
                    exit, _ = _depth_search(self, connection_id, finish_id, visited)
                    if exit: return True, visited

            return False, visited

        visited = list()
        found, path = _depth_search(self, start_id, finish_id, visited)

        graph    = from_numpy_matrix(self.network_matrix)
        netx_dfs = list(dfs_tree(graph, start_id))[: len(path)]

        if found:
            print(f"Path from User {start_id} to User {finish_id} found: {path}")
        else:
            print(f"Path from User {start_id} to User {finish_id} not found")

        assert path == netx_dfs, "Different results between networkx DFS and our DFS"

    def breadth_first_search(self, start_id: int, finish_id: int):
        def _breadth_search(self, node_id: int, finish_id: int, visited: List[int], queue: List[int]):
            visited.append(node_id)
            queue.append(node_id)

            path  = []
            found = False
            while queue:
                start = queue.pop(0)
                path.append(start)
                if start == finish_id: break

                for connection_id in self.users[start].connections_and_costs.keys(): 
                    if connection_id not in visited:
                        visited.append(connection_id)
                        queue.append(connection_id)

            if finish_id in path: found = True
            return found, path

        visited, queue = list(), list()
        found, path = _breadth_search(self, start_id, finish_id, visited, queue)
        print(path)

        graph    = from_numpy_matrix(self.network_matrix)
        netx_bfs = list(bfs_tree(graph, start_id))[: len(path)]
        print(netx_bfs)

    def has_connection(self, start_id: int, finish_id: int):
        graph = from_numpy_matrix(self.network_matrix)
        return has_path(graph, start_id, finish_id)

if __name__ == "__main__":
    NODES = 1000
    EDGE_PROBABILITY = 0.7

    network_matrix = generate_network_matrix(
        nodes            = NODES, 
        edge_probability = EDGE_PROBABILITY, 
        seed             = SEED, 
        view_graph       = False
    )

    print(network_matrix)
    
    network = Network(network_matrix = network_matrix) 
    network.breadth_first_search(start_id = 1, finish_id = 985)

    print(network.has_connection(1, 3))