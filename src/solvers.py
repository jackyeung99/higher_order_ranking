import random 
from .syntetic import * 



'''
 ==================== Ranking Workflow ====================

'''

def synch_solve_equations (bond_matrix, max_iter, pi_values, method = 'newman', sens=1e-6):
    
    
#     print('Method ', method)
    
    x, y, z = [], [], []
    
    
    scores = {}
#     for n in bond_matrix:
    for n in pi_values:
        # scores[n] = random.random()
        scores[n] = float(np.exp(logistic.rvs(size=1)))
        # scores[n] = 1.0
        # scores[n] = pi_values[n]
        # if n not in bond_matrix:
        #     bond_matrix[n] = {}
    normalize_scores (scores)
    
    list_of_nodes = list(scores.keys())
    
    
    err = 1.0
    rms = N = 0.0
    for n in scores:
        if n != 'f_p':
            N += 1.0
            rms += (scores[n]-pi_values[n])*(scores[n]-pi_values[n])
    rms = np.sqrt(rms/N)

    x.append(0)
    y.append(rms)
    z.append(err)
    
    

    
    iteration = 0
    while iteration < max_iter and err > sens:
        
        err = 0.0
        tmp_scores = {}
        
        for s in scores:
            
            if method == 'zermelo':
                tmp_scores[s] = iterate_equation_zermelo_new (s, scores, bond_matrix)
            if method == 'newman':
                tmp_scores[s] = iterate_equation_newman (s, scores, bond_matrix)
            if method == 'newman_leadership':
                tmp_scores[s] = iterate_equation_newman_leadership (s, scores, bond_matrix)
                            
        normalize_scores (tmp_scores)
        
        
        
        
        
        for s in tmp_scores:
            if abs(tmp_scores[s]-scores[s]) > err:
                err = abs(tmp_scores[s]-scores[s])
            scores[s] = tmp_scores[s]

                                
        iteration += 1
        
        rms = N = 0.0
        for n in scores:
            N += 1.0
            rms += (scores[n]-pi_values[n])*(scores[n]-pi_values[n])
        rms = np.sqrt(rms/N)

        x.append(iteration)
        y.append(rms)
        z.append(err)
        
        
            
    return scores, [x, y, z]

def solve_equations (bond_matrix, max_iter, pi_values, method = 'newman', sens=1e-6):

    ''' 
    Offline/asynchronous iterative method:
    update rankings of players in batchs
    '''


    x, y, z = [], [], []


    scores = {}
    for n in bond_matrix:
        scores[n] = random.random()
        normalize_scores (scores)


    list_of_nodes = list(scores.keys())


    err = 1.0
    rms = N = 0.0
    for n in scores:
        N += 1.0
        rms += (scores[n]-pi_values[n])*(scores[n]-pi_values[n])
    rms = np.sqrt(rms/N)

    x.append(0)
    y.append(rms)
    z.append(err)



    iteration = 0
    while iteration < max_iter and err > sens:

        err = 0.0

        for n in range(0, len(scores)):

            s = random.choice(list_of_nodes)

            old = scores[s]

            if method == 'zermelo':
                scores[s] = iterate_equation_zermelo_new (s, scores, bond_matrix)
            if method == 'newman':
                scores[s] = iterate_equation_newman (s, scores, bond_matrix)
            if method == 'newman_leadership':
                scores[s] = iterate_equation_newman_leadership (s, scores, bond_matrix)





            normalize_scores (scores)

            if abs(old-scores[s]) > err:
                err = abs(old-scores[s])




        iteration += 1

        rms = N = 0.0
        for n in scores:
            N += 1.0
            rms += (scores[n]-pi_values[n])*(scores[n]-pi_values[n])
        rms = np.sqrt(rms/N)

        x.append(iteration)
        y.append(rms)
        z.append(err)



    return scores, [x, y, z]




''' 
==================== ranking algorithms ====================
algorithms to develop rankings iteratively
'''

def point_wise_ranking(players, games):
    scores = {k: 0 for k in range(len(players))}
    num_games = {k: 0 for k in range(len(players))}
    
    for game in games:
        num_players = len(game)
        for idx, player in enumerate(game):
            num_games[player] += 1
            scores[player] += (num_players - idx) / num_players

    final_scores = {player: (scores[player] / num_games[player]) if num_games[player] > 0 else 0 for player in scores}

    return final_scores



