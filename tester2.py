'''
Created on Oct 23, 2013

@author: Jonathan Simon
'''

from domino_solver import Domino_Solver
from time import time

if __name__ == '__main__':
    
    # First find those subsets of the 28 dominoes which could plausibly be arranged into a solution.
    # Plausibility is defined as meeting the necessary (but not necessarily sufficient) condition that
    # the sum of all of the numbers on all of the dominoes = board_width * magic_number.
    
    Level_2 = Domino_Solver(3, 6, 13) #the solver is initialized with the variables representing board height, board width, and magic number
    solution_set = Level_2.get_plausible_subsets() #the plausible subsets are returned as a list of lists of individual domino sums 
    # Print all of the plausible domino sum-sets. Note that a single sum-set typically corresponds to multiple domino subsets.
    # In this case there are only 4 unique sum-sets, but 48 unique subsets (one arrives at this value of 48 can by working through come elementary combinatorics) 
    for sol in solution_set:
        print sol
    
    # We must now choose a particular domino set to feed into the SA algorithm.
    # We decided to choose the domino set from the 48 which minimized the maximum value within any given domino.
    # This corresponded to one of the three subsets associated with the sum-set: [7 7 7 6 6 6 6 5 5 4 4 4 3 3 2 2 1 0]
    # (See "Level 2 Analysis.txt" for additional details)
    domino_list = [[1,6],[2,5],[3,4],[0,6],[1,5],[2,4],[3,3],[1,4],[2,3],[0,4],[1,3],[2,2],[0,3],[1,2],[0,2],[1,1],[0,1],[0,0]]
    startTime = time() #start timer at beginning of SA algorithm
    best_cost, best_layout, cost_list, best_list = Level_2.run_SA(domino_list)
    timeElapsed = time()-startTime #record how long the entire SA scheme took
    print "Time Elapsed:", timeElapsed #print amount of time SA took to complete
    
    print "Best Cost:", best_cost #print the cost of the best solution (cost = 0 --> solution found)
    print "Best Layout:" #print the domino configuration corresponding to the best solution
    for row in best_layout:
        print row
    
    #Save the cost at each step to a text file 
    filename1 = "/Users/Macbook/Documents/Git_Repos/Mind-Games-domino-solver/cost_list.txt"
    f1 = open(filename1, 'w')
    for i1, cost in enumerate(cost_list):
        f1.write("%s," % i1)
        f1.write("%s\n" % cost)
    f1.close()
    
    #Save progression of best costs to a text file, along with the step that each occurred at
    filename2 = "/Users/Macbook/Documents/Git_Repos/Mind-Games-domino-solver/best_list.txt"
    f2 = open(filename2, 'w')
    for i2, best in best_list:
        f2.write("%s," % i2)
        f2.write("%s\n" % best)
    f2.close()
    