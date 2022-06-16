import pickle
import numpy as np
import matplotlib.pyplot as pyplot

f = open('data/leveDistanceMatrix', 'rb')
cl = pickle.load(f)

def hasRepeatedChars(s):
    for i in range(len(s)):
        if i != s.rfind(s[i]):
            return True
    return False

with open('data/spanish.txt', 'r', encoding="utf-8") as file:
    # Gets a word per array element
    data = file.read().splitlines()

    # Gets the number of words
    num_words = len(data)
    print('Number of words:', num_words)

    # Total distances for each word, minus distance is better
    row_sums = sum(cl)

    # Order of indexes
    ordered_rows_indexes = [i[0] for i in sorted(enumerate(row_sums), key=lambda k: k[1], reverse=False)]
    print(ordered_rows_indexes)

    # Print Ranking with his corresponding levenhstain distances
    for i, index in enumerate(ordered_rows_indexes):
        ranking = data[index]
        if not hasRepeatedChars(data[index]):
            print("Ranking[{}] -> {} -> Leve distance[{}]".format(i, data[index], row_sums[index]))



    min_index = np.argmin(row_sums)
    # Positions each in mins?
    # mins = min(cl, key=sum)
    pyplot.semilogy(row_sums)



f.close()