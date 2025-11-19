import solara
import random
import copy
import numpy as np

# ---------------- ENVIRONMENT ---------------- #
class SudokuEnvironment:
    """Holds Sudoku puzzle, solution, and solving state."""
    def __init__(self):
        self.puzzle = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.solving_board = [[0 for _ in range(9)] for _ in range(9)]


# ---------------- BASE AGENT ---------------- #
class Agent:
    """Base class for all agents."""
    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.status = "Idle"

    def log(self, msg):
        print(f"[{self.name}] {msg}")


# ---------------- GENERATOR AGENT ---------------- #
class GeneratorAgent(Agent):
    """Generates a random Sudoku puzzle."""
    def __init__(self, model):
        super().__init__("Generator Agent", model)

    def step(self):
        self.status = "Working"
        self.log("Generating Sudoku puzzle...")

        full = self.generate_full_board()
        puzzle = self.make_puzzle(copy.deepcopy(full))

        env = self.model.environment
        env.solution = full
        env.puzzle = puzzle
        env.solving_board = copy.deepcopy(puzzle)

        self.status = "Complete"
        self.log("Puzzle generated!")

    def generate_full_board(self):
        """Fill board completely using backtracking."""
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill(board)
        return board

    def fill(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for val in nums:
                        if self.valid(board, val, i, j):
                            board[i][j] = val
                            if self.fill(board):
                                return True
                            board[i][j] = 0
                    return False
        return True

    def make_puzzle(self, board):
        cells = random.randint(40, 50)
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        for i, j in positions[:cells]:
            board[i][j] = 0
        return board

    def valid(self, board, val, r, c):
        block_r, block_c = 3 * (r // 3), 3 * (c // 3)
        if any(board[r][x] == val for x in range(9)): return False
        if any(board[x][c] == val for x in range(9)): return False
        for i in range(block_r, block_r + 3):
            for j in range(block_c, block_c + 3):
                if board[i][j] == val: return False
        return True


# ---------------- VALIDATOR AGENT ---------------- #
class ValidatorAgent(Agent):
    """Validates Sudoku cells and full board."""
    def __init__(self, model):
        super().__init__("Validator Agent", model)

    def valid(self, board, val, r, c):
        block_r, block_c = 3 * (r // 3), 3 * (c // 3)
        if any(board[r][x] == val for x in range(9)): return False
        if any(board[x][c] == val for x in range(9)): return False
        for i in range(block_r, block_r + 3):
            for j in range(block_c, block_c + 3):
                if board[i][j] == val: return False
        return True

    def verify(self, board):
        for i in range(9):
            if sorted(board[i]) != list(range(1, 10)): return False
        for j in range(9):
            if sorted([board[i][j] for i in range(9)]) != list(range(1, 10)): return False
        return True


# ---------------- SOLVER AGENT ---------------- #
class SolverAgent(Agent):
    """Solves Sudoku puzzles using backtracking."""
    def __init__(self, model):
        super().__init__("Solver Agent", model)

    def step(self):
        env = self.model.environment
        validator = self.model.validator

        self.status = "Working"
        self.log("Solving puzzle...")
        board = copy.deepcopy(env.solving_board)

        if self.solve(board, validator):
            env.solving_board = board
            self.status = "Complete"
            self.log("Solved!")
        else:
            self.status = "Failed"
            self.log("No solution found.")

    def solve(self, board, validator):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for val in range(1, 10):
                        if validator.valid(board, val, i, j):
                            board[i][j] = val
                            self.model.refresh()
                            if self.solve(board, validator):
                                return True
                            board[i][j] = 0
                            self.model.refresh()
                    return False
        return True


# ---------------- DISPLAY AGENT (via Solara) ---------------- #
class DisplayAgent(Agent):
    """Handles Sudoku board visualization in Solara."""
    def __init__(self, model):
        super().__init__("Display Agent", model)

    def board_component(self, board, title):
        """Render Sudoku board as grid."""
        return solara.Column([
            solara.Text(title, style="font-weight:bold; font-size:20px; margin:5px;"),
            solara.Grid(
                [[
                    solara.Text(
                        str(board[i][j]) if board[i][j] != 0 else "·",
                        style=f"font-size:20px; text-align:center; width:25px; height:25px; "
                              f"border:1px solid #999; padding:3px; color:{'black' if board[i][j] != 0 else '#bbb'};"
                    )
                    for j in range(9)
                ] for i in range(9)]
            )
        ])


# ---------------- MAIN MODEL ---------------- #
class SudokuModel:
    """Coordinates all agents and Solara updates."""
    def __init__(self):
        self.environment = SudokuEnvironment()
        self.generator = GeneratorAgent(self)
        self.validator = ValidatorAgent(self)
        self.solver = SolverAgent(self)
        self.display = DisplayAgent(self)
        self.refresh_callback = None  # link to solara UI

    def refresh(self):
        if self.refresh_callback:
            self.refresh_callback()

    def generate(self):
        self.generator.step()
        self.refresh()

    def solve(self):
        self.solver.step()
        self.refresh()

    def verify(self):
        valid = self.validator.verify(self.environment.solving_board)
        self.refresh()
        return valid


# ---------------- SOLARA UI ---------------- #
@solara.component
def Page():
    model = solara.use_state(SudokuModel())[0]
    rerender = solara.use_reactive(0)
    model.refresh_callback = lambda: rerender.set(rerender.value + 1)

    def handle_generate():
        model.generate()

    def handle_solve():
        model.solve()

    def handle_verify():
        result = model.verify()
        solara.notify(f"✅ Solution valid!" if result else "❌ Invalid solution!")

    env = model.environment

    return solara.Column(
        gap="20px",
        align_items="center",
        children=[
            solara.Text("🎮 Multi-Agent Sudoku System", style="font-size:24px; font-weight:bold;"),
            solara.Button("Generate Puzzle", on_click=handle_generate),
            solara.Button("Solve Puzzle", on_click=handle_solve),
            solara.Button("Verify Solution", on_click=handle_verify),
            solara.Row([
                model.display.board_component(env.puzzle, "Generated Puzzle"),
                model.display.board_component(env.solving_board, "Solved Puzzle"),
            ]),
        ]
    )


# To run: `solara run sudoku_app.py`
