import sys

finish = False
finalState = -1


def buildTable(p_1, k):
    len_p1 = len(p_1)
    matrix = [[0 for x in range(len_p1+1)] for y in range(k)]
    for i in range(k):
        for j in range(len_p1+1):
            matrix[i][j] = (i * len_p1) + (j + i) + 1
    return matrix


# When is match
def nextState(currentState):
    return currentState+1


# When is missmatch
def nextEpsState(currentState, len_p1):
    return currentState+len_p1+1

# When is insertion, or delete
# def nextAnyState(currentState, len_p1):


def nfaSearch(p_1, p_2, i, j, currentState, k):
    global finish, finalState
    if finish == False:
        if currentState % (len(p_1)+1) == 0 and currentState <= ((len(p_1)+1)*k):
            finish = True
            finalState = currentState
            return currentState
        elif i < len(p_1) and j < len(p_2):
            if p_1[i] == p_2[j]:
                nfaSearch(p_1, p_2, i+1, j+1, currentState+1, k)
            else:
                nfaSearch(p_1, p_2, i, j+1, (currentState+len(p_1)+1), k)
                nfaSearch(p_1, p_2, i+1, j, (currentState+len(p_1)+2), k)
                nfaSearch(p_1, p_2, i+1, j+1, (currentState+len(p_1)+2), k)
        return currentState
    else:
        return -1


def main():
    global finalState
    if len(sys.argv) != 4:
        print("Incorrect number of parameters: \n" +
              "\t main.py \"pattern\" \"text\" \"k\"")
        return -1

    p_1 = sys.argv[1]
    p_2 = sys.argv[2]
    k = int(sys.argv[3])+1

    matrix = buildTable(p_1, k)

    for i in matrix:
        print(i)

    nfaSearch(p_1, p_2, 0, 0, 1, k)

    if finalState % (len(p_1)+1) == 0:
        mod = int((finalState / (len(p_1)+1)) - 1)
        print("Could finish with: " +
              str(mod) + " errors, the final state is: " + str(finalState))
    else:
        print("The value of k is not enough, try with a higher value of k")


if __name__ == "__main__":
    main()
