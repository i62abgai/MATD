import sys
import time
import os.path

def bruteForce(file, pattern):
    matches = []
    #for each line
    for index, line in enumerate(file):
        #compare the line with the pattern
        for i in range(len(line)-len(pattern)):
            for j in range(len(pattern)):
                #if it's different then we move to the next character
                if line[i+j] != pattern[j]:
                    break  
            if j == (len(pattern)-1):
                print('Pattern found: '+ str([index, i]))
                matches.append([index, i])
    return matches    

def main():

    fileName = sys.argv[1]
    file=open(fileName, "r")

    pattern = sys.argv[2]

    time_start = time.process_time()
    pos=bruteForce(file, pattern)
    time_elapsed = time.process_time()
    #If file exists we append the result, if not we create it and write the measure of time
    if os.path.exists('measures.txt'):
        f= open("measures.txt","a+")
    else:
        f= open("measures.txt","w+")

    f.write("Algorithm: Naive \t Time: "+str(time_elapsed)+" secs \t Pattern: " + str(pattern)+"\n")

if __name__ == "__main__":
    main()
    