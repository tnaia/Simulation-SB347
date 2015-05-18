# coding: utf-8
#
# Simulating SB347 populations
# ----------------------------
#
# Date: 09/02/2015
# Authors: Sophie Tandonnet and Tassio Naia
#
# Description:
# This python script takes the output of the processing script 
# "setting_bars.pde" (rate of offspring production, Sequential 
# order of female, hermaphrodite and male production) and calculates
# for each time t the number of adult males, females and hermaphrodites
#
# last modified: 16/05/2015
#


import sys, getopt
   
try:
  opts, args = getopt.getopt(sys.argv[1:],"af:h:g:i:",["help","Frate=", "Hrate=", "SexProportionF=", "SexProportionH="])
except getopt.GetoptError:
  print('simulation-SB347.py -f <rate of female offspring production> -h <rate of hermaphrodite offspring production> -g <file of proportion of each gender by females> -i <file of proportion of each gender by hermaphrodite>')
  sys.exit(2)

if len(sys.argv) < 2:
    print('USAGE: simulation-SB347.py -f <rate of female offspring production> -h <rate of hermaphrodite offspring production> -g <file of proportion of each gender by females> -i <file of proportion of each gender by hermaphrodite>')
    sys.exit()


# Parse command line options
# ==========================

for opt, arg in opts:
  if opt == '-a':
     print('simulation-SB347.py -f <rate of female offspring production> -h <rate of hermaphrodite offspring production> -g <file of proportion of each gender by females> -i <file of proportion of each gender by hermaphrodite')
     sys.exit()
  elif opt in ("-f", "--Frate"):
     Frate = arg
  elif opt in ("-h", "--Hrate"):
     Hrate = arg
  elif opt in ("-g", "--SexProportionF"):
     SexProportionF = arg
  elif opt in ("-i", "--SexProportionH"):
     SexProportionH = arg
  else:
     print('simulation-SB347.py -f <rate of female offspring production> -h <rate of hermaphrodite offspring production> -g <file of proportion of each gender by females> -i <file of proportion of each gender by hermaphrodite>')
     sys.exit()

###############################################
# Functions to transform input files in lists #
###############################################


def prod_rate(rate_file_name):
    '''this function reads a rate file line by line. 
    A rate file is a one column file where each line 
    corresponds to a rate of offspring production (float between 0 and 1). 
    The function returns a list of rates (number of eggs/time unit) where each index of the list corresponds 
    to a time point and each value at an index corresponds to the number of 
    offspring produced at that particular time.'''
    rate_file = open(rate_file_name)
    total_prod_rate = []
    for line in rate_file:
        line = line.rstrip()
        total_prod_rate += [int(float(line) * 50)] # 50 was chosen because it makes a good conversion between the number of individuals per time interval and a number between 0 and 1
     
    rate_file.close()  
    return total_prod_rate
    


def sex_proportions(proportions_file_name, rate_file_name):
    '''This function runs the previous function prod_rate on the rate_file_name
    and reads a proportions file. Each line of the proportion file consists of 
    three comma separated floats taking values between 0 and 1. They corespond, 
    respectively, to the proportions of males, females and hermaphrodites). 
    There are as many lines as time points.
    The function sex_proportions multiplies the rate of production by each gender 
    proportion for each time point. This results in a list of lists where each 
    sublist corresponds to a time point of the reproductive life and contains the 
    number of males, females and hermaphrodites (in this order)'''
    
    proportions_file = open(proportions_file_name)
    prodRate = prod_rate(rate_file_name)
    
    gender_prodRate = []
    line_counter = -1    
    for line in proportions_file:
        line_counter += 1
        comma_indexes = []
        i=0
        while i < len(line):
            if line[i] == ',': 
                comma_indexes += [i]
            i += 1
        
        Male_proportion = int(float(line[0:comma_indexes[0]]) * prodRate[line_counter])
        Female_proportion = int(float(line[comma_indexes[0]+1:comma_indexes[1]])*prodRate[line_counter]) #* prod_rate(rate_file)[line_counter]
        Hermaphrodite_proportion = int(float(line[comma_indexes[1]+1:]) * prodRate[line_counter])
    
        gender_prodRate += [[Male_proportion,Female_proportion,Hermaphrodite_proportion]]
        
    proportions_file.close()
        
    return gender_prodRate
            
####################
# Initial settings #
####################

day_time_points = 3 #population monitored every 8h, therefore 3 times in a day


# Hermaphrodite settings
# ----------------------

H_larval_time = 3 * day_time_points # Time period where the hermaphrodite is a larvae (3days)
H_adult_time = 5*day_time_points+1 # Time period where the hermaphrodite is reproducing (5days and 8h)
lifespanH = H_larval_time + H_adult_time # Total lifespan of a hermaphrodite (from egg to end of reproduction)

time_before_dauer = 2 * day_time_points # Time of egg + L1 + L2 (2 days)
time_of_L4 = 1
time_after_dauer = time_of_L4 + H_adult_time

# Female settings
# ---------------

F_larval_time = 2 * day_time_points + 1 # Time period where the female is a larvae (2days and 8h)
F_adult_time = 5*day_time_points+1 # Time period where the hermaphrodite is reproducing (5 days and 8 hours (=1 time point))
lifespanF = F_larval_time + F_adult_time # Total lifespan of a hermaphrodite (from egg to end of reproduction)

