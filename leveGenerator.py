import nltk
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
import pandas as pd
# from Levenshtein import distance
import numpy as np
import pickle

DEBUGG = 0  # 0 = False, 1 = True

# TODO make a distance that penalizes that a word is using two of the same character.
def levenshteinDistance(str1, str2):
    m = len(str1)
    n = len(str2)
    d = [[i] for i in range(1, m + 1)]  # d matrix rows
    d.insert(0, list(range(0, n + 1)))  # d matrix columns
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if str1[i - 1] == str2[j - 1]:  # Python (string) is 0-based
                substitutionCost = 0
            else:
                substitutionCost = 1
            d[i].insert(j, min(d[i - 1][j] + 1,
                               d[i][j - 1] + 1,
                               d[i - 1][j - 1] + substitutionCost))
    return d[-1][-1]


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def generateBaseMatrix():
    with open('data/spanish.txt', 'r', encoding="utf-8") as file:
        # Gets a word per array element
        words = file.read().splitlines()

        bmat = generateLeveMatrix(words)
        pickle.dump(bmat, open("data/leveDistanceMatrix", "wb"))


def generateLeveMatrix(data):
    # Y = pdist(data, lambda u, v: levenshteinDistance(u, v))
    list1 = data
    list2 = data

    matrix = np.zeros((len(list1), len(list2)), dtype=int)

    for i in range(0, len(list1)):
        # print("Progress : {}".format(str(i/len(list1)*100)))
        printProgressBar(i, len(list1))
        for j in range(0, len(list2)):
            matrix[i, j] = levenshteinDistance(list1[i], list2[j])

    if DEBUGG:
        print(matrix)

    return matrix
