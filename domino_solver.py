'''
Created on Oct 11, 2013

@author: Jonathan Simon

Structure is based on the code found here:
https://gist.github.com/ryangomba/1724881 
'''

import random
random.seed()

class Domino:
    '''
    Each domino is represented by 4 parameters:
    1) It's bottom number
    2) It's top number
    3) The value it's numbers sum to
    4) Whether it's two numbers are the same
    
    There is also a flip operation which swaps the domino's two numbers  
    '''
    
    def __init__(self, top_num, bottom_num):
        self.top = top_num
        self.bottom = bottom_num
        self.total = top_num + bottom_num
        self.flip_sym = top_num == bottom_num
        
    def _flip(self):
        self.bottom, self.top = self.top, self.bottom        
                
                
    ##########################################################################################


#Domino_Board shares attributes (width/height) with Domino_Solver. This isn't ideal, but I'll leave it for now. 
class Domino_Board:
    '''
    Denotes the board_heightxboard_width board of dominoes which sum to magic_number
    '''
    def __init__(self, board_height, board_width, magic_number, num_pair_list):
        self.board_height = board_height #e.g. 3
        self.board_width = board_width # e.g. 6
        self.magic_number = magic_number # e.g. 13
        self.domino_layout = self._get_domino_layout(num_pair_list)
    
    def _get_domino_layout(self, num_pair_list):
        domino_obj_list = [Domino(*num_pair) for num_pair in num_pair_list]
        
        random.shuffle(domino_obj_list)
        for domino in domino_obj_list:
            if random.random() > .5:
                domino._flip()
        
        #Reshape the board
        domino_layout = [domino_obj_list[self.board_width*i:self.board_width*(i+1)] for i in range(self.board_height)]
        return domino_layout
    
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
    
    #Numbering is top to bottom: 'domino_row' goes up to 'board_height', but 'digit_row' can only be 0 or 1 (for 'top' or 'bottom')
    def _row_sum(self, domino_row, digit_row):
        if digit_row == 0:
            return sum([self.domino_layout[domino_row][col].top for col in range(self.board_width)])
        elif digit_row == 1:
            return sum([self.domino_layout[domino_row][col].bottom for col in range(self.board_width)])
    
    #Numbering is left to right
    def _col_sum(self, col_idx):
        return sum([self.domino_layout[row][col_idx].total for row in range(self.board_height)])
    
    #diag_num == 0 --> main diag, diag_num == 1 --> other diag 
    def _diag_sum(self, diag_num):
        if diag_num == 0:
            return sum([self.domino_layout[i/2][i].top if i%2==0 else self.domino_layout[(i-1)/2][i].bottom for i in range(self.board_width)])
        elif diag_num == 1:
            return sum([self.domino_layout[self.board_height-1 - i/2][i].bottom if i%2==0 else self.domino_layout[self.board_height-1 - (i-1)/2][i].top for i in range(self.board_width)])
    
    def _get_cost(self):
        col_cost = sum([abs(self.magic_number - self._col_sum(i)) for i in range(self.board_width)]) 
        row_cost = sum([abs(self.magic_number - self._row_sum(i,j)) for j in [0,1] for i in range(self.board_height)])
        diag_cost = abs(self.magic_number - self._diag_sum(0)) + abs(self.magic_number - self._diag_sum(1))
        return col_cost + row_cost + diag_cost
    
    
