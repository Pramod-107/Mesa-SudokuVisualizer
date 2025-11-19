# 🎮 Multi-Agent Sudoku Visualizer

A pure Python web application that demonstrates a **Multi-Agent System (MAS)** for generating, solving, and validating Sudoku puzzles. This project uses [Solara](https://solara.dev) for a reactive, component-based web user interface.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Solara](https://img.shields.io/badge/UI-Solara-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

## ✨ Features

* **Agent-Based Architecture:** Distinct agents handle generation, validation, solving, and display logic.
* **Puzzle Generation:** Creates unique, valid Sudoku puzzles on the fly using randomized backtracking.
* **Visual Solver:** Watch the *Solver Agent* attempt to solve the puzzle in real-time.
* **Validation:** Verifies agent moves and final board states against standard Sudoku rules.
* **Interactive UI:** A clean, browser-based interface to interact with the agent model.

## 🏗️ Architecture

The system is orchestrated by a central `SudokuModel` which coordinates the following agents:

| Agent | Role |
| :--- | :--- |
| **🤖 Generator Agent** | Generates a full valid board and removes cells to create a playable puzzle. |
| **🧠 Solver Agent** | Attempts to solve the puzzle using a recursive backtracking algorithm. |
| **⚖️ Validator Agent** | Enforces Sudoku rules (row, column, and 3x3 subgrid constraints). |
| **🎨 Display Agent** | Renders the state of the environment into Solara UI components. |

## 🚀 Getting Started

### Prerequisites

Ensure you have Python installed. You will need to install the following dependencies:

```bash
pip install solara numpy
