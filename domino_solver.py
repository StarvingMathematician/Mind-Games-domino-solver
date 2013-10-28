'''
Created on Oct 11, 2013

@author: Jonathan Simon

Structure is based on the code found here:
https://gist.github.com/ryangomba/1724881 
'''

import random

class Domino:
    '''
    Each domino is represented by 4 parameters:
    1) It's bottom number
    2) It's top number
    3) The value it's numbers sum to
    4) Whether it's two numbers are the same
    
    There is also a flip operation which swaps the domino's two numbers  
    '''
    
    def __init__(self, bottom_num, top_num):
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
        
        random.seed()
        random.shuffle(domino_obj_list)
        for domino in domino_obj_list:
            if random.random() > .5:
                domino._flip()
        
        #Reshape the board
        domino_layout = [domino_obj_list[self.board_width*i:self.board_width*(i+1)] for i in range(self.board_height)]
        return domino_layout
    
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
    
    #Consider flip symmetry to be irrelevant. If we perform a trivial flip, then so be it.
    #def _flip_domino(self,idx):
    #    self.domino_layout[idx[0]][idx[1]]._flip()
        
    #Numbering is top to bottom: 'domino_row' goes up to 'board_height', but 'digit_row' can only be 0 or 1 (for 'top' or 'bottom')
    def _row_sum(self, domino_row, digit_row):
        if digit_row == 0:
            return sum([self.domino_layout[domino_row][col].top for col in self.board_width])
        elif digit_row == 1:
            return sum([self.domino_layout[domino_row][col].bottom for col in self.board_width])
    
    #Numbering is left to right
    def _column_sum(self, col_idx):
        return sum([self.domino_layout[row][col_idx].total for row in self.board_height])
    
    #diag_num == 0 --> main diag, diag_num == 1 --> other diag 
    def _diag_sum(self, diag_num):
        if diag_num == 0:
            return sum([self.domino_layout[i/2][i].top if i%2==0 else self.domino_layout[(i-1)/2][i].bottom for i in range(self.board_width)])
        elif diag_num == 1:
            return sum([self.domino_layout[self.board_height-1 - i/2][i].bottom if i%2==0 else self.domino_layout[self.board_height-1 - (i-1)/2][i].top for i in range(self.board_width)])
    
    def _get_cost(self):
        col_cost = sum([abs(self.magic_number - self._col_sum(i)) for i in range(self.board_width)]) 
        row_cost = sum([abs(self.magic_number - self._row_sum(i,j)) for j in [0,1] for i in range(self.board_height)])
        diag_cost = abs(self.magic_number - self.diag_sum(0)) + abs(self.magic_number - self.diag_sum(1))
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
    def _get_neighboring_state(self):
        random.seed()
        if random.uniform(0, self.board_size + (self.board_size * (self.board_size-1)) / 2) > self.board_size: #perform swap
            idx1 = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
            idx2 = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
            while idx1 == idx2:
                idx2 = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
            self.This_Board._swap_dominos(idx1, idx2)
        else:
            idx = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
            while not self.This_Board._flip_domino(idx): #recall that if the domino is flip symmetric, then 'flip_domino' simply returns 'False' 
                idx = [random.randint(0,self.board_height - 1),random.randint(0,self.board_width - 1)]
        
    def _get_init_temp(self, num_steps):
        

    ##########################################################################################
            
    def run_SA(self, num_pair_list):
        self.This_Board = Domino_Board(self.board_height, self.board_width, self.magic_number, num_pair_list)
        cooling_rate = .99
        mdp_length = self.board_size ** 2 #consider changing this value to something more meaningful
        temp = self._get_init_temp(mdp_length) #I can choose this value more intelligently later, if I want
        
        
    
    
    
    
    
    
    
    
    