class Domino_Solver:
    
    def __init__(self, board_height, board_width, magic_number):
        self.board_height = board_height #e.g. 3
        self.board_width = board_width # e.g. 6
        self.board_size = board_height*board_width # e.g. 18
        self.magic_number = magic_number # e.g. 13
    
    ##########################################################################################
    
    def _generate_all_sums(self):
        all_sums = []
        for i in range(7):
            for j in range(i+1):
                all_sums.append(i+j)
        grouped_sums = [[n,all_sums.count(n)] for n in range(13)]
        grouped_sums.reverse()
        return grouped_sums
    
    def _generate_unique_subsets(self,grouped_sums):
        
        def _recursive_generate(amount_remaining, dominoes_remaining, grouped_sums_remaining, this_subset):
            if dominoes_remaining < 0:
                return []
            elif dominoes_remaining == 0:
                if amount_remaining == 0:
                    return this_subset
                else:
                    return []
            else:
                if (amount_remaining < 0) or (len(grouped_sums_remaining) == 0):
                    return []
                else: #note that this '+' operator concatenates the lists, so you'll need to split them back up afterwards
                    # Only difference between this cases is whether we reduce the front element freq by 1 (which requires making a deep copy), or remove it altogether.
                    # Note that reducing the frequency only makes sense to do if the freq is >1
                    if grouped_sums_remaining[0][1] == 1:
                        return _recursive_generate(amount_remaining - grouped_sums_remaining[0][0], dominoes_remaining - 1, grouped_sums_remaining[1:], this_subset + [grouped_sums_remaining[0][0]]) + _recursive_generate(amount_remaining, dominoes_remaining, grouped_sums_remaining[1:], this_subset[:])
                    else:
                        head_copy = grouped_sums_remaining[0][:]
                        head_copy[1] -= 1
                        return _recursive_generate(amount_remaining - grouped_sums_remaining[0][0], dominoes_remaining - 1, [head_copy] + grouped_sums_remaining[1:], this_subset + [grouped_sums_remaining[0][0]]) + _recursive_generate(amount_remaining, dominoes_remaining, grouped_sums_remaining[1:], this_subset[:])
        
        solution_blob = _recursive_generate(self.magic_number*self.board_width, self.board_size, grouped_sums, [])
        #Need to reshape solution list before returning it 
        solution_list = [solution_blob[self.board_size*i:self.board_size*(i+1)] for i in range(len(solution_blob)/self.board_size)]
        return solution_list
        
    ##########################################################################################
            
    def get_plausible_subsets(self):
        grouped_sums = self._generate_all_sums()
        unique_subsets = self._generate_unique_subsets(grouped_sums)
        
        return unique_subsets
        
    ##########################################################################################
    
    #First decide whether we're going to flip or swap, and then choose random domino(es) to do it to
    #I will probably NOT want add a 'trade' option, since that undermines the nature of the Domino_Board object
    #
    #The probability of swap vs flip should correspond to the number of unique ways in which they can occur.
    #That is, swap is proportional to '(size choose 2)', and flip is proportional to 'size'
    #Thus, we choose a random number in the range [0, size + (size choose 2)], and swap if it's > n, and flip otherwise  
    def _get_neighboring_state(self, This_Board):
        if random.uniform(0, self.board_size + (self.board_size * (self.board_size-1)) / 2) > self.board_size: #perform swap
            idx1 = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
            idx2 = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
            while idx1 == idx2:
                idx2 = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
            This_Board._swap_dominos(idx1, idx2)
        else:
            idx = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
            while not This_Board._flip_domino(idx): #recall that if the domino is flip symmetric, then 'flip_domino' simply returns 'False' 
                idx = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
        
    def _get_init_temp(self, This_Board, num_steps):
        from numpy import zeros, std
        cost_arr = zeros(num_steps)
        for n in range(num_steps):
            cost_arr[n] = This_Board._get_cost()
            self._get_neighboring_state(This_Board)
        return std(cost_arr)

    ##########################################################################################
            
    def run_SA(self, num_pair_list):
        from copy import deepcopy
        from math import exp
        
        This_Board = Domino_Board(self.board_height, self.board_width, self.magic_number, num_pair_list)
        cooling_rate = .98 # <-- solution parameter value
        mdp_length = self.board_size ** 2 #consider changing this value to something more meaningful
        temp = self._get_init_temp(This_Board, mdp_length) #I can choose this value more intelligently later, if I want
        
        best_cost = curr_cost = This_Board._get_cost()
        best_layout = deepcopy(This_Board.domino_layout)
        best_list = [[0, best_cost]]
        
        max_steps = mdp_length*200 # <-- solution parameter value
        cost_list = [curr_cost]
        step_num = 0
        
        #no reheating
        while best_cost > 0 and step_num < max_steps:
            step_num += 1
            Prev_Board = deepcopy(This_Board)
            self._get_neighboring_state(This_Board)
            curr_cost = This_Board._get_cost()
            cost_diff = curr_cost - Prev_Board._get_cost()
            
            if cost_diff < 0 or random.random() < exp(-cost_diff / temp): #if the cost of the new board is better, or tunneling occurs
                if curr_cost < best_cost:
                    best_cost = curr_cost
                    best_layout = This_Board._get_printable_domino_layout()
                    best_list.append([step_num,curr_cost])
            else:
                This_Board = Prev_Board
            
            cost_list.append(curr_cost)
            if step_num % mdp_length == 0:
                temp *= cooling_rate
                if (step_num / mdp_length) % 10 == 0:
                    print "Done with loop number", step_num / mdp_length
        
        return best_cost, best_layout, cost_list, best_list
 
    