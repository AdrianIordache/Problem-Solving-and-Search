from utils import *
from games import *

class DepthFirstSearch:
    def __init__(self, start_node: Sudoku):
        self.start_node = start_node
        self.stack = [self.start_node]
        self.visited_nodes = []
        
        self.steps = 0
        self.path  = []

    def append(self, node: Sudoku):
        self.stack.insert(0, node)

    def pop(self):
        node = self.stack.pop(0)
        self.visited_nodes.append(node)
        return node

    def search(self):
        while True:
            if len(self.stack) == 0: return False, self.visited_nodes
            self.steps += 1
            current_node = self.pop()
            self.path.append(current_node)

            if current_node.is_solution(): return True, self.path
            extended_nodes = current_node.expand()

            for extended_node in extended_nodes:
                if extended_node not in self.stack and \
                    extended_node not in self.visited_nodes:
                    self.stack.append(extended_node)


class BreadthFirstSearch:
    def __init__(self, start_node: Sudoku):
        self.start_node = start_node
        self.queue = [self.start_node]
        self.visited_nodes = []
        
        self.steps = 0
        self.path  = []

    def append(self, node):
        self.queue.append(node)

    def pop(self):
        node = self.queue.pop(0)
        self.visited_nodes.append(node)
        return node

    def search(self):
        while True:
            if len(self.queue) == 0: return False, self.visited_nodes

            self.steps += 1
            current_node = self.pop()
            self.path.append(current_node)

            if current_node.is_solution(): return True, self.path
            extended_nodes = current_node.expand()

            for extended_node in extended_nodes:
                if extended_node not in self.queue and \
                    extended_node not in self.visited_nodes:
                    self.queue.append(extended_node)



class AStar:
    def __init__(self, start_node: Puzzle8):
        self.start_node = start_node
        self.opened = [self.start_node]
        self.closed = []

        self.computation_steps = 0
        self.solution = []

    # check if we already have a better node in list so we wont use the current one
    def already_have_better_node(self, current_node: Puzzle8, already_have_nodes: Puzzle8):
        for existing_node in already_have_nodes: 
            if existing_node < current_node: return True
        return False

    def reconstruct_solution(self, node: Puzzle8):
        while node.parent is not None:
            self.solution.append(node)
            node = node.parent

        self.solution.append(self.start_node)
        self.solution.reverse()

        for node in self.solution:
            print(node)

        print(f"Total number of moves: {len(self.solution)}")

    def search(self): 
        while len(self.opened) > 0:
            current = self.opened.pop(0)
            self.closed.append(current)
            self.computation_steps += 1

            if current.is_solution():
                print(f"Found solution after: {self.computation_steps} iteration steps")
                self.reconstruct_solution(current)
                break

            extended_nodes = current.expand()

            for extended_node in extended_nodes:
                if extended_node in self.opened and self.already_have_better_node(extended_node, self.opened):
                    continue
                elif extended_node in self.closed and self.already_have_better_node(extended_node, self.closed):
                    continue
                else:
                    self.opened.append(extended_node)

            self.opened.sort(key = lambda x: x.f)


class GeneticAlgorithm:
    def __init__(self, n_queens: int = 8, population_size: int = 10, mixing_parents: int = 2, mutation_rate: float = 0.05):
        self.n_queens        = n_queens
        self.population_size = population_size
        self.mixing_parents  = mixing_parents
        self.mutation_rate   = mutation_rate

        self.population = [NQueens(self.n_queens) for _ in range(self.population_size)]

    def solution_in_population(self):
        for idx, individual in enumerate(self.population):
            if individual.is_solution(): return (True, idx)
        return (False, -1)

    def selection(self):
        return [individual for individual in self.population if random.randrange(sc.comb(self.n_queens, 2) * 2) < individual.fitness_score()]

    def crossover(self, parents):
        # cross-points between idividuals, lets say there are 3 individuals we want to mix, we need 2 cross points
        cross_points = random.sample(range(self.n_queens), self.mixing_parents - 1)

        # Mixing parents M by M 
        permutations = list(itertools.permutations(parents, self.mixing_parents))

        offsprings = []
        for pm in permutations:
            offspring = []
            start_pt  = 0

            for parent_idx, cross_point in enumerate(cross_points):
                parent_part = pm[parent_idx].get_genes(start_pt, cross_point)
                offspring.extend(parent_part)
                start_pt = cross_point

            last_parent = pm[-1]
            parent_part = last_parent.get_genes(cross_point, self.n_queens)
            offspring.extend(parent_part)

            offsprings.append(NQueens(self.n_queens, offspring))

        return offsprings

    def mutate(self, individual):
        for gene_idx in range(len(individual)):
            if random.random() < self.mutation_rate:
                individual.set_genes(gene_idx, random.randrange(self.n_queens)) 

        return individual

    def evolution(self):
        parents    = self.selection()
        offsprings = self.crossover(parents) 
        mutations  = [self.mutate(individual) for individual in offsprings]

        self.population = mutations + self.population
        self.population = sorted(
            self.population, 
            key     = lambda individual: individual.fitness_score(), 
            reverse = True)[: self.population_size]

    def run(self):
        while True:
            is_solution, solution_idx = self.solution_in_population()
            
            print(self.population[0])
            if is_solution:
                print(self.population[solution_idx].individual)
                print(f"Solution Found, Score: {self.population[solution_idx].fitness_score()}")
                print(self.population[solution_idx])
                break

            self.evolution()
            

class MinMaxAlgorithm:
    def change_player(self, player):
        if player == "X": return "O"
        return "X"

    def _min_max(self, game, depth, player):
        if depth == 0 or game.is_solution():
            if game.check_board_state() == "X":
                return 0 
            elif game.check_board_state() == "O":
                return 100
            else:
                return 50

        if player == "O":
            best_score = 0
            for move in game.check_available_moves():
                game.expand(move, player)
                move_score = self._min_max(game, depth - 1, self.change_player(player))
                game.expand(move, " ")
                best_score = max(best_score, move_score)

            return best_score
        
        if player == "X":
            best_score = 100
            for move in game.check_available_moves():
                game.expand(move, player)
                move_score = self._min_max(game, depth - 1, self.change_player(player))
                game.expand(move, " ")
                best_score = min(best_score, move_score)

            return best_score

    def best_move(self, game, depth, player):
        choices = []
        neutral_score = 50

        for move in game.check_available_moves():
            game.expand(move, player)
            move_score = self._min_max(game, depth - 1, self.change_player(player))
            game.expand(move, " ")

            if move_score > neutral_score:
                choices = [move]
                break

            elif move_score == neutral_score:
                choices.append(move)
        
        print("AI possible choices: ", [c + 1 for c in choices])

        if len(choices) > 0:
            return random.choice(choices)
        else:
            return random.choice(game.check_available_moves())
