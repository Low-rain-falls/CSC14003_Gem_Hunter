# Gem Hunter

## Introduction

**Gem Hunter** is an Artificial Intelligence problem that involves solving the task of finding gems on a grid map. The grid consists of various types of cells: traps (T), numbers indicating the count of traps around the cell, empty cells, and gems (G). The challenge is to determine the locations of the gems by translating the map into Conjunctive Normal Form (CNF) and solving it using different SAT-solving algorithms.

### Algorithms used in this project

- **PySAT**: Solves the problem using SAT solvers from the `pysat` library.
- **Brute-force**: Exhaustively checks all possible configurations.
- **Backtracking**: Attempts to find a solution by trying possibilities and backtracking when a solution fails.
- **DPLL**: A more efficient SAT-solving algorithm based on the Davis-Putnam-Logemann-Loveland procedure.

## Project Structure

The project is organized as follows:

```
Gem Hunter/
│
├── algorithm
│   ├── backtracking.py         # Backtracking algorithm
│   ├── bruteforce.py           # Brute-force algorithm
│   ├── CNF.py                  # Converts map to CNF form
│   ├── pysat.py                # Solves using the PySAT library
│   └── solvers.py              # Contains generic solver functions
├── main.py                     # Main program to run the algorithms (DPLL is called here)
├── table.py                    # Manages the grid map
└── Utils
    ├── filehandle.py           # File input/output handling
    └── helper.py               # Helper functions for auxiliary tasks
```

## Installation

To run the project, you can set up the required environment using **Conda** or **Pip**. Follow the instructions below for each method.

### 1. Installation with Conda

If you're using **Conda**, you can create a virtual environment and install the required libraries as follows:

1. **Create a new Conda environment**:

   ```bash
   conda create -n gem_hunter python=3.11
   ```

2. **Activate the environment**:

   ```bash
   conda activate gem_hunter
   ```

3. **Install required libraries**:

   - Install `pysat` from Conda:

     ```bash
     conda install -c conda-forge pysat
     ```

   - If you need additional libraries like `itertools`, you can install them using `pip`:

     ```bash
     pip install itertools
     ```

4. After installing the libraries, you can run the scripts in the project.

### 2. Installation with Pip

If you prefer **Pip**, you can install the libraries as follows:

1. **Create and activate a virtual environment** (optional, but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

2. **Install the required libraries**:

   ```bash
   pip install pysat
   pip install itertools
   ```

   Alternatively, you can use the provided `requirements.txt` file to install all dependencies at once:

   ```bash
   pip install -r requirements.txt
   ```

   **requirements.txt**:

   ```txt
   pysat
   python-sat
   itertools
   ```

### 3. Additional Libraries (for Conda users)

For **Conda** users, some libraries like `pysat` may not be available by default in Conda repositories. You can install them using `pip` after setting up the Conda environment.

## Running the Program

Once the environment is set up and the required libraries are installed, you can run the program using:

```bash
python main.py
```

### Input and Output

- **Input**: The program will read the map from the files located in the `testcases/` directory (e.g., `input_1.txt`, `input_2.txt`, etc.).
- **Output**: The results will be written to `output.txt`, which will indicate the discovered locations of the gems.

---

## Algorithms

### 1. **PySAT Algorithm**

The `PySAT` algorithm uses the `pysat` library to solve the problem by encoding it as a SAT problem. It utilizes advanced SAT solvers to efficiently find solutions to the gem-hunting problem.

### 2. **Brute-force Algorithm**

The brute-force algorithm explores all possible configurations, checking each one to see if it satisfies the constraints of the problem. While it guarantees a solution, it is computationally expensive for larger grids.

### 3. **Backtracking Algorithm**

Backtracking is a more intelligent approach, where the algorithm searches for a solution by incrementally building up possibilities and backtracks when an invalid solution path is encountered.

### 4. **DPLL Algorithm**

The **DPLL (Davis-Putnam-Logemann-Loveland)** algorithm is an optimization of the SAT-solving process. It uses efficient techniques such as unit propagation and variable elimination to improve performance compared to brute-force methods.

---

## Files in the Project

- **`main.py`**: The main program that orchestrates the execution of different algorithms. The DPLL algorithm is implemented and invoked here.
- **`algorithm/`**: This directory contains various algorithms, such as backtracking, brute-force, pysat, and CNF generation.
- **`Utils/`**: A folder for utility functions, such as file I/O handling and other helper functions.

---

## Development Guide

### Adding New Algorithms

If you'd like to add new algorithms, simply create a new Python file in the `algorithm/` directory. Then, you can integrate it into `main.py` by importing the appropriate functions.

### Improving the User Interface

Currently, the program runs in the command line. If desired, you could create a graphical user interface (GUI) to enhance user interaction. Consider using frameworks like `Tkinter` or `PyQt` for a GUI.

---
