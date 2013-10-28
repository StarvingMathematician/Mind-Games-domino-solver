'''
Created on Oct 23, 2013

@author: Macbook
'''

from domino_solver import Domino_Solver
from time import time

if __name__ == '__main__':
    
    '''
    #.017sec
    Level_1 = Domino_Solver(2, 4, 6) #board height, board width, magic number
    
    startTime = time()
    solution_set = Level_1.get_plausible_subsets()
    timeElapsed = time()-startTime
    
    print solution_set
    print len(solution_set)
    print len(solution_set)/8
    print timeElapsed
    '''
    
    '''
    #2.2sec
    Level_2 = Domino_Solver(3, 6, 13) #board height, board width, magic number
    
    startTime = time()
    solution_set = Level_2.get_plausible_subsets()
    timeElapsed = time()-startTime
    
    for sol in solution_set:
        print sol
    print len(solution_set)
    print timeElapsed
    
    #Corresponding to the sum list [7 7 7 6 6 6 6 5 5 4 4 4 3 3 2 2 1 0] (skipping [0,5]):
    domino_list = [[1,6],[2,5],[3,4],[0,6],[1,5],[2,4],[3,3],[1,4],[2,3],[0,4],[1,3],[2,2],[0,3],[1,2],[0,2],[1,1],[0,1],[0,0]]
    min_solution = Level_2.run_SA(domino_list)
    '''
    
    # Takes .2sec simply to initialize the problem. Not a good sign...
    Level_2 = Domino_Solver(3, 6, 13) #board height, board width, magic number
    
    #Corresponding to the sum list [7 7 7 6 6 6 6 5 5 4 4 4 3 3 2 2 1 0] (skipping [0,5]):
    domino_list = [[1,6],[2,5],[3,4],[0,6],[1,5],[2,4],[3,3],[1,4],[2,3],[0,4],[1,3],[2,2],[0,3],[1,2],[0,2],[1,1],[0,1],[0,0]]
    startTime = time()
    best_cost, best_layout, cost_list, best_list = Level_2.run_SA(domino_list) #min_solution = Level_2.run_SA(domino_list)
    timeElapsed = time()-startTime
    print "Time Elapsed:", timeElapsed
    
    print "Best Cost:", best_cost
    print "Best Layout:"
    for row in best_layout:
        print row
    
    filename1 = "/Users/Macbook/Documents/Git_Repos/Mind-Games-domino-solver/cost_list.txt"
    f1 = open(filename1, 'w')
    for i1, cost in enumerate(cost_list):
        f1.write("%s," % i1)
        f1.write("%s\n" % cost)
    f1.close()
    
    filename2 = "/Users/Macbook/Documents/Git_Repos/Mind-Games-domino-solver/best_list.txt"
    f2 = open(filename2, 'w')
    for i2, best in best_list:
        f2.write("%s," % i2)
        f2.write("%s\n" % best)
    f2.close()
  
    import matplotlib.pyplot as plt
    best_idx, best_val = zip(*best_list)
    plt.plot(cost_list, 'b', best_idx, best_val, 'r')
    plt.show()
    
    
    
    
    
    