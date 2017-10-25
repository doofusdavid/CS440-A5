import copy as copy
import numpy as np
import random

def printState(state):
    stateCopy = copy.deepcopy(state)
    maxLength = findLongest(stateCopy)
    for item in stateCopy:
        for x in range (len(item) , maxLength):
            item.insert(0, ' ')

    for i in range(maxLength):
        for j in range(len(stateCopy)):
            print("  {}".format(stateCopy[j][i]), end='')
        print()
    print('--|--|--|--\n\n')


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

def myTupler(state):
    '''Need immutable type for key to dictionary '''
    superTuple = tuple(tuple(s) for s in state)
    return superTuple


def epsilonGreedy(epsilon, Q, state, validMovesF):
    goodMoves = validMovesF(state)
    if np.random.uniform() < epsilon:
        # Random Move
        return tuple(random.choice(goodMoves))
    else:
        # Greedy Move
        Qs = np.array([Q.get((myTupler(state),tuple(m)), 0.0) for m in goodMoves])
        return tuple(goodMoves[np.argmax(Qs)])


def trainQ(nRepetitions, learningRate, epsilonDecayFactor, validMovesF, makeMoveF):
    maxGames = nRepetitions
    rho = learningRate
    epsilonDecayRate = epsilonDecayFactor
    epsilon = 1.0
    Q = {}
    stepList = []
    showMoves = False

    for nGames in range(maxGames):
        epsilon *= epsilonDecayRate
        step = 0
        state = [[1, 2, 3], [], []]
        done = False

        while not done:
            step += 1
            move = epsilonGreedy(epsilon, Q, state, validMovesF)
            stateNew = copy.deepcopy(state)
            makeMoveF(stateNew, move)
            if (myTupler(state), move) not in Q:
                Q[(myTupler(state), move)] = 0.0  # Initial Q value for new state, move
            if showMoves:
                printState(stateNew)
            if winner(stateNew):
                # We won!  backfill Q
                if showMoves:
                    print('End State, we won!')
                Q[(myTupler(state), move)] = 1.0
                done = True
                stepList.append(step)

            if step > 1:
                #Q[(myTupler(stateOld), moveOld)] += rho * (Q[(myTupler(state), move)] - Q[(myTupler(stateOld), moveOld)])
                Q[(myTupler(stateOld), moveOld)] += rho * (Q[(myTupler(state), move)] - Q[(myTupler(stateOld), moveOld)])

            stateOld, moveOld = state, move
            state = stateNew

    print(epsilon)
    return Q,stepList


myQ, myStep = trainQ(1000, 0.5, 0.7, validMoves, makeMove)
print(len(myStep),len(myQ))

print("mean:", np.mean(myStep))
