# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
import sys

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if action == "Stop":
            return -10;

        total = successorGameState.getScore()
        # print "start:", total,
        x, y = newPos
        curX, curY  = currentGameState.__dict__["data"].__dict__["agentStates"][0].__dict__["configuration"].__dict__ ["pos"]
        # print curX, curY
        # print total,

        if newFood[x][y]:
            total += 200
        else:
            smallest = 1000;
            for i, each in enumerate(newFood.asList()):
                mDist = abs(x - each[0]) + abs(y - each[1])
                if mDist <= smallest:
                    smallest = mDist
            # print "small: ", smallest,
            if(smallest > 1):
                total += 10 / (smallest)
            else:
                total += 95
        total += random.randint(20, 40);

            # print "after path:", total,


        # print(newGhostStates[0].__dict__["configuration"].__dict__ .keys())
        for i, each in enumerate(newGhostStates):
            gX, gY  = newGhostStates[i].__dict__["configuration"].__dict__ ["pos"]

            mDist = abs(x-gX) + abs(y-gY)
            if newScaredTimes[i] < mDist + 5:
                if mDist < 2:
                    return int(-50000)

                elif mDist < 3:
                    # print ("factoring ghost")

                    total = ( -2000 / ( mDist))
                # else:
                    # print ("not factoring ghost")

            else:
                total += 410

        for each in currentGameState.__dict__["data"].__dict__["capsules"]:
            smallest = 1000;
            for i, each in enumerate(newFood.asList()):
                mDist = abs(x - each[0]) + abs(y - each[1])
                if mDist <= smallest:
                    smallest = mDist
            # print "small: ", smallest,
            if (smallest > 1):
                total += 10 / (smallest)
            else:
                total += 100


        # print "final: ", total
        return int(total)

        # return successorGameState.getScore







