'''
Created on Oct 11, 2013

@author: Jonathan Simon

Overall structure of the program in based on the code here:
https://gist.github.com/ryangomba/1724881 
'''

#initialize and seed a random number generator
import random
random.seed()


#########################################################################################################################


#See description below
class Domino:
    '''
    An object of class Domino represents an individual domino.
    
    Member Variables:
    'top' -- the domino's top number (Type: Int)
    'bottom' -- the domino's top number (Type: Int)
    'total' -- the sum of the domino's two numbers (Type: Int)
    'flip_sym' -- whether or not the domino's two numbers are equal (Type: Boolean)
    
    Class Methods:
    '_flip' -- flips the domino, swapping its top and bottom numbers (Input: self ; Output: nothing)
    '''
    
    #Initial Domino
    def __init__(self, top_num, bottom_num):
        self.top = top_num
        self.bottom = bottom_num
        self.total = top_num + bottom_num
        self.flip_sym = top_num == bottom_num
    
    #Flip the domino    
    def _flip(self):
        self.bottom, self.top = self.top, self.bottom        
                
                
#########################################################################################################################


#See description below
class Domino_Board:
    '''
    An object of class Domino_Board represents a particular set of dominoes laid out in a particular configuration on the game board.
    
    Member Variables:
    'board_height' -- height of the board, as measured in # of dominoes (Type: Int)
    'board_width' -- width of the board, as measured in # of dominoes; this is generally 2*board_height (Type: Int)
    'magic_number' -- the number that every row, column and diagonal is required to sum to (Type: Int)
    'domino_layout' -- how the dominoes are arranged on the board (Type: List[List[Domino]])
    
    Class Methods:
    '_get_domino_layout' -- initializes domino_layout by placing a given set of dominoes randomly on the board (Input: List[List[Int]] ; Output: List[List[Domino]])
    '_get_printable_domino_layout' -- prints domino_layout in a human-readable format (Input: self ; Output: List[List[List[Int]]])
    '_swap_dominos' -- swaps the positions of two dominoes on the board (Input: self, List[Int], List[Int] ; Output: nothing)
    '_flip_domino' -- returns 'True' and flips a particular domino if that domino is *not* flip symmetric, otherwise simply return 'False' (Input: self, List[Int] ; Output: Boolean)
    '_row_sum' -- sums the numbers in a particular row, where a row is defined by both the domino row *and* top-vs-bottom (Input: self, Int, Int ; Output: Int)
    '_col_sum' -- sums the numbers in a particular column (Input: self, Int ; Output: Int)
    '_diag_sum' -- sums the numbers in a particular diagonal, where the diagonal is specified by a binary value (Input: self, Int ; Output: Int)
    '_get_cost' -- get the total cost associated with domino_layout, where the cost is given by the sum of the absolute differences between each row/column/diagonal sum, and magic_number (Input: self ; Output: Int)
    '''
    
    #Initialize Domino Board
    def __init__(self, board_height, board_width, magic_number, num_pair_list):
        self.board_height = board_height #e.g. 3
        self.board_width = board_width # e.g. 6
        self.magic_number = magic_number # e.g. 13
        self.domino_layout = self._get_domino_layout(num_pair_list)
    
    #Initialize domino_layout
    def _get_domino_layout(self, num_pair_list):
        #Place the dominoes on the board in the order they were provided
        domino_obj_list = [Domino(*num_pair) for num_pair in num_pair_list]  
        
        random.shuffle(domino_obj_list)
        for domino in domino_obj_list: #randomly flip each domino on the board with a 50/50 probability
            if random.random() > .5:
                domino._flip()
        
        #Reshape the board
        domino_layout = [domino_obj_list[self.board_width*i:self.board_width*(i+1)] for i in range(self.board_height)]
        return domino_layout
    
    #Return domino_layout in a human-readable format 
    def _get_printable_domino_layout(self):
        return [[[self.domino_layout[row][col].top, self.domino_layout[row][col].bottom] for col in range(self.board_width)] for row in range(self.board_height)]
                
        
    #Swaps a pair of dominoes on the board
    def _swap_dominos(self, idx1, idx2):
        self.domino_layout[idx1[0]][idx1[1]], self.domino_layout[idx2[0]][idx2[1]] = self.domino_layout[idx2[0]][idx2[1]], self.domino_layout[idx1[0]][idx1[1]]
    
    #Returns 'True' and flips a domino on the board if it's *not* flip symmetric, otherwise simply return 'False'
    def _flip_domino(self,idx):
        if self.domino_layout[idx[0]][idx[1]].flip_sym == True:
            return False
        else:
            self.domino_layout[idx[0]][idx[1]]._flip()
            return True
    
    #Calculates a given row's sum. The row is identified via two values, where numbering is top to bottom:
    #'domino_row' can take values in 'range(board_height)', but 'digit_row' can only be '0' or '1' (corresponding to 'top' or 'bottom')
    def _row_sum(self, domino_row, digit_row):
        if digit_row == 0:
            return sum([self.domino_layout[domino_row][col].top for col in range(self.board_width)])
        elif digit_row == 1:
            return sum([self.domino_layout[domino_row][col].bottom for col in range(self.board_width)])
    
    #Calculates a given column's sum. Numbering is left to right, where 'col_idx' can take values in 'range(board_width)'. 
    def _col_sum(self, col_idx):
        return sum([self.domino_layout[row][col_idx].total for row in range(self.board_height)])
    
    #Calculates a given diagonal's sum. '0' denotes the main diagonal, and '1' denotes the non-main diagonal. 
    def _diag_sum(self, diag_num):
        if diag_num == 0:
            return sum([self.domino_layout[i/2][i].top if i%2==0 else self.domino_layout[(i-1)/2][i].bottom for i in range(self.board_width)])
        elif diag_num == 1:
            return sum([self.domino_layout[self.board_height-1 - i/2][i].bottom if i%2==0 else self.domino_layout[self.board_height-1 - (i-1)/2][i].top for i in range(self.board_width)])
    
    #Get the total cost of the board by summing the costs of every row, column, and diagonal.
    def _get_cost(self):
        col_cost = sum([abs(self.magic_number - self._col_sum(i)) for i in range(self.board_width)]) 
        row_cost = sum([abs(self.magic_number - self._row_sum(i,j)) for j in [0,1] for i in range(self.board_height)])
        diag_cost = abs(self.magic_number - self._diag_sum(0)) + abs(self.magic_number - self._diag_sum(1))
        return col_cost + row_cost + diag_cost

    