# Male settings
# -------------

M_larval_time = 2 * day_time_points+1 # Time period where the male is a larvae (2days and 8h)
M_adult_time = 5*day_time_points +1 # Time period where the male is reproducing (5 days and 8 hours (=1 time point))
lifespanM = M_larval_time + M_adult_time # Total lifespan of a male (from egg to end of reproduction)


# initial population
# ------------------

# The population starts with 1 dauer larvae that arrive in an optimal environment (abundance of food)

N_fem = [0]*lifespanF # Number of females at every unit of time (index of the list) of their life. At the begining of the simulation there are no females.
N_mal = [0]*lifespanM # Number of males at every unit of time. At the begining of the simulation there are no males.
N_her = [0]*time_before_dauer + [0] + [1] + [0]*time_after_dauer # Number of hermaphrodites at every unit of time. The simulation begins with one dauer larvae (hermaphrodite-fated).The [0] and [1] represent the dauer larvae time (16h).

# Assert: Testing if the hermaphrodite lifespan in the same in the lists "lifespanH" (initial settings) and "N_her" (initial population)

if len(N_her) != lifespanH: print("Length of hermaphrodite list N_her different from hermaphrodite lifespan")


# Number of offspring of each gender produced at each time point by females and hermaphrodites
# --------------------------------------------------------------------------------------------

# The order in the sublists is: [males,females,hermaphrodite]
# Prepending zeros to production rate vector as larvas do not reproduce

fem_prodRate = [[0,0,0]]*F_larval_time+sex_proportions(SexProportionF, Frate)
her_prodRate = [[0,0,0]]*H_larval_time+sex_proportions(SexProportionH, Hrate)

#EXAMPLE: her_prodRate = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[40,80,40],[20,80,80],[20,80,200],[15,40,100],[10,15,70],[5,5,50],[0,25,15]]
#EXAMPLE: fem_prodRate = [[0,0,0],[0,0,0],[0,0,0],[30,30,70],[20,20,150],[10,10,200],[5,5,200],[2,2,80],[2,2,50],[0,0,40]]

# Storing the length of the previous vectors (which represent the total units of time ie, the lifespan)
# -----------------------------------------------------------------------------------------------------

L_fem = len(N_fem)
L_her = len(N_her)
L_mal = len(N_mal)


# header of output
# ----------------

print('#M','#F','#H','%M','%F','%H', sep="\t")

#####################################################################
# Simulating the growth of the population from the initial settings #
#####################################################################

# Number of units of time to run the program 
# ------------------------------------------

N_iterations = 102 # each iteration corresponds to 8h. One day is therefore 3 iterations. 102 iterations = 34 days.
current_iteration = 0

while current_iteration < N_iterations:

# initializing result vectors (number of individual at each age). Their length is the lifespan of each sex.

    N_fem_res = [0]*L_fem
    N_her_res = [0]*L_her
    N_mal_res = [0]*L_mal
    
# Time passes -> individuals age and are passed in the following index of the list
    
    for i in range(1,L_fem):
        N_fem_res[i] = N_fem[i-1]
        
    for i in range(1,L_mal):
        N_mal_res[i] = N_mal[i-1]
        
    for i in range(1,L_her):
        N_her_res[i] = N_her[i-1] 

# Adult females and hermaphrodites produce eggs: We add eggs (index 0) according to the rate of production of each gender and age
    i = 0
    while i < L_fem:
        N_fem_res[0] += N_fem[i]*fem_prodRate[i][1]
        N_her_res[0] += N_fem[i]*fem_prodRate[i][2]
        N_mal_res[0] += N_fem[i]*fem_prodRate[i][0]
        i += 1
      
    i = 0     
    while i < L_her:
        N_fem_res[0] += N_her[i]*her_prodRate[i][1]
        N_her_res[0] += N_her[i]*her_prodRate[i][2]
        N_mal_res[0] += N_her[i]*her_prodRate[i][0]
        i += 1

# update population
                       
    N_fem = N_fem_res
    N_her = N_her_res 
    N_mal = N_mal_res 


# Total number of adults

    Total_Afem = sum(N_fem[F_larval_time+1:])
    Total_Aher = sum(N_her[H_larval_time+1:])
    Total_Amal = sum(N_mal[M_larval_time+1:])
    
    result_A = [Total_Amal,Total_Afem,Total_Aher]
    total_A = sum(result_A)


# Total number of individuals of each gender

    Total_fem = sum(N_fem)
    Total_her = sum(N_her)
    Total_mal =sum(N_mal)
    
    result = [Total_mal,Total_fem,Total_her]
    total = sum(result)  
    
# Total number of individuals of each gender

    L1_fem = sum(N_fem[1:2])
    L1_her = sum(N_her[1:2])
    L1_mal =sum(N_mal[1:2])
    
    result_L1 = [L1_mal,L1_fem,L1_her]
    total_L1 = sum(result_L1)    
    
# Choosing population for output (Adults or mixed individuals)

    population_output = result
    total_population_output = total

    if total_population_output != 0:
        proportion = [x * 100/total_population_output for x in population_output]
    else:
        proportion = [0,0,0]
        
# print result to Standard output

    print(population_output[0] , population_output[1] , population_output[2] , proportion[0] , proportion[1] , proportion[2] , sep="\t")
    
    current_iteration += 1
    

