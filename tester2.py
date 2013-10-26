'''
Created on Oct 23, 2013

@author: Macbook
'''

from domino_solver import Domino_Solver
from time import time

if __name__ == '__main__':
    
    '''
    #.017sec
    level1 = Domino_Solver(2, 4, 6) #board height, board width, magic number
    
    startTime = time()
    solution_set = level1.get_plausible_subsets()
    timeElapsed = time()-startTime
    
    print solution_set
    print len(solution_set)
    print len(solution_set)/8
    print timeElapsed
    '''
    
    #2.2sec
    level2 = Domino_Solver(3, 6, 13) #board height, board width, magic number
    
    startTime = time()
    solution_set = level2.get_plausible_subsets()
    timeElapsed = time()-startTime
    
    for sol in solution_set:
        print sol
    print len(solution_set)
    print timeElapsed
    
    #Corresponding to the sum list [7 7 7 6 6 6 6 5 5 4 4 4 3 3 2 2 1 0] (skipping [0,5]):
    domino_list = [[1,6],[2,5],[3,4],[0,6],[1,5],[2,4],[3,3],[1,4],[2,3],[0,4],[1,3],[2,2],[0,3],[1,2],[0,2],[1,1],[0,1],[0,0]]
    min_solution = level2.run_SA(domino_list)