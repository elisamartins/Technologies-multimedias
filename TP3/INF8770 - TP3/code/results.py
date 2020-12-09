from key_frame import get_solution
from carol import get_carol_solution
import time
import csv
import histograms
import numpy as np 
from itertools import islice

N_IMAGES = 200

def get_my_results(algo):
        
    # Algorithme perso
    ecart_minutage = 0
    temps_execution_moyen = 0

    if algo == "carol":
        start = time.time()
        get_carol_solution("jpeg")
        stop = time.time()
        temps_execution_moyen = (stop-start)/N_IMAGES
        bonnes_reponses = 0
    
    else:
        #Temps d'exécution moyen par image
        start = time.time()
        get_solution("jpeg")
        stop = time.time()
        temps_execution_moyen = (stop-start)/N_IMAGES
        bonnes_reponses = 0

    if algo == "carol":
        f_1 = open('../data/carol_solution_jpeg.csv', 'r')
    else: 
        f_1 = open('../data/q3_solution_jpeg.csv', 'r')

    fr_1 = csv.reader(f_1, delimiter=',')
    f_1.readline()

    f_sol = open('../data/solution.csv', 'r')
    fr_solution = csv.reader(f_sol, delimiter=',')
    f_sol.readline()

    sol_data=[]
    sol_results = []

    for row in fr_solution:
        if (row[1] == "out"):
            sol_data.append([row[0], row[1], 0])
        else:
            sol_data.append([row[0], row[1], float(row[2])])

    for row in fr_1:
        if (row[1] == "out"):
            sol_results.append([row[0], row[1], 0])
        else:
            sol_results.append([row[0], row[1], float(row[2])])

    for i in range(0, 200):
        if sol_results[i][1] == sol_data[i][1]:
            bonnes_reponses += 1
            ecart_minutage += abs(float(sol_results[i][2]) -  float(sol_data[i][2]))
            
    ecart_minutage /= bonnes_reponses
    bonnes_reponses = (bonnes_reponses/N_IMAGES)*100

    print("Temps d'exécution moyen: ", str(temps_execution_moyen))
    print("Pourcentage bonnes réponses: ", str(bonnes_reponses))
    print("Écart minutage: ", str(ecart_minutage))
        




get_my_results("other")