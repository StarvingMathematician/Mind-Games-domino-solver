Mind-Games-domino-solver
========================

Solves the "Domino 2" level (seen [here](http://youtu.be/azF2lZjlScw)) from the Android puzzle app "Mind Games". The goal of the game is to fill the board on the left with dominoes from the right such that all rows, columns, and diagonals sum to 13. (Although the program was designed with this particular board size/summation value in mind, it works for other values of these parameters as well.)

The algorithm operates in two parts:

1. "get_plausible_subsets": Finds all subsets of the 28 dominoes which could plausibly meet the required summation criteria. Note that these sets only meet certain *necessary* criteria which are not gauranteed to be suffient to yield a solution. This step decreases the number of subsets we need to consider from (28 choose 18) = 1.3e7 to only 48.
2. "run_SA": Using one of the domino subsets found in step (1), run a simulated annealing schedule on the domino configuration such that at each time step either a single domino gets flipped, or two dominoes have their positions swapped. This tranforms the problem from a brute-force examination of all 18!*2^18 = 1.7e21 states, into a guided traversal of the state-space graph whose diameter is only (18 choose 2) + 18 = 171. This approach was inspired by the paper ("Metaheuristics can Solve Sudoku Puzzles")[http://www.inf.utfsm.cl/~mcriff/Tesistas/Games/sudoku.pdf].

The functions described above are found in the file "domino_solver.py", and a sample execution of this code is found in "tester2.py". Because I was interested in the behavior of the SA algorithm, I ran the code twice, producing two different solutions. The specifics of these solutions are found in the below files, where the solution number ('1' or '2') goes where the asterisk is:
- "Solution_Output*.txt" -- what gets printed to the screen after "tester2.py" is run
- "Successful_Level_2_Solution*.txt" -- a graph showing the progress of the algorithm; the current cost is shown in blue, and the best cost up to that point is shown in red
- "best_list*.txt" -- the best cost values that were found over the course of the algorithm's execution
- "cost_list*.txt" -- the cost at any given step in the algorithm's execution
