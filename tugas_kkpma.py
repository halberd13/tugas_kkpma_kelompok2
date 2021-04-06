# -*- coding: utf-8 -*-
"""tugas KKPMA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1htW77gnKvKZMtSzWZ6OYF1-vy1aOpV27
"""

import math
import random as rd
import numpy as np

def nilaiFitness(kombinasi):
    fitness = 0
    for i in range(1,len(kombinasi)):
        fitness = fitness + math.sqrt((math.pow((node[kombinasi[i]][0] - node[kombinasi[i-1]][0]),2))+math.pow((node[kombinasi[i-1]][1] - node[kombinasi[i]][1]),2))
    return -fitness

def tournamentParent(populasi, panjangTournament):
    idxSample = np.arange(len(populasi))
    np.random.shuffle(idxSample)
    idxSample = idxSample[0:panjangTournament]
    fitnesses = [(nilaiFitness(pop[idxSample[i]])) for i in range(panjangTournament)]
    mergedArray = [(idxSample[i], fitnesses[i]) for i in range(panjangTournament)]
    mergedArray = sorted(mergedArray,key = lambda a : a[1], reverse = True)
    return mergedArray[0][0], mergedArray[1][0]


def generateKromosom(jumlahPopulasi, panjangKromosom):
    populasi = []
    tmpStartEndNode = np.array([0])
    for i in range(jumlahPopulasi):
        kromosom = []
        kromosom = np.arange(1,panjangKromosom)
        np.random.shuffle(kromosom)
        kromosom = np.concatenate((tmpStartEndNode,kromosom), axis = 0)
        kromosom = np.concatenate((kromosom,tmpStartEndNode), axis = 0)
        populasi.append(list(kromosom))
    print(populasi)
    return populasi


def crossover(kromosom1, kromosom2, pC):
    prob = np.random.random()
    point = np.random.randint(1,len(kromosom1)-1)
    tmpKromosom1 = []
    tmpKromosom2 = []
    cekKromosom1 = []
    cekKromosom2 = []
    if(prob <= pC):
        tmpKromosom1 = kromosom1[:point]
        tmpKromosom2 = kromosom2[:point]
        cekKromosom1 = kromosom1[point:]
        cekKromosom2 = kromosom2[point:]
        for i in range(point, len(kromosom2)):
            if(kromosom2[i] in tmpKromosom1):
                for j in range(len(kromosom1)):
                    if((kromosom1[j] not in tmpKromosom1) and (kromosom1[j] not in cekKromosom2)):
                        tmpKromosom1 = tmpKromosom1 + [kromosom1[j]]
                        break
                        
            else:
                tmpKromosom1 = tmpKromosom1 + [kromosom2[i]]
        for i in range(point, len(kromosom1)):
            if(kromosom1[i] in tmpKromosom2):
                for j in range(len(kromosom2)):
                    if((kromosom2[j] not in tmpKromosom2) and (kromosom2[j] not in cekKromosom1)):
                        tmpKromosom2 = tmpKromosom2 + [kromosom2[j]]
                        break
            else:
                tmpKromosom2 = tmpKromosom2 + [kromosom1[i]]
        
        tmpKromosom1 = tmpKromosom1 + kromosom1[len(kromosom1)-1:len(kromosom1)]
        tmpKromosom2 = tmpKromosom2 + kromosom2[len(kromosom2)-1:len(kromosom2)]
    else:
        tmpKromosom1 = kromosom1
        tmpKromosom2 = kromosom2
    return tmpKromosom1, tmpKromosom2


def mutasi(kromosom, pM):
    for i in range(1,len(kromosom)-1):
        tmp = 0
        prob = np.random.random()
        if(prob <= pM):
            while(tmp == 0):
                tmp = np.random.randint(1,len(kromosom)-2)
            for j in range(1, len(kromosom)-1):
                if(tmp == kromosom[j]):
                    kromosom[j] = kromosom[i]
                    kromosom[i] = tmp
                    break
    return kromosom


def steadyState(jumlahGeneration ,populasi, jumlahPopulasi, panjangTournament):
    for j in range(jumlahGeneration):
        gabungan = []
        child = []
        fitnesses = []
