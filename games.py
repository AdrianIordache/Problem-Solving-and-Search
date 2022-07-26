from utils import *

class Sudoku(State):
    def __init__(self, initial_config: List[List[int]] = None):
        self.config = initial_config
        self.rows = self.columns = 9

    def __eq__(self, other: State):
        if isinstance(other, Sudoku): return self.config == other.config
        return self.config == other

    def __str__(self) -> str:
        text = ""
        text += "-" * 37 + '\n'
        for row in range(self.rows):
            text += "| "
            for column in range(self.columns):
                text += f"{self.config[row][column]} | "
            text += "\n"
            text += "-" * 37 + '\n'

        return text

    def is_solution(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.config[row][column] == 0:
                    return False
        return True

    def expand(self):
        def find_empty_space(self) -> Tuple[int, int]:
            row, column = None, None
            for r in range(self.rows):
                for c in range(self.columns):
                    if self.config[r][c] == 0:
                        row    = r 
                        column = c

            return row, column

        def valid_row(self, row: int, value: int) -> bool:
            for c in range(self.columns):
                if self.config[row][c] == value: return False

            return True 

        def valid_column(self, column: int, value: int) -> bool:
            for r in range(self.rows):
                if self.config[r][column] == value: return False

            return True

        def valid_square(self, row: int, column: int, value: int) -> bool:
            r_square = (row    // 3) * 3
            c_square = (column // 3) * 3
            
            for r in range(r_square, r_square + 3):
                for c in range(c_square, c_square + 3):
                    if self.config[r][c] == value:
                        return False

            return True

        possible_configs = []
        r, c = find_empty_space(self)
        for value in range(1, 10):
            if valid_row(self, r, value) and \
                valid_column(self, c, value) and \
                valid_square(self, r, c, value):
                    config = copy.deepcopy(self.config)
                    config[r][c] = value
                    possible_configs.append(Sudoku(config))

        return possible_configs


class Puzzle8(State):
    def __init__(self, initial_config: List[int], objective: List[int], parent: List[int] = None, g: int = 0, h: int = 0):
        self.config    = initial_config
        self.objective = objective
        self.parent    = parent

        self.columns   = self.rows = 3
        
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def __str__(self):
        string = '+---+---+---+\n'
        for r in range(self.rows):
            for c in range(self.columns):
                tile = self.config[r * 3 + c]
                string = string + '| {} '.format(' ' if tile == '0' else tile)
            string = string + '|\n'
            string = string + '+---+---+---+\n'
        return string

    def __gt__(self, other: State):
        if self.g > other.g: return True
        return False

    def __eq__(self, other: State):
        if isinstance(other, Puzzle8): return self.config == other.config
        return self.config == other

    def is_solution(self):
        return self.config == self.objective

    def expand(self):
        def manhattan_distance(self, value: int, objective: List[int], i: int, j: int):
            found_idx = objective.index(value)
            i_elem    = found_idx // self.rows
            j_elem    = found_idx %  self.columns
            distance  = np.abs(i_elem - i) + np.abs(j_elem - j)
            return distance

        def swap(self, i: int, j: int):
            config = copy.deepcopy(self.config)
            config[i], config[j] = config[j], config[i]
            return config

        def compute_heuristics(self, config: List[int]):
            heuristic = 0
            for idx in range(len(config)):
                i_elem     = idx // self.rows
                j_elem     = idx %  self.columns
                heuristic += manhattan_distance(self, self.config[idx], self.objective, i_elem, j_elem)
            return heuristic

        empty_idx = self.config.index(0)
        empty_row = empty_idx // self.rows
        empty_col = empty_idx %  self.columns

        possible_configs = []
        if empty_row > 0:
            move   =  (empty_row - 1) * self.rows + empty_col 
            config = swap(self, empty_idx, move)
            metric = compute_heuristics(self, config)
            possible_configs.append(Puzzle8(config, self.objective, self, g = self.g + 1, h = metric))
        if empty_row < 2:
            move   = (empty_row + 1) * self.rows + empty_col
            config = swap(self, empty_idx, move)
            metric = compute_heuristics(self, config)
            possible_configs.append(Puzzle8(config, self.objective, self, g = self.g + 1, h = metric))
        if empty_col > 0:
            move   = empty_row * self.rows + (empty_col - 1)
            config = swap(self, empty_idx, move)
            metric = compute_heuristics(self, config)
            possible_configs.append(Puzzle8(config, self.objective, self, g = self.g + 1, h = metric))
        if empty_col < 2:
            move   = empty_row * self.rows + (empty_col + 1)
            config = swap(self, empty_idx, move)
            metric = compute_heuristics(self, config)
            possible_configs.append(Puzzle8(config, self.objective, self, g = self.g + 1, h = metric))

        return possible_configs

class NQueens(State):
    def __init__(self, n_queens: int = 8, individual: List[int] = None):
        self.n_queens = n_queens
        
        if individual == None:
            self.individual = self.expand()
        else: 
            self.individual = individual

    def __eq__(self, other: State):
        if isinstance(other, NQueens): return self.individual == other.individual
        return self.individual == other    

    def __len__(self):
        return self.n_queens

    def __str__(self):
        text = ""
        for row in range(self.n_queens):
            queen = self.individual[row]
            for column in range(self.n_queens):
                if column == queen:
                    text += '[Q]'
                else:
                    text += '[ ]'
            text += '\n'
        return text

    def get_genes(self, begin: int, end: int):
        return self.individual[begin : end]

    def set_genes(self, idx: int, value: int):
        self.individual[idx] = value

    def expand(self):
        return [random.randrange(self.n_queens) for _ in range(self.n_queens)]

    def fitness_score(self):
        score = 0
        for gene_idx, gene in enumerate(self.individual):
            for other_gene_idx, other_gene in enumerate(self.individual):
                # on each column can be only one queen
                if gene_idx == other_gene_idx: 
                    continue
                # on each row can be only one queen
                if other_gene == gene: 
                    continue
                # diagonal conditions for queens
                if other_gene_idx + other_gene == gene_idx + gene:
                    continue
                if other_gene_idx - other_gene == gene_idx - gene:
                    continue

                score += 1

        # divide by 2 as pairs of queens are commutative
        return score / 2

    def is_solution(self):
        score = self.fitness_score()
        if score == sc.comb(self.n_queens, 2):  # number of combinations of N things taken k at a time
            return True

        return False


class TicTacToe(State):
    def __init__(self):
        self.board = [" ", " ", " ",
                      " ", " ", " ",
                      " ", " ", " "]

        self.final_states = (
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        )

    def __str__(self):
        return """
        -------------
        | {} | {} | {} |
        -------------
        | {} | {} | {} |
        -------------
        | {} | {} | {} |
        -------------
        """.format(*self.board)

    def __eq__(self, other: State):
        if isinstance(other, TicTacToe): return self.board == other.board
        return self.board == other    

    def check_player_moves(self, player: str):
        return [idx for idx, position in enumerate(self.board) if player == position]

    def check_available_moves(self):
        return [idx for idx, position in enumerate(self.board) if position == " "]

    def check_board_state(self):
        for player in ("X", "O"):
            player_positions = self.check_player_moves(player)

            for combo in self.final_states:
                if set(combo).issubset(player_positions):
                    return player

        return None

    def is_solution(self):
        if self.check_board_state() != None: return True
        if " " in self.board: return False
        return True

    def expand(self, position: int, player: str):
        self.board[position] = player

    def display_winner(self): 
        if self.check_board_state() == "X":
            return "X"
        elif self.check_board_state() == "O":
            return "O"
        elif self.is_solution() == True:
            return "Nobody"