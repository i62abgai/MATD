import sys
import time
import os.path

def buildLPSTable(pattern, lenPattern):
    #We build the array that allows us to look the shift
    lpsTable = [0]*(lenPattern)
    #If the first one missmatch we just move ahead
    lpsTable[0] = 0
    length = 0
    
    i = 1

    while i < (lenPattern-1):
        #First check the length 1 prefix
        if pattern[i] == pattern[lenPattern-1]:
            length+=1
            lpsTable[i]=length
        else:
            if length != 0:
                length = lpsTable[length-1]
                i-=1
            else:
                #If the prefix with length 1
                #not matches with the sufix we dont check anything else
                #the value its 0
                lpsTable[i]=0
        i+=1

    return lpsTable       

def kmpSearch(file, pattern):
    matches = []

    lenPattern = len(pattern)
    lpsTable = buildLPSTable(pattern, lenPattern)
    print(lpsTable)

    for index, line in enumerate(file):
        lenLine = len(line)
        i = j = 0
        while i < lenLine:
            if line[i] == pattern[j]:
                i+=1
                j+=1
            if j == (lenPattern-1):
                matches.append([index, i-j])
                j = lpsTable[j-1]
            elif i < lenLine and pattern[j] != line[i]:
                if j != 0:
                    j = lpsTable[j-1]
                else:
                    i+=1
                
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
    f.write("Algorithm: KMP \t Time: "+str(time_elapsed)+" secs \t Pattern: " + str(pattern)+"\t N_Matches: "+str(len(pos))+"\n")

if __name__ == "__main__":
    main()