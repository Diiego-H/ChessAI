# Evaluate the board to return a reward signal for exercise 1
def evaluateSim(state, nextState):
    return 1000000 if nextState.isTerminal() else (-10 if nextState.list[1][0] != 0 else 0) + (-10 if nextState.list[1][1] in [4,5,6] else 0) - 10 * abs(nextState.list[0][0] - 2) - 10 * abs(nextState.list[0][1] - 5)

steps = { "7,5,6/7,0,2-0,5,12/0,0,8-True" : "7,5,6/0,0,2-0,5,12-False",
          "7,5,6/0,0,2-0,5,12-False"      : "7,5,6/0,0,2-1,5,12-True",
          "7,5,6/0,0,2-1,5,12-True"       : "7,5,6/1,0,2-1,5,12-False",
          "7,5,6/1,0,2-1,5,12-False"      : "7,5,6/1,0,2-0,5,12-True",
          "7,5,6/1,0,2-0,5,12-True"       : "6,5,6/1,0,2-0,5,12-False",
          "6,5,6/1,0,2-0,5,12-False"      : "6,5,6/1,0,2-0,4,12-True",
          "6,5,6/1,0,2-0,4,12-True"       : "5,5,6/1,0,2-0,4,12-False",
          "5,5,6/1,0,2-0,4,12-False"      : "5,5,6/1,0,2-0,5,12-True",
          "5,5,6/1,0,2-0,5,12-True"       : "4,5,6/1,0,2-0,5,12-False",
          "4,5,6/1,0,2-0,5,12-False"      : "4,5,6/1,0,2-0,4,12-True",
          "4,5,6/1,0,2-0,4,12-True"       : "3,5,6/1,0,2-0,4,12-False",
          "3,5,6/1,0,2-0,4,12-False"      : "3,5,6/1,0,2-0,5,12-True",
          "3,5,6/1,0,2-0,5,12-True"       : "2,4,6/1,0,2-0,5,12-False",
          "2,4,6/1,0,2-0,5,12-False"      : "2,4,6/1,0,2-0,4,12-True",
          "2,4,6/1,0,2-0,4,12-True"       : "2,4,6/0,0,2-0,4,12-False" }

# Evaluate the board to return a reward signal for exercise 2 (blacks and whites cooperate)
def evaluate(state, nextState):
    #s = str(state)
    #return 1 if (s in steps and steps[s] == str(nextState)) else -1
    if nextState.isTerminal():
        return 100000 if not nextState.isKingSafe(False) else -200000
    if len(nextState.listB) == 1 and len(state.listB) == 2:
        return 10000
    if len(nextState.listW) == 1:
        return -20000
    if state.listB[0][0] - 1 == nextState.listB[0][0]:
        return 1000
    if state.listB[0][0] + 1 == nextState.listB[0][0]:
        return -2000
    if (state.listW[0][0] - state.listB[0][0] > 2) and (state.listW[0][0] - 1 == nextState.listW[0][0]):
        return 1000
    if state.listW[0][0] + 1 == nextState.listW[0][0]:
        return -1000

    return -1