def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"



        # util.raiseNotDefined()

        level = 1
        maxVal = -1 * sys.maxint

        take = gameState.getLegalActions(self.index)[0]
        for action in gameState.getLegalActions(self.index):
            next = gameState.generateSuccessor(self.index, action)
            cur = self.minValue(next, level)
            if cur > maxVal:
                maxVal = cur
                take = action
        return take

    def maxValue(self, state, level):

        num = state.getNumAgents()
        if state.isWin() or state.isLose() :
            return self.evaluationFunction(state)

        val = -1 * sys.maxint  #-inf

        if level == (num * self.depth):
            return self.evaluationFunction(state)

        level += 1

        for action in state.getLegalActions(self.index):


            next = state.generateSuccessor(self.index, action)

            val = max(val, self.minValue(next, level))

        return val


    def minValue(self, state, level):

        num = state.getNumAgents()
        if state.isWin() or state.isLose() :
            return self.evaluationFunction(state)

        val = sys.maxint  # inf

        if level == (num * self.depth):
            return self.evaluationFunction(state)

        level += 1


        for action in state.getLegalActions(self.index):
            next = state.generateSuccessor(self.index, action)

            if level % num != 0:
                val = min(val, self.minValue(next, level))
            else:
                val = min(val, self.maxValue(next, level))


        return val



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game

      gameState.isWin():
        Returns whether or not the game state is a winning state

      gameState.isLose():
        Returns whether or not the game state is a losing state
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # def max_value(state, alpha, beta, agent, d):
        #     if state.isWin() or state.isLose():
        #         print "hit1"
        #         return self.evaluationFunction(state)
        #
        #     v = -1 * sys.maxint
        #
        #     for action in state.getLegalActions(agent):
        #         succ = state.generateSuccessor(agent, action)
        #         tempVal = 0
        #         print "max, depth",d
        #         print "max, agent",agent
        #         if agent >= succ.getNumAgents():
        #             #goto next depth
        #             print "max, next depth"
        #             agent = 0
        #             d += 1
        #             if d == self.depth:
        #                 print "hit2"
        #                 return self.evaluationFunction(succ)
        #
        #             if agent == self.index:
        #                 tempVal = max_value(succ, alpha, beta, agent + 1, d)
        #             else:
        #                 tempVal = min_value(succ, alpha, beta, agent + 1, d)
        #
        #         else:
        #             if d == self.depth:
        #                 print "hit3"
        #                 return self.evaluationFunction(succ)
        #
        #             if agent == self.index:
        #                 tempVal = max_value(succ, alpha, beta, agent + 1, d)
        #             else:
        #                 tempVal = min_value(succ, alpha, beta, agent + 1, d)
        #
        #         if tempVal > v:
        #             v = tempVal
        #
        #         if v > beta:
        #             print "hit4"
        #             return v
        #
        #         alpha = max(alpha, v)
        #
        #         print "hit5"
        #         return v
        #
        # def min_value(state, alpha, beta, agent, d):
        #     if state.isWin() or state.isLose():
        #         print "hit6"
        #         return self.evaluationFunction(state)
        #
        #     v = -1 * sys.maxint
        #
        #     for action in state.getLegalActions(agent):
        #         succ = state.generateSuccessor(agent, action)
        #         tempVal = 0
        #         print "min, depth",d
        #         print "min, agent",agent
        #         if agent >= succ.getNumAgents():
        #             #goto next depth
        #             print "min, next depth"
        #             agent = 0
        #             d += 1
        #             if d == self.depth:
        #                 print "hit7"
        #                 return self.evaluationFunction(succ)
        #
        #             if agent == self.index:
        #                 tempVal = max_value(succ, alpha, beta, agent + 1, d)
        #             else:
        #                 tempVal = min_value(succ, alpha, beta, agent + 1, d)
        #
        #         else:
        #             if d == self.depth:
        #                 print "hit8"
        #                 return self.evaluationFunction(succ)
        #
        #             if agent == self.index:
        #                 tempVal = max_value(succ, alpha, beta, agent + 1, d)
        #             else:
        #                 tempVal = min_value(succ, alpha, beta, agent + 1, d)
        #
        #         if tempVal < v:
        #             v = tempVal
        #
        #         if v < alpha:
        #             print "hit9"
        #             return v
        #
        #         beta = min(beta, v)
        #
        #         print "hit10"
        #         return v
        #
        #
        # #start with agent 0, depth 0
        # a = -1 * sys.maxint
        # b = sys.maxint
        # return max_value(gameState, a, b, 0, 0)


        level = 1
        maxVal = -1 * sys.maxint

        alpha = -1 * sys.maxint
        beta = sys.maxint

        take = gameState.getLegalActions(self.index)[0]
        for action in gameState.getLegalActions(self.index):
            next = gameState.generateSuccessor(self.index, action)
            cur = self.minValue(next, level, alpha, beta)
            if cur > maxVal:
                maxVal = cur
                take = action
        return take

    def maxValue(self, state, level, alpha, beta):

        num = state.getNumAgents()
        if state.isWin() or state.isLose() :
            return self.evaluationFunction(state)

        val = -1 * sys.maxint  #-inf

        if level == (num * self.depth):
            return self.evaluationFunction(state)

        level += 1

        for action in state.getLegalActions(self.index):


            next = state.generateSuccessor(self.index, action)

            val = max(val, self.minValue(next, level, alpha, beta))

            if val > beta:
                return val

            alpha = max(alpha, val)

        return val


    def minValue(self, state, level, alpha, beta):

        num = state.getNumAgents()
        if state.isWin() or state.isLose() :
            return self.evaluationFunction(state)

        val = sys.maxint  # inf

        if level == (num * self.depth):
            return self.evaluationFunction(state)

        level += 1


        for action in state.getLegalActions(self.index):
            next = state.generateSuccessor(self.index, action)

            if level % num != 0:
                val = min(val, self.minValue(next, level, alpha, beta))
            else:
                val = min(val, self.maxValue(next, level, alpha, beta))

            if val < alpha:
                return val

            beta = min(beta, val)

        return val



        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        # print  gameState.__dict__["data"].__dict__.keys()
        level = 1
        maxVal = -1 * sys.maxint

        take = gameState.getLegalActions(self.index)[0]
        for action in gameState.getLegalActions(self.index):
            next = gameState.generateSuccessor(self.index, action)
            cur = self.minValue(next, level)
            if cur > maxVal:
                maxVal = cur
                take = action
        return take

    def maxValue(self, state, level):

        num = state.getNumAgents()
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        val = -1 * sys.maxint  # -inf

        if level == (num * self.depth):
            return self.evaluationFunction(state)

        level += 1

        for action in state.getLegalActions(self.index):
            next = state.generateSuccessor(self.index, action)

            val = max(val, self.minValue(next, level))

        return val

    def minValue(self, state, level):

        num = state.getNumAgents()
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        val = 0.0

        if level == (num * self.depth):
            return self.evaluationFunction(state)

        level += 1

        for action in state.getLegalActions(self.index):
            next = state.generateSuccessor(self.index, action)

            if level % num != 0:
                val = (val + self.minValue(next, level)) / 1.0
            else:
                val = (val + self.maxValue(next, level)) / 1.0

        return val



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    util.raiseNotDefined()

    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


    total = successorGameState.getScore()
    x, y = newPos

    if newFood[x][y]:
        total += 200
    else:
        smallest = 1000;
        for i, each in enumerate(newFood.asList()):
            mDist = abs(x - each[0]) + abs(y - each[1])
            if mDist <= smallest:
                smallest = mDist
        # print "small: ", smallest,
        if (smallest > 1):
            total += 10 / (smallest)
        else:
            total += 95
    total += random.randint(20, 40);

    for i, each in enumerate(newGhostStates):
        gX, gY = newGhostStates[i].__dict__["configuration"].__dict__["pos"]

        mDist = abs(x - gX) + abs(y - gY)
        if newScaredTimes[i] < mDist + 5:
            if mDist < 2:
                return int(-50000)
            elif mDist < 3:
                total = (-2000 / (mDist))


        else:
            total += 410

    for each in currentGameState.__dict__["data"].__dict__["capsules"]:
        smallest = 1000;
        for i, each in enumerate(newFood.asList()):
            mDist = abs(x - each[0]) + abs(y - each[1])
            if mDist <= smallest:
                smallest = mDist
        # print "small: ", smallest,
        if (smallest > 1):
            total += 10 / (smallest)
        else:
            total += 100

    return total


# Abbreviation
better = betterEvaluationFunction
