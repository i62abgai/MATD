import sys
import time
import os.path

def buildLPSTable(pattern, lenPattern):
    lpsTable = [0]*(lenPattern+1)
    pos = 1
    cnd = 0

    lpsTable[0] = -1

    while pos < lenPattern:
        if pattern[pos] == pattern[cnd]:
            lpsTable[pos] = lpsTable[cnd]
        else:
            lpsTable[pos] = cnd
            cnd = lpsTable[cnd]
            while cnd >= 0 and pattern[pos] != pattern[cnd]:
                cnd = lpsTable[cnd]
        pos = pos + 1
        cnd = cnd + 1
    lpsTable[pos] = cnd 
    
    return lpsTable       

def kmpSearch(file, pattern):
    matches = []

    lenPattern = len(pattern)
    lpsTable = buildLPSTable(pattern, lenPattern)
    print(lpsTable)

    for index, line in enumerate(file):
        lenLine = len(line)
        k = j = 0
        while j < (lenLine):
            if pattern[k] == line[j]:
                j += 1
                k += 1
                if k == (lenPattern):
                    matches.append([index, j-k])
                    k = lpsTable[k-1]
            else:
                k = lpsTable[k-1]
                if k < 0:
                    j += 1
                    k += 1 
    return matches


def main():
    fileName = sys.argv[1]
    file=open(fileName, "r")

    pattern = sys.argv[2]

    time_start = time.process_time()
    pos=kmpSearch(file, pattern)
    time_elapsed = time.process_time()
    #If file exists we append the result, if not we create it and write the measure of time
    if os.path.exists('measures.txt'):
        f= open("measures.txt","a+")
    else:
        f= open("measures.txt","w+")
    print(len(pos))
    f.write("Algorithm: KMP \t Time: "+str(time_elapsed)+" secs \t Pattern: " + str(pattern)+"\n")

if __name__ == "__main__":
    main()