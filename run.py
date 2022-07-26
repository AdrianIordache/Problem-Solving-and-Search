from utils import *
from games import *
from algorithms import *

parser = argparse.ArgumentParser()

parser.add_argument('--task', dest = "task", type = int, required = True, default = 1, 
        help = "Run the application for a specific task [1: Sudoku, 2: 8-Puzzle, 3: N-Quens, 4: TicTacToe]"
    )

if __name__ == "__main__":
    args = parser.parse_args()
    task = args.task 

    if task == 1:
        print("Solving Sudoku using DFS or BFS")
        name = str(input("Enter the number of the text file (between 1 and 3): "))
        assert name in ["1", "2", "3"], "The number of text file should be in: [1, 2, 3]"
        path = f"data/task-1/sudoku-{name}.txt"
        
        with open(path, "r", encoding = "utf-8") as handler: contents = handler.readlines()
        config = [[int(number.strip()) for number in row if number != '\n' and number != ' '] for row in contents]
        sudoku = Sudoku(config)

        method = int(input("Select a method to solve [1 -> DFS, 2 -> BFS]: "))
        if method == 1:
            print("Depth First Search")
            dfs = DepthFirstSearch(sudoku)
            (found, path) = dfs.search()

            if found == True:
                print(f"Solution found in {len(path)} computational steps")
                print(path[-1])
            else:
                print("Solution not found")

        elif method == 2:
            print("Breadth First Search")
            bfs = BreadthFirstSearch(sudoku)
            (found, path) = bfs.search()

            if found == True:
                print(f"Solution found in {len(path)} computational steps")
                print(path[-1])
            else:
                print("Solution not found")

        else:
            print("Method should be in [1 -> DFS, 2 -> BFS]")

    elif task == 2:
        print("Solving 8-Puzzle using A*")
        start  = [7, 2, 4, 5, 0, 6, 8, 3, 1] # [1, 8, 2, 7, 4, 3, 0, 6, 5] 
        target = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        start_node = Puzzle8(start, target, None, g = 0, h = 0)
        a_star = AStar(start_node)
        a_star.search()
        
    elif task == 3:
        print("Solving N-Quens using Genetic Algorithms")
        MUTATION_RATE   = 0.05
        MIXING_PARENTS  = 2

        n_queens        = int(input("Select number of queens (default should be 8): "))
        population_size = int(input("Select the size of the population (default should be 10): "))

        ga = GeneticAlgorithm(n_queens, population_size, MIXING_PARENTS, MUTATION_RATE)
        ga.run()

    elif task == 4:
        print("Solving TicTacToe using Min Max Algorithm")
        game    = TicTacToe()
        min_max = MinMaxAlgorithm()

        print(game)
        while not game.is_solution():
            human_move = int(input(f"You are X, available moves {[m + 1 for m in game.check_available_moves()]}: "))
            if human_move not in [m + 1 for m in game.check_available_moves()]:
                human_move = int(input(f"Move not available, please select one move from {[m + 1 for m in game.check_available_moves()]}: "))

            game.expand(human_move - 1, "X")
            print(game)

            if game.is_solution() == True: break

            ai_move = min_max.best_move(game, -1, "O")
            game.expand(ai_move, "O")
            print(game)

        print(f"Game Result: {game.display_winner()} won!")
    else:
        print("Invalid option, run the application with task [1: Sudoku, 2: 8-Puzzle, 3: N-Quens, 4: TicTacToe]")