#########################################################################################################################


# Domino_Solver solves the problem of identifying a particular subset of dominoes (Part 1), and then 
# arranging then on a board in such a way that all rows, columns and diagonals sum to the same value (Part 2).
# This dual-purpose means that 'board_height', 'board_width' and 'magic_number' must exist as members 
# of both Domino_Solver *and* Domino_Board. This repetition is ugly, but necessary.
class Domino_Solver:
    '''
    An object of class Domino_Solver solves the domino puzzle in two parts:
    1) Identify every domino subset which satisfies a certain necessary condition for being a solution set.
       The problem of finding these subsets is similar to certain knapsack-type problems, and can likewise be solved with a recursive algorithm. 
    2) Using one of the domino subsets identified in (1), find an arrangement of its constituent dominoes
       satisfying the puzzle's summation criteria. We use a simulated annealing scheme to find such an arrangement.  
    
    Member Variables:
    'board_height' -- height of the board, as measured in # of dominoes (Type: Int)
    'board_width' -- width of the board, as measured in # of dominoes; this is generally 2*board_height (Type: Int)
    'board_size' -- the total number of dominoes on the board; this is the product of 'board_height' and 'board_width' (Type: Int)
    'magic_number' -- the number that every row, column and diagonal is required to sum to (Type: Int)
    
    Class Methods:
    Part 1:
    '_generate_all_sums' -- returns a list of the sums of the top/bottom numbers for each domino (Input: self ; Output: List[List[Int]])
    '_generate_unique_subsets' -- returns a list of all lists of domino sums satisfying the condition that the constituent domino sums sum to 'board_width * magic_number' (Input: self, List[List[Int]]; Output: List[List[Int]])
    'get_plausible_subsets' -- runs '_generate_all_sums' and '_generate_unique_subsets', and returns the list of sum-sets (Input: self, Output: List[List[Int]])
    Part 2:
    '_get_neighboring_state' -- gets a neighboring board configuration state by randomly either flipping a domino, or swapping two dominoes (Input: self, Domino_Board ; Output: nothing)
    '_get_init_temp' -- finds the initial temperature for the SA algorithm by calling '_get_neighboring_state' several times, and calculating the standard deviation of the resulting costs (Input: self, Domino_Board ; Output: nothing)  
    'run_SA' -- runs the SA algorithm until a solution is found, or max_steps is exceeded; returns information about the algorithm's progress, and about the cost and form of the best solution (Input: self, List[List[Int]] ; Output: Int, List[List[List[Int]]], List[Int], List[List[Int]])
    '''
    
    #Initialize Domino_Solver
    def __init__(self, board_height, board_width, magic_number):
        self.board_height = board_height #e.g. 3
        self.board_width = board_width # e.g. 6
        self.board_size = board_height*board_width # e.g. 18
        self.magic_number = magic_number # e.g. 13
    
    
    ##############################
    ######## Part 1 Setup ########
    ##############################
    
    
    #Generate a list of all top/bottom domino sums
    def _generate_all_sums(self):
        all_sums = []
        for i in range(7):
            for j in range(i+1):
                all_sums.append(i+j)
        #Turn the list of domino sums into a list of pairs [sum, count] where 'count' is the number of times 'sum' appeared
        grouped_sums = [[n,all_sums.count(n)] for n in range(13)]
        grouped_sums.reverse()
        return grouped_sums
    
    #Find all domino sum lists which satisfy the condition that all of the numbers of all of the dominoes sum to 'board_width * magic_number' 
    def _generate_unique_subsets(self,grouped_sums):
        
        # Solve the problem recursively by accumulating numbers until:
        # 1) We've hit the max accumulation size, but our sum is wrong (return empty list)
        # 1) Our sum is too high (return empty list)
        # 2) We run out of numbers to pull from (return empty list) (return empty list)
        # 3) We actually find a solution (return solution)
        # By the nature of the recursion, we examine all possible numerical combinations. However, since the solutions we find
        # get concatenated together via the '+' operator, we'll need to split them back up again after the function execution is over.
        def _recursive_generate(amount_remaining, dominoes_remaining, grouped_sums_remaining, this_subset):
            if dominoes_remaining == 0:
                if amount_remaining == 0: #found a solution!
                    return this_subset
                else: #total sum is too low
                    return []
            else:
                if (amount_remaining < 0) or (len(grouped_sums_remaining) == 0): #either sum is too high, or we prematurely ran out of dominoes
                    return []
                else: #recursion step
                    if grouped_sums_remaining[0][1] == 1: #remove the head [sum, count] pair altogether (occurs when count == 1)
                        return _recursive_generate(amount_remaining - grouped_sums_remaining[0][0], dominoes_remaining - 1, grouped_sums_remaining[1:], this_subset + [grouped_sums_remaining[0][0]]) + _recursive_generate(amount_remaining, dominoes_remaining, grouped_sums_remaining[1:], this_subset[:])
                    else: #decrement the head sum's count (occurs when count > 1)
                        head_copy = grouped_sums_remaining[0][:]
                        head_copy[1] -= 1
                        return _recursive_generate(amount_remaining - grouped_sums_remaining[0][0], dominoes_remaining - 1, [head_copy] + grouped_sums_remaining[1:], this_subset + [grouped_sums_remaining[0][0]]) + _recursive_generate(amount_remaining, dominoes_remaining, grouped_sums_remaining[1:], this_subset[:])
        
        solution_blob = _recursive_generate(self.magic_number*self.board_width, self.board_size, grouped_sums, []) #call the recursive function
        solution_list = [solution_blob[self.board_size*i:self.board_size*(i+1)] for i in range(len(solution_blob)/self.board_size)] #reshape the solution list
        return solution_list
        
        
    ##################################
    ######## Part 1 Execution ########
    ##################################
            
    
    # Callable method which returns all domino sum-sets satisfying the condition that their elements sum to 'board_width * magic_number'   
    def get_plausible_subsets(self):
        grouped_sums = self._generate_all_sums()
        unique_subsets = self._generate_unique_subsets(grouped_sums)
        
        return unique_subsets
        
        
    ##############################
    ######## Part 2 Setup ########
    ##############################
    
    
    # Find a board which is a neighbor to the current one by randomly performing a (nontrivial) domino flip, or a (nontrivial) domino swap.
    # The odds of performing a flip vs a swap are proportion to the number of possibilities for each, namely 'board_size' vs '(board_size choose 2)'
    # Once an operation has been chosen, a random domino or pair of dominoes in chosen to perform it on.      
    def _get_neighboring_state(self, This_Board):
        if random.uniform(0, self.board_size + (self.board_size * (self.board_size-1)) / 2) > self.board_size: #perform swap
            idx1 = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
            idx2 = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
            while idx1 == idx2: #make sure we've chosen two different dominoes
                idx2 = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
            This_Board._swap_dominos(idx1, idx2)
        else:
            idx = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
            while not This_Board._flip_domino(idx): #make sure our domino is *not* flip symmetric 
                idx = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
    
    # Find the initial temperature for the SA algorithm. This technique is discussed in the paper "Metaheuristics can Solve Sudoku Puzzles".
    def _get_init_temp(self, This_Board, num_steps):
        from numpy import zeros, std
        cost_arr = zeros(num_steps)
        for n in range(num_steps):
            cost_arr[n] = This_Board._get_cost()
            self._get_neighboring_state(This_Board)
        return std(cost_arr)


    ##################################
    ######## Part 2 Execution ########
    ##################################
    
    
    # Run the simulated annealing algorithm (without reheating). It returns the best solution found,
    # either when that solution is optimal, or when the maximum number of iterations has been reached.
    def run_SA(self, num_pair_list):
        from copy import deepcopy
        from math import exp
        
        This_Board = Domino_Board(self.board_height, self.board_width, self.magic_number, num_pair_list) #initialize the board
        cooling_rate = .98 # <-- parameter value used in my solution
        mdp_length = self.board_size ** 2 # value taken from the paper "Metaheuristics can Solve Sudoku Puzzles"
        temp = self._get_init_temp(This_Board, mdp_length) # initialize the temperature; using 'mdp_length' here was largely arbitrary
        max_steps = mdp_length*200 # <-- parameter value used in my solution
        
        best_cost = curr_cost = This_Board._get_cost()
        best_layout = deepcopy(This_Board.domino_layout)
        best_list = [[0, best_cost]]
        cost_list = [curr_cost]
        step_num = 0
        
        # Continue looping so long as the solution is nonoptimal, and we haven't exceeded the maximum allowered number of iterations
        while best_cost > 0 and step_num < max_steps:
            step_num += 1
            Prev_Board = deepcopy(This_Board)
            self._get_neighboring_state(This_Board)
            curr_cost = This_Board._get_cost()
            cost_diff = curr_cost - Prev_Board._get_cost()
            
            # Change states if the cost of the new board is better, or if a certain temperature-dependent probabalistic condition is met   
            if cost_diff < 0 or random.random() < exp(-cost_diff / temp):
                if curr_cost < best_cost:
                    best_cost = curr_cost
                    best_layout = This_Board._get_printable_domino_layout()
                    best_list.append([step_num,best_cost])
            else:
                This_Board = Prev_Board
            
            cost_list.append(curr_cost)
            if step_num % mdp_length == 0: #update the temperature periodically 
                temp *= cooling_rate
                if (step_num / mdp_length) % 10 == 0: #inform the user of the algorithm's progress
                    print "Done with loop number", step_num / mdp_length
        
        return best_cost, best_layout, cost_list, best_list
    