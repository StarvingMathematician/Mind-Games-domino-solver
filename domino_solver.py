'''
Created on Oct 11, 2013

@author: Jonathan Simon

Structure is based on the code found here:
https://gist.github.com/ryangomba/1724881 
'''

class Domino:
    '''
    Each domino is represented by 4 parameters:
    1) It's bottom number
    2) It's top number
    3) The value it's numbers sum to
    4) Whether it's two numbers are the same
    
    There is also a flip operation which swaps the domino's two numbers  
    '''
    
    def __init__(self, lower_num, upper_num):
        self.lower_num = lower_num
        self.upper_num = upper_num
        self.total_num = lower_num + upper_num
        self.flip_sym = lower_num == upper_num
        
    def _flip(self):
        self.lower_num, self.upper_num = self.upper_num, self.lower_num        
                
                
    ##########################################################################################
    
    
class Domino_Solver:
    
    def __init__(self, board_height, board_width, magic_number):
        self.board_height = board_height #e.g. 3
        self.board_width = board_width # e.g. 6
        self.board_size = board_height*board_width # e.g. 18
        self.magic_number = magic_number # e.g. 13
    '''    
    def _get_all_dominos(self):
        all_dominos = [Domino(i,j) for i in range(7) for j in range(i+1)]
        return all_dominos
    '''
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
        
        def _recursive_generate(amount_remaining, dominos_remaining, grouped_sums_remaining, this_subset):
            if dominos_remaining < 0:
                return []
            elif dominos_remaining == 0:
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
                        return _recursive_generate(amount_remaining - grouped_sums_remaining[0][0], dominos_remaining - 1, grouped_sums_remaining[1:], this_subset + [grouped_sums_remaining[0][0]]) + _recursive_generate(amount_remaining, dominos_remaining, grouped_sums_remaining[1:], this_subset[:])
                    else:
                        head_copy = grouped_sums_remaining[0][:]
                        head_copy[1] -= 1
                        return _recursive_generate(amount_remaining - grouped_sums_remaining[0][0], dominos_remaining - 1, [head_copy] + grouped_sums_remaining[1:], this_subset + [grouped_sums_remaining[0][0]]) + _recursive_generate(amount_remaining, dominos_remaining, grouped_sums_remaining[1:], this_subset[:])
        
        solution_blob = _recursive_generate(self.magic_number*self.board_width, self.board_size, grouped_sums, [])
        #Need to reshape solution list before returning it 
        solution_list = [solution_blob[self.board_size*i:self.board_size*(i+1)] for i in range(len(solution_blob)/self.board_size)]
        return solution_list
        
    ##########################################################################################
            
    def get_plausible_subsets(self):
        grouped_sums = self._generate_all_sums()
        unique_subsets = self._generate_unique_subsets(grouped_sums)
        
        return unique_subsets
        
    
    
    
    '''
    To save on space and time, only generate sums, not the dominos.
    We can generate a list of domino objects when they're needed.
    '''
    
    
    
    
    
    
    
    