#         print(populasi)
        for i in range(round(len(populasi)/2)):
            idxParent1, idxParent2 = tournamentParent(populasi, panjangTournament)
            anak1 = populasi[idxParent1][:]
            anak2 = populasi[idxParent2][:]
            
            #Crossover
            anak1,anak2 = crossover(anak1,anak2,pC)
            
            #Mutasi
            anak1 = mutasi(anak1,pM)
            anak2 = mutasi(anak2,pM)
            
            child.append(anak1)
            child.append(anak2)
            
        gabungan = populasi + child
        for i in range(len(gabungan)):
            fitnesses.append(nilaiFitness(gabungan[i]))
        mergedArray = [(gabungan[i], fitnesses[i]) for i in range(len(gabungan))]
        mergedArray = sorted(mergedArray, key = lambda a : a[1], reverse = True)
        pop = []
        tmp = []
        t = 0
        jumlah = 0
        
#         print(mergedArray)
        for i in range(len(gabungan)):
            if(i >= 1):
                nilai = nilaiFitness(gabungan[i])
                if(nilai == mergedArray[jumlah-1][1]):
                    tmp.append(mergedArray[i][0])
                    t += 1
                else:
                    pop.append(mergedArray[i][0])
                    jumlah+=1
            else:
                pop.append(mergedArray[i][0])
                jumlah+=1
            if(jumlah == jumlahPopulasi):
                break
        
        z = 0
#         print(len(populasi))
        while(jumlah < jumlahPopulasi):
            pop.append(tmp[z])
            z+=1
            jumlah+=1
        populasi = []
        populasi = pop
#         print(pop)
#         print(len(pop))
        
#         nilai = -nilaiFitness(populasi[0])
#         print()
#         print(nilai)
        
    return populasi

node = [[82,76],
        [96,44],
        [50,5],
        [49,8],
        [13,7],
        [29,89],
        [58,30],
        [84,39],
        [14,24],
        [2,39],
        [3,82],
        [5,10],
        [98,52],
        [84,25],
        [61,59],
        [1,65]]

jumlahGenerasi = 500
jumlahIndividu = 50
panjangTournament = round(jumlahIndividu/2)
pC = 0.7
pM = 0.1


pop = generateKromosom(jumlahIndividu,16)
pop = list(pop)
pop = steadyState(jumlahGenerasi, pop, jumlahIndividu, panjangTournament)
print("Generasi ke- "+str(jumlahGenerasi))
print("Rute terbaik : "+str(pop[0]))
print("Cost (jarak) : "+str(-nilaiFitness(pop[0])))

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

def generateChromosome(popSize, population, summaryPopulation):
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

def rouletWheelSelection(popSize, population):
  probabilityCrossOver = 0.8
  totalSelectedIndividu = round(popSize * probabilityCrossOver)
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
    1:	2,
    2:	0.0,
    3:	0.0,
    4:	0.0,
    5:	2,
    6:	0.0,
    7:	2,
    8:	13,
    9:	8,
    10:	0.0,
    11:	35,
    12:	27,
    13:	21,
    14:	17,
    15:	38,
    16:	55,
    17:	82,
    18:	60,
    19:	81,
    20:	64,
    21:	65,
    22:	106,
    23:	105,
    24:	103,
    25:	153,
    26:	109,
    27:	130,
    28:	129,
    29:	114,
    30:	149,
    31:	113,
    32:	196,
    33:	106,
    34:	181,
    35:	218,
    36:	247,
    37:	218,
    38:	337,
    39:	219,
    40:	330,
    41:	399,
    42:	316,
    43:	282,
    44:	297,
    45:	380,
    46:	407,
    47:	325,
    48:	327,
    49:	185,
    50:	375
}

lenghtOfchromosome = 3
popSize = 10
generation = 10
population = []
pM = 0.1

# Step 1 Generate Chromosome
population = generateChromosome(popSize, population, summaryPopulation)
print("====Population with fitness value=====")
for i in population:
  print(i, end="\n")
print("Population Size ", len(population))

for x in range(generation):
  print("", end='\n')
  # Step 2 selection using roulete wheel
  parents = []
  while(len(parents)==0):
    parents = rouletWheelSelection(popSize, population)
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

"""Coba Implementasi GA by Franki Halberd """