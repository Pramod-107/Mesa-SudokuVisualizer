# 🎮 Multi-Agent Sudoku Visualizer

A pure Python web application that demonstrates a **Multi-Agent System (MAS)** for generating, solving, and validating Sudoku puzzles. This project uses [Solara](https://solara.dev) for the reactive web user interface.

## ✨ Features

* **Agent-Based Architecture:** Distinct agents handle generation, validation, solving, and display logic.
* **Puzzle Generation:** Creates unique, valid Sudoku puzzles on the fly.
* **Backtracking Solver:** Visualizes the solving process algorithmically.
* **Validation:** Verifies agent moves and final board states against Sudoku rules.
* **Interactive UI:** A clean web interface to interact with the agent model.

## 🏗️ Architecture

The system is orchestrated by a central `SudokuModel` which coordinates the following agents:

| Agent | Role |
| :--- | :--- |
| **🤖 Generator Agent** | Uses randomized backtracking to create full boards and remove cells to create puzzles. |
| **🧠 Solver Agent** | Attempts to solve the puzzle using a recursive backtracking algorithm. |
| **⚖️ Validator Agent** | Enforces Sudoku rules (row, column, and 3x3 subgrid constraints). |
| **🎨 Display Agent** | Renders the state of the environment into Solara UI components. |

## 🚀 Getting Started

### Prerequisites

Ensure you have Python installed. You will need to install `solara` and `numpy`:

```bash
pip install solara numpy