def iterate_equation_zermelo (s, scores, bond_matrix):


    #a = b = 0.0

    ##prior
    a = 1.0
    b = 2.0/(scores[s]+1.0)

    for K in bond_matrix[s]:



        for r in bond_matrix[s][K]:


            if r < K-1:
                a += len(bond_matrix[s][K][r])

                for t in range(0, len(bond_matrix[s][K][r])):
                    tmp = 0.0
                    for q in range(r, K):
                        tmp += scores[bond_matrix[s][K][r][t][q]]
                    b += 1.0 / tmp


            for t in range(0, len(bond_matrix[s][K][r])):
                for v in range(0, r):
                    tmp = 0.0
                    for q in range(v, K):
                        tmp += scores[bond_matrix[s][K][r][t][q]]
                    b += 1.0 / tmp
#                     print ('> ', tmp)


#             for t in range(0, len(bond_matrix[s][K][r])):
#                 tmp = 0.0
#                 for q in range(0, K):
#                     tmp += scores[bond_matrix[s][K][r][t][q]]
#                 b += 1.0 / tmp
#                 print ('>> ', tmp)
#                 for q in range(0, r-1):
#                     tmp = tmp - scores[bond_matrix[s][K][r][t][q]]
#                     print ('>> ', tmp)
#                     b += 1.0 / tmp


    return a/b



def iterate_equation_zermelo_new (s, scores, bond_matrix):


    #a = b = 0.0

    ##prior
    a = 1.0
    b = 2.0/(scores[s]+1.0)

    for K in bond_matrix[s]:



        for r in bond_matrix[s][K]:



            a += len(bond_matrix[s][K][r])



            for t in range(0, len(bond_matrix[s][K][r])):
                for v in range(0, r+1):
                    tmp = 0.0
                    for q in range(v, K):
                        tmp += scores[bond_matrix[s][K][r][t][q]]
                    b += 1.0 / tmp


    return a/b




def iterate_equation_newman (s, scores, bond_matrix):



    ##prior
    a = b = 1.0 / (scores[s]+1.0)
    if s in bond_matrix:

      for K in bond_matrix[s]:


          for r in bond_matrix[s][K]:


              if r < K-1:

                  for t in range(0, len(bond_matrix[s][K][r])):
                      tmp1 = tmp2 =  0.0
                      for q in range(r, K):
                          if q > r:
                              tmp1 += scores[bond_matrix[s][K][r][t][q]]
                          tmp2 += scores[bond_matrix[s][K][r][t][q]]

                      a += tmp1/tmp2


              for t in range(0, len(bond_matrix[s][K][r])):
                  for v in range(0, r):
                      tmp = 0.0
                      for q in range(v, K):
                          tmp += scores[bond_matrix[s][K][r][t][q]]
                      b += 1.0 / tmp

  #             for t in range(0, len(bond_matrix[s][K][r])):
  #                 tmp = 0.0
  #                 for q in range(0, K):
  #                     tmp += scores[bond_matrix[s][K][r][t][q]]
  #                 b += 1.0 / tmp
  #                 for q in range(0, r-1):
  #                     tmp = tmp - scores[bond_matrix[s][K][r][t][q]]
  #                     b += 1.0 / tmp



    return a/b



def iterate_equation_newman_leadership (s, scores, bond_matrix):

    
    
    ##prior
    a = b = 1.0 / (scores[s]+1.0)
    if s in bond_matrix:

        for K in bond_matrix[s]:
            
    #         print (bond_matrix[s][K])
            

            for r in bond_matrix[s][K]:
                
                
                if r == 0:
                    
    #                 print (bond_matrix[s][K][r])
                    
                    for t in range(0, len(bond_matrix[s][K][r])):
                        tmp1 = tmp2 =  0.0
                        for q in range(0, K):
                            if q>0:
                                tmp1 += scores[bond_matrix[s][K][r][t][q]]
                            tmp2 += scores[bond_matrix[s][K][r][t][q]]

                        a += tmp1/tmp2
                    
                

                else:
                    for t in range(0, len(bond_matrix[s][K][r])):
                        tmp = 0.0
                        for q in range(0, K): 
                            tmp += scores[bond_matrix[s][K][r][t][q]]
                        b += 1.0 / tmp

    return a/b

