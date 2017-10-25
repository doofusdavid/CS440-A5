import copy as copy
import numpy as np
import random

def printState(state):
    '''
    Prints a Tower of Hanoi state.  Now, with added pegs.
    :param state: list of lists representing tower of hanoi state
    :return: prints out the state nicely.
    '''
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
    '''
    Finds the longest (highest) peg in Towers of Hanoi.  Used to display in printState
    :param state: list of lists representing tower of hanoi state
    :return: length of longest item
    '''
    length = 0
    for item in state:
        length = max(length, len(item))

    return length


def validMoves(state):
    '''
    Returns a list of lists representing valid tower of hanoi moves from the given state.
    :param state: list of lists representing tower of hanoi state
    :return: list of lists representing valid tower of hanoi moves from the given state.
    '''
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
    '''
    Takes a move and makes it on a tower of hanoi state
    :param state: list of lists representing tower of hanoi state
    :param move: tuple representing a move from (peg1,peg2)
    :return:the state after the move was made
    '''
    item = state[move[0]-1].pop(0)
    state[move[1]-1].insert(0, item)
    return state


def unMakeMove(state, move):
    '''
    Reverses a move made by makeMove.  No longer used.
    :param state: list of lists representing tower of hanoi state
    :param move: move: tuple representing a move from (peg1,peg2)
    :return: the state after the move was made
    '''
    item = state[move[1]-1].pop(0)
    state[move[0]-1].insert(0, item)
    return state


def winner(state):
    '''
    Determines if a winning state occured
    :param state: list of lists representing tower of hanoi state
    :return: True if winning state, False otherwise.
    '''
    board = [[], [], [1,2,3]]
    return state == board


def myTupler(state):
    '''
    Need immutable type for key to dictionary
    :param state: list of lists representing tower of hanoi state
    :return: tuple representation of the state
    '''
    superTuple = tuple(tuple(s) for s in state)
    return superTuple


def epsilonGreedy(epsilon, Q, state, validMovesF):
    '''
    Makes either a random move, or tries the move which Q indicates is the best.
    :param epsilon: A decreasing number representing the level of randomness
    :param Q: Dictionary of state,move - value pairs, with the higher values being better moves
    :param state: list of lists representing tower of hanoi state
    :param validMovesF: function returning valid moves
    :return:
    '''
    goodMoves = validMovesF(state)
    if np.random.uniform() < epsilon:
        # Random Move
        return tuple(random.choice(goodMoves))
    else:
        # Greedy Move
        Qs = np.array([Q.get((myTupler(state),tuple(m)), 0.0) for m in goodMoves])
        return tuple(goodMoves[np.argmax(Qs)])


def trainQ(nRepetitions, learningRate, epsilonDecayFactor, validMovesF, makeMoveF):
    '''
    Creates and fills a dictionary, Q, representing the (state,move) - value pairs which, if followed
    should create the shortest path to the solution.
    :param nRepetitions: how many times to iterate through.  Higher numbers would generate more accurate results
    :param learningRate: How much to adjust the value part of the dictionary
    :param epsilonDecayFactor: how quickly to reduce the random factor.
    :param validMovesF: function returning valid moves of a state
    :param makeMoveF: function making a move on a state
    :return: the dictionary, Q, and a list containing the number of steps it took per iteration to find the goal state
    '''
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
                Q[(myTupler(state), move)] = -1.0
                done = True
                stepList.append(step)

            if step > 1:
                Q[(myTupler(stateOld), moveOld)] += rho * (-1+Q[(myTupler(state), move)] - Q[(myTupler(stateOld), moveOld)])

            stateOld, moveOld = state, move
            state = stateNew

    return Q,stepList

def testQ(Q, maxSteps, validMovesF, makeMoveF):
    '''
    Using the dictionary Q, and the initial state of the game, traverse and return the best path.
    :param Q: dictionary representing the (state,move) - value pairs which, if followed should create the shortest path to the solution.
    :param maxSteps: The number of steps to attempt before giving up.
    :param validMovesF: function returning valid moves of a state
    :param makeMoveF: function making a move on a state
    :return: list containing the states from start to finish
    '''
    state = [[1, 2, 3], [], []]
    statePath = []
    statePath.append(state)

    for i in range(maxSteps):
        if winner(state):
            return statePath
        goodMoves = validMovesF(state)
        Qs = np.array([Q.get((myTupler(state), tuple(m)), 0.0) for m in goodMoves])
        move = goodMoves[np.argmax(Qs)]
        nextState = copy.deepcopy(state)
        makeMoveF(nextState, move)
        statePath.append(nextState)
        state = nextState

    return "No path found"



g = 0
print('\nTesting   Q, steps = trainQ(1000, 0.5, 0.7, validMoves, makeMove).')
try:
    Q, steps = trainQ(10000, 0.5, 0.7, validMoves, makeMove)
    for key,value in Q.items(): print(key,value)
    if 70 < len(Q) < 80:
        g += 10
        print('\n--- 10/10 points. Q dictionary has correct number of entries.')
    else:
        print('\n---  0/10 points. Q dictionary should have close to 76 entries. Yours has {}'.format(len(Q)))

    mn = np.array(steps).mean()
    if mn < 10:
        g += 10
        print('\n--- 10/10 points. The mean of the number of steps is {} which is correct.'.format(mn))
    else:
        print('\n---  0/10 points. The mean of the number of steps is incorrect.  Yours is {}.  It should be less than 10.'.format(mn))
except Exception as ex:
    print('\n--- trainQ raised the exception\n {}'.format(ex))
print('\nTesting   path = testQ(Q, 20, validMoves, makeMove).')
try:
    path = testQ(Q, 20, validMoves, makeMove)
    if len(path) < 10:
        g += 20
        print('\n--- 20/20 points. Correctly returns path of length {}, less than 10.'.format(len(path)))
    else:
        print('\n---  0/20 points. Did not return correct path.  Length of your path is {}. It should be less than 10.'.format(len(path)))
except Exception as ex:
    print('\n--- testQ raised the exception\n {}'.format(ex))
