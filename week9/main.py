import sys
from os.path import isfile, join
from os import listdir
import os
import re
import collections
import math
import operator
tdMatrix = {}

listDocs = []

nDocs = 0


def readFile(folderPrePath, fileName):
    global tdMatrix, nDocs
    nDocs += 1
    # Read the content
    proccessedWords = []
    f = folderPrePath + fileName
    with open(f) as fp:
        line = fp.readline()
        while line:
            line = fp.readline()
            line = line.replace("\n", "")
            proccessedWords.append(line)

    freq = collections.Counter(proccessedWords)
    print(freq)
    input()
    for index, obj in enumerate(freq):
        if obj in tdMatrix:
            tdMatrix[obj].append([fileName, freq[obj]])
        else:
            tdMatrix[obj] = []
            tdMatrix[obj].append([fileName, freq[obj]])
            
def dot(d1, d2):
   if len(d1) != len(d2):
      return 0
   return sum(i[0] * i[1] for i in zip(d1, d2))

def compute_inverse_frequency():
    global tdMatrix, nDocs
    idf_t_vector = {}
    for index, obj in enumerate(tdMatrix):
        idf_t_vector[obj] = math.log(nDocs/len(tdMatrix[obj]), 10)
        for i, o in enumerate(tdMatrix[obj]):
            tdMatrix[obj][i][1] = o[1] * idf_t_vector[obj]

def compute_score(splitted_query):
    global tdMatrix, nDocs
    doc_scores = {}
    for q in splitted_query:
        if q in tdMatrix:
            for doc in tdMatrix[q]:
                if doc[0] in doc_scores:
                    doc_scores[doc[0]] = doc_scores[doc[0]] + doc[1]
                else:
                    doc_scores[doc[0]] = doc[1]
                    
    sorted_scores = sorted(doc_scores.items(), key=operator.itemgetter(1), reverse=True)

    if len(sorted_scores)>= 10:
        for i in range(0,10):
            print("\t\tDocument id: ", sorted_scores[i][0], " Score: ", sorted_scores[i][1])
    elif len(sorted_scores)>0:
        for i in sorted_scores:
            print("\t\tDocument id: ", i[0], " Score: ", i[1])
    else:
        print("\t\tNo matches found")


def main():
    global listDocs, tdMatrix
    if len(sys.argv) > 2:
        folderPrePath = sys.argv[1]
        folderPostPath = sys.argv[2]

        if not os.path.exists(folderPostPath):
            os.makedirs(folderPostPath)

        onlyfiles = [f for f in listdir(
            folderPrePath) if isfile(join(folderPrePath, f))]

        onlyfiles.sort(key=int)

        for fileName in onlyfiles:
            readFile(folderPrePath, fileName)
            
        compute_inverse_frequency()
        
        query = input("\n\n\tSearch: ")
        splitted = query.split()
        
        compute_score(splitted)
        
    else:
        print("Usage: \n main.py \"folder\" \"destination folder\" ")

if __name__ == "__main__":
    main()
