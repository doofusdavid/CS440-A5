import copy as copy

def printState(state):
    printState = copy.deepcopy(state)
    maxLength = findLongest(printState)
    for item in printState:
        for x in range (len(item) , maxLength):
            item.insert(0, ' ')

    for i in range(maxLength):
        for j in range(len(printState)):
            print("  {}".format(printState[j][i]), end='')
        print()
    print('--|--|--|--\n\n')


def findLongest(state):
    length = 0
    for item in state:
        length = max(length, len(item))

    return length


def validMovesOld(state):
    validStates = []

    for itemToMove in state:
        # Check if the list is empty
        if itemToMove:
            # Iterate through the rest of the states
            for placeToMove in range(len(state)):
                # don't count as valid move if it's back to the same location
                if state.index(itemToMove) != placeToMove:
                    # valid move if the place to move is empty or the item to move is smaller
                    if len(state[placeToMove]) == 0 or itemToMove[0] < state[placeToMove][0]:
                        # append the tuple (move from, move to) to the valid states
                        validStates.append((state.index(itemToMove), placeToMove))
    return validStates

def validMoves(state):
    validStates = []

    for itemToMove in state:
        # Check if the list is empty
        if itemToMove:
            # Iterate through the rest of the states
            for placeToMove in range(len(state)):
                # don't count as valid move if it's back to the same location
                if state.index(itemToMove) != placeToMove:
                    # valid move if the place to move is empty or the item to move is smaller
                    if len(state[placeToMove]) == 0 or itemToMove[0] < state[placeToMove][0]:
                        # append the tuple (move from, move to) to the valid states
                        validStates.append([state.index(itemToMove)+1, placeToMove+1])
    return validStates


def makeMove(state, move):
    item = state[move[0]-1].pop(0)
    state[move[1]-1].insert(0, item)
    return state


def unMakeMove(state, move):
    item = state[move[1]-1].pop(0)
    state[move[0]-1].insert(0, item)
    return state


def winner(state):
    board = [[], [], [1,2,3]]
    return state == board


# def trainQ(nRepetitions, learningRate, epsilonDecayFactor):

initialState = [[],[],[1,2,3]]
# initialState = [[1,2],[],[3]]
# myState = [[1 ,2] ,[3] ,[]]
printState(initialState)
makeMove([[], [], [1, 2, 3]], [3, 2])
makeMove(initialState, [3,2])
printState(initialState)
print(validMoves(initialState))
#
#
# for move in validMoves(initialState):
#     makeMove(initialState, move)
#     printState(initialState)
#     unMakeMove(initialState, move)
#
# Q = {}
#
#
# def myTupler(state):
#     '''Need immutable type for key to dictionary '''
#     superTuple = tuple(tuple(l) for l in state)
#     return superTuple
#
#
# Q[myTupler(initialState), (0, 1)] = 0
# print(Q)
#
# rho = 0.1
# import random
# import numpy as np
# # move = random.choice(validMoves(myState))
# move = (0,2)
# print(validMoves(initialState))
# print(Q.get((myTupler(initialState),move),0))
# #print(Q[(myTupler(initialState),move)])
#
# Q[(myTupler(initialState),move)] = Q.get((myTupler(initialState),move),0) + rho * (-1 - Q.get((myTupler(initialState),move),0))
#
#
# print(Q)