#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:22:03 2022

@author: Diego
"""

import chess, piece
from collections import defaultdict
from evaluation import evaluate, evaluateSim
import numpy as np
import datetime

# Make a move in the board for the exercise 1 version (IT DOES NOT CASTLE)
def moveSingle(aichess, origin, target, verbose):
    aichess.chess.moveSim([i for i in origin if i not in target][0][:2], [j for j in target if j not in origin][0][:2], verbose)
    
# Make a move in the board for the exercise 2 version (IT DOES NOT CASTLE)
def moveDouble(aichess, origin, target, verbose):
    x, y = (origin.listW, target.listW) if origin.turn else (origin.listB, target.listB)
    aichess.chess.move([i for i in x if i not in y][0][:2], [j for j in y if j not in x][0][:2], verbose)
        
# Get a state's successors for the exercise 1 version
def nextStatesSingle(aichess, state):
    if state.isTerminal():
        return []
    if len(state.successors) == 0:
        # We must filter the states in which the king will be threatened
        for s_list in aichess.chess.getListNextStatesSim():
            s = Aichess.State(s_list)
            if s.isKingSafe():
                state.successors.append(s)
    return state.successors

# Get a state's successors for the exercise 2 version
def nextStatesDouble(aichess, state):
    return state.successors
            
class Aichess():
    """
    A class to represent the game of chess.

    ...

    Attributes:
    -----------
    chess : Chess
        represents the chess game

    Methods:
    --------
    startGame(pos:stup) -> None
        Promotes a pawn that has reached the other side to another, or the same, piece

    """
        
    def __init__(self, TA, sim, myinit=True):
        if myinit:
            self.chess = chess.Chess(TA, True)
        else:
            self.chess = chess.Chess([], False)

        if sim:
            self.makeMove = moveSingle
            self.nextStates = nextStatesSingle
            self.initial_state = Aichess.State(self.chess.board.currentStateW)
            self.evaluate = evaluateSim
            self.test = lambda x, y: y == 6
        else:
            self.makeMove = moveDouble
            self.nextStates = nextStatesDouble
            self.initial_state = Aichess.Double_State(self, [self.chess.board.currentStateW, self.chess.board.currentStateB], True)
            self.evaluate = evaluate
            self.test = lambda x, y: x.isTerminal() and (not x.isKingSafe(False))
    
    # Make a move in the board (IT DOES NOT CASTLE)
    def move(self, origin, target, verbose=False):
        self.makeMove(self, origin, target, verbose)
    
    # Get a state's successors
    def getNextStates(self, state):
        return self.nextStates(self, state)
    
    # State class
    class State():
        def __init__(self, state_list):
            
            # Computes if a movement is valid (if our king would be in check, or not)
            def computeSafety():
                if [1,5,6] == self.list[0]:
                    return False
                for i in [0,1]:
                    for j in [4,6]:
                        if [i, j, 6] == self.list[0]:
                            return False
                return True
            
            # Computes if a state is terminal
            def computeTerminal():
                if [2, 5, 6] == self.list[0]:
                    for i in [0,1,2,3,7]:
                        if [0, i, 2] == self.list[1]:
                            return True
                return False
            
            # List sorted so as we know the king is always in the first position, useful for unique ID and evaluations
            x, y = sorted([[i for i in item] for item in state_list], key=lambda x : x[2], reverse=True)
            self.string = f"{x[0]},{x[1]},{x[2]}/{y[0]},{y[1]},{y[2]}"
            self.list = [x,y]
            self.safe = computeSafety()
            self.terminal = computeTerminal()
            self.successors = []
        
        def __iter__(self):
            return iter(self.list)
        
        def __str__(self):
            return self.string
            
        # Checks whether the king is safe
        def isKingSafe(self):
            return self.safe
        
        # Check if it is a checkmate state
        def isTerminal(self):
            return self.terminal

        
    class Double_State():
        
        pieces = {2 : piece.Rook(True), 6 : piece.King(True), 8 : piece.Rook(False), 12 : piece.King(False)}
        
        def __init__(self, aichess, state_list, turn):
            
            def computeString():
                z = x[0]
                s = f"{z[0]},{z[1]},{z[2]}"
                if len(x) == 2:
                    z = x[1]
                    s += f"/{z[0]},{z[1]},{z[2]}"
                z = y[0]
                s += f"-{z[0]},{z[1]},{z[2]}"
                if len(y) == 2:
                    z = y[1]
                    s += f"/{z[0]},{z[1]},{z[2]}"
                s += f"-{turn}"
                return s
            
            # Lists sorted so as we know the king is always in the first position, useful for unique ID and evaluations
            x, y = sorted([[i for i in item] for item in state_list[0]], key=lambda x : x[2], reverse=True), sorted([[i for i in item] for item in state_list[1]], key=lambda x : x[2], reverse=True)
            self.string = computeString()
            self.aichess = aichess
            self.listW = x
            self.listB = y
            self.turn = turn
            self.successors = None
            self.safeW = None
            self.safeB = None
            
        def __iter__(self):
            return iter(self.listW if self.turn else self.listB)
        
        def __str__(self):
            return self.string
        
        # Check if the king is safe, other is to know if the king to evaluate is the other side's
        def isKingSafe(self, other=True):
            
            def computeSafety():
                pos, i = (self.listW[0][0:2], 1) if b else (self.listB[0][0:2], 0)
                
                # Check if the king is threatened (if a piece of the other color can move to its position)
                self.aichess.chess.turn = not b
                for nextState in self.aichess.chess.getListNextStates():
                    check_list = nextState[i]
                    for p in check_list:
                        if p[0:2] == pos:
                            self.aichess.chess.turn = self.turn
                            return False
                self.aichess.chess.turn = self.turn
                return True
            
            b = self.turn ^ other
            if b:
                if self.safeW == None:
                    self.safeW = computeSafety()
                return self.safeW
            else:
                if self.safeB == None:
                    self.safeB = computeSafety()
                return self.safeB
        
        # Check if it is a terminal state
        def isTerminal(self):
            if self.successors == None:
                # Get state successors'
                self.successors = []
                my_list, other_list = (self.listW, self.listB) if self.turn else (self.listB, self.listW)
                 # We must filter the states in which the king will be threatened
                for s_list in self.aichess.chess.getListNextStates():
                    s = Aichess.Double_State(self.aichess, s_list, not self.turn)
                    moveDouble(self.aichess, self, s, False)
                    if s.isKingSafe():
                        self.successors.append(s)
                        
                    # Undo move
                    self.aichess.chess.turn = not self.aichess.chess.turn
                    board = self.aichess.chess.board
                    board.currentStateW = [[z for z in item] for item in self.listW]
                    board.currentStateB = [[z for z in item] for item in self.listB]
                    board = board.board
                    for z in (s_list[0] if self.turn else s_list[1]):
                        board[z[0]][z[1]] = None
                    for z in my_list:
                        board[z[0]][z[1]] = Aichess.Double_State.pieces[z[2]]
                    for z in other_list:
                        board[z[0]][z[1]] = Aichess.Double_State.pieces[z[2]]
                        
            return len(self.successors) == 0
        
    # Find best successors according to Q_values. PRECONDITION: State is not terminal
    def find_best_successor(self, state, Q_vals):
        k = Q_vals[str(state)]
        if len(k) == 0:
            return np.random.choice(self.getNextStates(state))
        
        # Find a best successor among those with a Q_value (if there are more than one, we choose one randomly)
        v, bests = float("-inf"), []
        for successor in self.getNextStates(state):
            successor_s = str(successor)
            if successor_s in k:
                newValue = k[successor_s]
                if v == newValue:
                    bests.append(successor)
                elif v < newValue:
                    v, bests = newValue, [successor]
                    
        return np.random.choice(bests)

    # Q-Learning algorithm
    def Q_learning(self, Q_vals, max_depth, gamma, alpha):
        # Choose a successor based on an epsilon-greedy policy derived from Q_vals. PRECONDITION: State is not terminal
        def chooseSuccessor(epsilon=0.4):
            # Exploration / Exploitation
            return bestNext if np.random.uniform() >= epsilon else np.random.choice(self.getNextStates(state))
        
        # Return the reward signal observed from the move done
        def getReward():
            return self.evaluate(state, nextState)
        
        # Update the Q values table based on the reward observed in this iteration
        def update_Q_vals():
            next_s = str(nextState)
            d = Q_vals[str(state)]
            q = d[next_s] if next_s in d else 0
            if nextState.isTerminal():
                # Terminal states does not have Q vals!
                d[next_s] = q + alpha * (getReward() - q)
            else:
                # Find the best successor for the next state
                nonlocal bestNext
                bestNext = self.find_best_successor(nextState, Q_vals)
                # Note that, by doing this, we are not taking into account the Q_val updated know, so it will
                # be less likely that we repeat a move. It is not an inconvenient since we want to avoid loops
                d[next_s] = q + alpha * (getReward() + gamma * (Q_vals[next_s][str(bestNext)] if str(bestNext) in Q_vals[next_s] else 0) - q)
        
        state = self.initial_state
        bestNext = self.find_best_successor(state, Q_vals)
        depth = 0
        while not state.isTerminal() and depth < max_depth:
            depth += 1
            nextState = chooseSuccessor()
            self.move(state, nextState)
            update_Q_vals()
            state = nextState
    
# Read the Q-values table from a file
def get_tables(filePath):
    Q_vals = defaultdict(lambda: {})
    try:
        with open(filePath, "r") as f:
            for l in f.readlines():
                s, t = l.split()
                d = Q_vals[s]
                for x in t.split("_"):
                    n, q = x.split(":")
                    d[n] = float(q)
    except IOError:
        pass
    
    return Q_vals

# Save the Q-values in a file
def save_tables(Q_vals, filePath):
    try:
        with open(filePath, "w") as f:
            for s in Q_vals:
                d = Q_vals[s]
                if len(d) != 0:
                    successors = list(d.keys())
                    n = successors[0]
                    f.write(f"{s} {n}:{d[n]}")
                    for i in range(1, len(successors)):
                        n = successors[i]
                        f.write(f"_{n}:{d[n]}")
                    f.write("\n") 
    except IOError:
        print("ERROR: Unable to save the Q-values learnt")

# Run an exercise
def run(aichess, filePath, max_depth, gamma=0.7, alpha=0.1, verbose=False):
    # Check if we reach our goal in a match using the current optimal policy
    def test_match(aichess, Q_vals, max_depth):
        state = aichess.initial_state
        nonlocal depth
        while not state.isTerminal() and depth < max_depth:
            depth += 1
            nextState = aichess.find_best_successor(state, Q_vals)
            aichess.move(state, nextState)
            state = nextState
        if verbose:
            print("\tResult using the policy derived from the current Q values:")
            aichess.chess.board.print_board()
        return aichess.test(state, depth)

    # Load the computed Q_values from other executions
    Q_vals = get_tables(filePath)
    timer = datetime.datetime.now()
    counter = 0
    depth = 0
    while not test_match(aichess, Q_vals, max_depth):
        # We train until obtaining our goal
        for i in range(1000):
            aichess.chess = chess.Chess(TA, True)
            aichess.Q_learning(Q_vals, max_depth, gamma, alpha)
        aichess.chess = chess.Chess(TA, True)
        depth = 0
        counter += 1
    timer = datetime.datetime.now() - timer
    print(f"\tLearning time: {timer} ({1000 * counter} games needed)")
    print(f"\tCheckmate obtained in {depth} turns:")
    aichess.chess.board.print_board()
    save_tables(Q_vals, filePath)

if __name__ == "__main__":
    gammas = [0.1, 0.4, 0.7]
    alphas = [0.1, 0.4, 0.7]
    
    # EXERCISE 1
    print("EXERCISE 1:")

    # initialize board
    TA = np.zeros((8, 8))
    # white pieces
    TA[7][0] = 2
    TA[7][5] = 6
    # black pieces
    TA[0][5] = 12
    
    aichess = Aichess(TA, True)
    state = aichess.initial_state
    print(f"\tInitial state: {state}\n\tNext states:")
    for s in aichess.getNextStates(state):
        print(f"\t\t{s}")
    for x in gammas:
        for y in alphas:
            aichess.chess = chess.Chess(TA, True)
            print(f"Computing Q-learning. Gamma = {x}, alpha = {y}")
            run(aichess, f"Q1_{x}_{y}.txt", 10, x, y)
    
    # EXERCISE 2
    print("\nEXERCISE 2:\n")
    
    # We add the black rook
    TA[0][0] = 8
    
    aichess = Aichess(TA, False)
    state = aichess.initial_state
    b = state.isTerminal()
    print(f"\tInitial state: {state}\n\tNext states:")
    for s in aichess.getNextStates(state):
        print(f"\t\t{s}")
    for x in gammas:
        for y in alphas:
            aichess.chess = chess.Chess(TA, True)
            print(f"Computing Q-learning. Gamma = {x}, alpha = {y}")
            run(aichess, f"Q2_{x}_{y}.txt", 20, x, y)
