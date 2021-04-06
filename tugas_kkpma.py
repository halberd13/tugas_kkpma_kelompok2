import math
import random as rd
import numpy as np


def nilaiFitness(population):
  sumFitness = 0
  for i in range(len(population)):
    # print(population[i])
    sumFitness += population[i]["totalFitness"] 
  
  for i in range(len(population)):
    population[i]["percentOfFitness"] = population[i]["totalFitness"] / sumFitness * 100
  
  return population

def generateChromosome(popSize, population):
  totalError = 0
  totalFitness = 0
  totalIndividu = len(covidSummaryPerDays)
  
  
  for i in range(popSize):
    individu = []
    fitness = 0
    a = rd.random()
    b = rd.random()
    c = rd.random()
    for j in range(len(covidSummaryPerDays)):
      kromosom = {}
      if j > 2 :
        currentDay = j
        #formula using multilinear regression
        #kt=a*kt-1+b*kt-2+c
        predictValue = a*covidSummaryPerDays[j-1]+b*covidSummaryPerDays[j-2]+c
        errorValue = abs(covidSummaryPerDays[currentDay]-predictValue/(covidSummaryPerDays[currentDay]+0.01)) #DITAMBAH 0.01 SUPAYA UNTUK MENGATASI ADA PERTAMBAHAN PER HARI YANG 0
        actualValue = covidSummaryPerDays[currentDay]
        fitness = 1/errorValue
        totalError += errorValue
        totalFitness += fitness 
        kromosom = {
            "day" : currentDay,
            "predictValue" : predictValue,
            "actualValue" : covidSummaryPerDays[currentDay],
            "errorValue" : errorValue,
            "fitness" : fitness
        }
        individu.append(kromosom)
    #append individu to population
    # population.append({ "individu-"+str(i):individu, "totalFitness" : totalFitness, "a":a, "b":b, "c":c })
    population.append({"key":i, "individu-"+str(i):individu, "totalFitness" : totalFitness, "a":a, "b":b, "c":c })
    
  #count fitness value each individu
  population = nilaiFitness(population)
    
  # population = sorted(population, key=lambda x: int(x['percentOfFitness']), reverse=True)
  return population

def rouletWheelSelection(popSize, population, pC):
  totalSelectedIndividu = round(popSize * pC)
  selectedIndividu = []
  population = sorted(population, key=lambda x: int(x['percentOfFitness']), reverse=True)
  areaRoulet = []
  indexArea = 0
  lastValue = 0

  for j in range(len(population)):
    if indexArea == 0 :
      population[j]["start"] = 0
      population[j]["end"] = population[j]["percentOfFitness"]
    else:
      population[j]["start"] = population[j-1]["end"]
      population[j]["end"] = population[j-1]["end"] + population[j]["percentOfFitness"]
    indexArea +=1

  # put some random value to rouletwheel
  # print("population after roulet " , population)
  for i in range(len(population)):
    rouletArea = rd.randrange(1, 100)
    # print(rouletArea)
    if rouletArea > population[i]["start"] and rouletArea < population[i]["end"]:
      # selectedIndividu.append(population[i])
      selectedIndividu.append(population[i])     
  
  return selectedIndividu


def crossOver(parents):
  if len(parents) == 1 :
    return parents
  else:
    # get the best fitness to be a parents 
    sorted(parents, key=lambda x: int(x['percentOfFitness']), reverse=True)
    #cut point crossover in threshold a
    tmp1_a = parents[0]["a"]
    tmp2_a = parents[1]["a"] 
    #change value index 0 of a to index 1 to a
    parents[0]["a"] = tmp2_a
    parents[1]["a"] = tmp1_a
     
  return parents

def mutation(parents, pM, lenghtOfchromosome):
  resultMutation = []
  genomeSize = len(parents)*lenghtOfchromosome
  totalPM = round(pM * genomeSize)
  locateMutation = rd.randrange(0, len(parents)) 
  if len(parents)==1:
    a = rd.random()
    parents[0]["a"] = a
  else:
    for i in range(totalPM):
      locateMutation = rd.randrange(0, len(parents))
      randValueOfMutate = rd.random() 
      if locateMutation % len(parents) == 0:
        parents[locateMutation]["a"] = randValueOfMutate
      else:
        parents[locateMutation]["b"] = randValueOfMutate
  
  return parents

