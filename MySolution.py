import copy as copy

def printState(state):
    printState = copy.deepcopy(state)
    maxLength = findLongest(printState)
    for item in printState:
        for x in range (len(item) , maxLength):
            item.insert(0,('' * (maxLength - len(item))))

    for i in range(maxLength):
        for j in range(len(printState)):
            print("{}\t".format(printState[j][i]), end='')
        print()
    print('------------')


def findLongest(state):
    length = 0
    for item in state:
        length = max(length, len(item))

    return length


def validMoves(state):
    validStates = []

    for itemToMove in state:
        # Check if the list is empty
        if itemToMove:
            for placeToMove in state:
                # don't count as valid move if it's back to the same location
                if state.index(itemToMove) != state.index(placeToMove):
                    if len(placeToMove) == 0 or itemToMove[0] < placeToMove[0]:
                        validStates.append((state.index(itemToMove), state.index(placeToMove)))
    return validStates


def makeMove(state, move):
    item = state[move[0]].pop(0)
    state[move[1]].insert(0, item)


def unMakeMove(state, move):
    item = state[move[1]].pop(0)
    state[move[0]].insert(0, item)


def winner(state):
    board = [[], [], [1,2,3]]
    return state == board


myState = [[1 ,2] ,[3] ,[]]

print(validMoves(myState))
for move in validMoves(myState):
    makeMove(myState, move)
    printState(myState)
    unMakeMove(myState, move)
