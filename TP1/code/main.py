import arithmetique
import paires
import random
import string
import csv
import Result

# Fonction issu de PYnative
def get_random_string(length, letters):
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# Fonction pour les expériences 1 et 2
def tauxCompressionExperience(exp):
    csvArithmetiqueFile = open('./results/' + exp + '_arithmetique.csv', 'w', newline='')
    ariWriter = csv.writer(csvArithmetiqueFile)
    ariWriter.writerow(['Nombre de symboles', 'Longueur originale', 'Longueur code', 'Taux de compression'])

    csvPairesOctetsFile = open('./results/' + exp + '_paires_octets.csv', 'w', newline='')
    paireWriter = csv.writer(csvPairesOctetsFile)
    paireWriter.writerow(['Nombre de symboles', 'Longueur originale', 'Longueur code', 'Taux de compression'])

    for i in range(5, 1003, 100):
        Message = get_random_string(i, get_random_string(i, ['A', 'B']))

        result1 = arithmetique.algo(Message,  len(Message))
        ariWriter.writerow([i, result1.lOriginal, result1.lCode, 1-(result1.lCode/result1.lOriginal)])
        
        result2 = paires.algo(Message)
        paireWriter.writerow([i, result2.lOriginal, result2.lCode, 1-(result2.lCode/result2.lOriginal)])

    csvArithmetiqueFile.close()
    csvPairesOctetsFile.close()

""" Expérience 1 """
#tauxCompressionExperience("exp1")

""" Expérience 2 """
#tauxCompressionExperience("exp2")

""" Expérience 3 """ 

# csvArithmetiqueFile = open('./results/exp3_arithmetique.csv', 'w', newline='')
# ariWriter = csv.writer(csvArithmetiqueFile)
# ariWriter.writerow(['Nombre de symboles', 'Temps'])

# csvPairesOctetsFile = open('./results/exp3_paires_octets.csv', 'w', newline='')
# paireWriter = csv.writer(csvPairesOctetsFile)
# paireWriter.writerow(['Nombre de symboles', 'Temps'])

# for i in range(2, 1003, 100):
#     Message = get_random_string(i, string.ascii_lowercase)
#     SymbACoder = len(Message)

#     result1 = arithmetique.algo(Message, SymbACoder)
#     ariWriter.writerow([i, result1.temps])
    
#     result2 = paires.algo(Message)
#     paireWriter.writerow([i, result2.temps])

# csvArithmetiqueFile.close()
# csvPairesOctetsFile.close()


""" Expérience 4 """ 
# Messages = 
# ["In every forest there is a cabin. In every cabin there is a stove. In every stove there is an ash pile. In every ash pile there is a bone. In every bone there is a story. In every story there is a yearning. In every yearning there is a prize. In every prize there is a cost. In every cost there is a cut. In every cut there is a ghost. In every ghost there is a home. In every home there is a witch. In every witch there is a girl. In every girl there is a forest."
# for message in Messages:
#     paires.algo(message)
#     arithmetique.algo(message, len(message))

for text in ["In_Every_Girl_There_Is_a_Forest", "The_Disciple", "The_Mice"]:
    m = open('./Textes/' + text + ".txt", 'r').read()
    print(text + ": " )
    paires.algo(m)
    arithmetique.algo(m, len(m))