def updateGeneration(population, offspring):
  sorted(population, key=lambda x: int(x['percentOfFitness']), reverse=True)
  
  lengthOfPopulation = len(population)-1
  lengthOfSpring = len(offspring)
  #replace all individu that not survive with offspring
  for i in range(len(offspring)):
    population[lengthOfPopulation]["a"] = offspring[i]["a"]
    population[lengthOfPopulation]["b"] = offspring[i]["b"]
    population[lengthOfPopulation]["c"] = offspring[i]["c"]
    totalError = 0
    totalFitness = 0
    individu = population[lengthOfPopulation]["individu-"+str(lengthOfPopulation)]
    
    #re-calculate index for the new fitness value  
    for j in range(len(individu)):
      currentDay = individu[j]["day"]
      predictValue = offspring[i]["a"]*covidSummaryPerDays[currentDay-1]+offspring[i]["b"]*covidSummaryPerDays[currentDay-2]+offspring[i]["c"]
      errorValue = abs(covidSummaryPerDays[currentDay]-predictValue/(covidSummaryPerDays[currentDay]+0.01)) 
      actualValue = covidSummaryPerDays[currentDay]
      fitness = 1/errorValue
      totalError += errorValue
      totalFitness += fitness 
      individu[j]["predictValue"] = predictValue
      individu[j]["actualValue"] = actualValue
      individu[j]["errorValue"] = errorValue
      individu[j]["fitness"] = fitness
      
    #put again individu into population after update chromosome   
    population[lengthOfPopulation]["individu-"+str(lengthOfPopulation)] = individu      
    lengthOfPopulation-=1

  #re-calculate fitness funct   
  population = nilaiFitness(population)
  return population
#50 hari pertama 
covidSummaryPerDays = {
    1 :	2,
    2 :	2,
    3 :	2,
    4 :	2,
    5 :	4,
    6 :	4,
    7 :	6,
    8 :	19,
    9 :	27,
    10 :	34,
    11 :	69,
    12 :	96,
    13 :	117,
    14 :	134,
    15 :	172,
    16 :	227,
    17 :	309,
    18 :	369,
    19 :	450,
    20 :	514,
    21 :	579,
    22 :	685,
    23 :	790,
    24 :	893,
    25 :	1046,
    26 :	1155,
    27 :	1285,
    28 :	1414,
    29 :	1528,
    30 :	1677,
    31 :	1790,
    32 :	1986,
    33 :	2092,
    34 :	2273,
    35 :	2491,
    36 :	2738,
    37 :	2956,
    38 :	3293,
    39 :	3512,
    40 :	3842,
    41 :	4241,
    42 :	4557,
    43 :	4839,
    44 :	5136,
    45 :	5516,
    46 :	5923,
    47 :	6248,
    48 :	6575,
    49 :	6760,
    50 :	7135,
}

lenghtOfchromosome = 3
popSize = 10
generation = 10
population = []
#Probability Crossover
pC = 0.8
#Probability Mutation
pM = 0.1 


# Step 1 Generate Chromosome
population = generateChromosome(popSize, population)
print("====Population with fitness value=====")
for i in population:
  print(i, end="\n")
print("Population Size ", len(population))

for x in range(generation):
  print("", end='\n')
  # Step 2 selection using roulete wheel
  parents = []
  while(len(parents)==0):
    parents = rouletWheelSelection(popSize, population, pC)
  print("====Gen-"+str(x)+" selected individu after roulet wheel selection====")
  for i in parents:
    print(i, end='\n')
  print("", end='\n')
  # print("Population Size ", len(population))
  print("====Gen-"+str(x)+" selected individu to be a parents by default====")

  # Step 3 Crossover 
  child = crossOver(parents)
  print("====Gen-"+str(x)+" Individu to be a child after crosOver====")
  for i in child:
    print(i,end="\n")
  # print("Population Size ", len(population))

  #step 4 Mutate that child 
  print("", end='\n')
  print("====Gen-"+str(x)+" individu after mutation to be offspring====")
  offspring = mutation(child, pM, lenghtOfchromosome)
  for i in offspring:
    print(i, end="\n")
  # print("Population Size ", len(population))

  #step 5 Update Generation using elitism , the most fitness absolutely to be next generation
  newPopulation = updateGeneration(population, offspring)
  print("==== Gen-"+str(x)+" New Population was generated====")
  for i in newPopulation:
    print(i, end='\n')

print("", end='\n')
print("result of the best generation :")
print("a : " + str(newPopulation[0]["a"]))
print("b : " + str(newPopulation[0]["b"]))
print("c : " + str(newPopulation[0]["c"]))

predictValue51 = round(newPopulation[0]["a"]*covidSummaryPerDays[49]+newPopulation[0]["b"]*covidSummaryPerDays[50]+newPopulation[0]["c"])
print("untuk proyeksi hari ke 51 : "+str(predictValue51))

