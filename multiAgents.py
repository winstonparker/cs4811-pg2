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

        #stop action is not optimal so we try to avoid it
        if action == "Stop":
            return -10;

        #starting total
        total = successorGameState.getScore()

        #new position of pacman
        x, y = newPos

        #old position of pacman
        curX, curY  = currentGameState.__dict__["data"].__dict__["agentStates"][0].__dict__["configuration"].__dict__ ["pos"]

        #go to the food if its the next pos
        if newFood[x][y]:
            total += 200
        else:

            #find closest food
            smallest = 1000;
            for i, each in enumerate(newFood.asList()):
                mDist = abs(x - each[0]) + abs(y - each[1])
                if mDist <= smallest:
                    smallest = mDist

            if(smallest > 1):
                total += 10 / (smallest)
            else:
                total += 95

        #choose random food when costs are equal
        total += random.randint(20, 40);

        #go through ghost states to find if they are near by
        for i, each in enumerate(newGhostStates):
            gX, gY  = newGhostStates[i].__dict__["configuration"].__dict__ ["pos"]

            #manh. dist.
            mDist = abs(x-gX) + abs(y-gY)

            #if check if they are scared
            if newScaredTimes[i] < mDist + 5:

                #dont do near if they are not scared
                if mDist < 2:
                    return int(-50000)

                elif mDist < 3:
                    # print ("factoring ghost")

                    total = ( -2000 / ( mDist))
                # else:
                    # print ("not factoring ghost")

            else:
                #go after them if they are scared
                total += 410

        #hunt the pods
        for each in currentGameState.__dict__["data"].__dict__["capsules"]:
            smallest = 1000;
            #find closest one
            for i, each in enumerate(newFood.asList()):
                mDist = abs(x - each[0]) + abs(y - each[1])
                if mDist <= smallest:
                    smallest = mDist

            #find closest
            if (smallest > 1):
                total += 10 / (smallest)
            else:
                total += 100

        return total



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
        self.calls = 0;
        self.cur = 0;

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

        #starting level
        level = 1

        #max node val
        maxVal = -1 * sys.maxint

        #state to take
        take = gameState.getLegalActions(self.index)[0]

        #get max of starting actions
        for action in gameState.getLegalActions(self.index):

            #get next node for each action
            next = gameState.generateSuccessor(0, action)

            #if ghost, set index to 1st ghost
            if gameState.getNumAgents() > 1:
                self.cur = 1
            else:
                self.cur = 0

            #get max val for this action
            cur = self.minValue(next, level)

            #penalty for stopping
            if action == "Stop":
                cur -= 1
            #check if this value is a new max and update choosen action
            if cur > maxVal:
                maxVal = cur
                take = action

        #return action with maxVal
        return take




    def maxValue(self, state, level):

        #number of agents
        num = state.getNumAgents()

        #check if winning case
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        #max value
        val = -1 * sys.maxint  # -inf

        #return if at depth limit
        if level == (num * self.depth):
            return self.evaluationFunction(state)

        #go to next level
        level += 1

        #get index of current agent
        temp = self.cur

        #get max of action of current agent
        for action in state.getLegalActions(temp):

            #get state of this action
            next = state.generateSuccessor(temp, action)

            #update agent if >= 1 ghosts
            if state.getNumAgents() > 1:
                self.cur = 1
            else:
                self.cur = 0

            #ypdate max val
            val = max(val, self.minValue(next, level))

        return val

    def minValue(self, state, level):

        #number of agests
        num = state.getNumAgents()

        #check if state is winner
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        #min value
        val = sys.maxint  # inf

        #check if at max depth
        if level == (num * self.depth):
            return self.evaluationFunction(state)

        #go to next level
        level += 1

        #save index of current agent
        temp = self.cur

        #go through agent's actions
        for action in state.getLegalActions(temp):

            #get state of agent action
            next = state.generateSuccessor(temp, action)

            #check if ghost action, if so find the min and do another min, else, do a min on a max
            if level % num != 0:
                self.cur = level % num
                val = min(val, self.minValue(next, level))
            else:
                self.cur = 0;
                val = min(val, self.maxValue(next, level))

        #return min
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

        level = 1
        maxVal = -1 * sys.maxint
        # cur = -1 * sys.maxint

        alpha = -1 * sys.maxint
        beta = sys.maxint

        take = gameState.getLegalActions(self.index)[0]
        for action in gameState.getLegalActions(self.index):


            next = gameState.generateSuccessor(0, action)
            if gameState.getNumAgents() > 1:
                self.cur = 1
            else:
                self.cur = 0

            cur = self.minValue(next, level, alpha, beta)

            if cur > maxVal:
                maxVal = cur
                take = action

            #is there a conflict? if so prune!
            if cur > beta:
                return take

            #set alpha
            alpha = max(alpha, cur)

        return take

    def maxValue(self, state, level, alpha, beta):

        num = state.getNumAgents()
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        val = -1 * sys.maxint  # -inf

        if level == (num * self.depth):
            return self.evaluationFunction(state)

        level += 1

        temp = self.cur
        for action in state.getLegalActions(temp):


            next = state.generateSuccessor(temp, action)
            if state.getNumAgents() > 1:
                self.cur = 1
            else:
                self.cur = 0
            val = max(val, self.minValue(next, level, alpha, beta))

            #is there a conflict? if so prune!
            if val > beta:
                return val

            #set AlphaBetaAgent
            alpha = max(alpha, val)

        return val

    def minValue(self, state, level, alpha, beta):
        num = state.getNumAgents()

        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        val = sys.maxint  # inf

        if level == (num * self.depth):
            return self.evaluationFunction(state)

        level += 1

        temp = self.cur
        for action in state.getLegalActions(temp):

            next = state.generateSuccessor(temp, action)

            if level % num != 0:
                self.cur = level % num
                val = min(val, self.minValue(next, level, alpha, beta))
            else:
                self.cur = 0;
                val = min(val, self.maxValue(next, level, alpha, beta))

            #is there a conflict? if so prune!
            if val < alpha:
                return val

            #set beta
            beta = min(beta, val)


        return val

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
        # starting level
        level = 1

        # max node val
        maxVal = -1 * sys.maxint

        # state to take
        take = gameState.getLegalActions(self.index)[0]

        # get max of starting actions
        for action in gameState.getLegalActions(self.index):

            # get next node for each action
            next = gameState.generateSuccessor(0, action)

            # if ghost, set index to 1st ghost
            if gameState.getNumAgents() > 1:
                self.cur = 1
            else:
                self.cur = 0

            # get max val for this action
            cur = self.avgValue(next, level)

            # penalty for stopping
            if action == "Stop":
                cur -= 100
            # check if this value is a new max and update choosen action
            if cur > maxVal:
                maxVal = cur
                take = action

        # return action with maxVal
        return take




    def maxValue(self, state, level):

        #number of agents
        num = state.getNumAgents()

        #check if winning case
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        #max value
        val = -1 * sys.maxint  # -inf

        #return if at depth limit
        if level == (num * self.depth):
            return self.evaluationFunction(state)

        #go to next level
        level += 1

        #get index of current agent
        temp = self.cur

        #get max of action of current agent
        for action in state.getLegalActions(temp):

            #get state of this action
            next = state.generateSuccessor(temp, action)

            #update agent if >= 1 ghosts
            if state.getNumAgents() > 1:
                self.cur = 1
            else:
                self.cur = 0

            #ypdate max val
            val = max(val, self.avgValue(next, level))

        return val

    def avgValue(self, state, level):
        num = state.getNumAgents()

        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        if level == (num * self.depth):
            return self.evaluationFunction(state)

        level += 1

        temp = self.cur
        vals = []
        for action in state.getLegalActions(temp):

            next = state.generateSuccessor(temp, action)

            if level % num != 0:
                self.cur = level % num
                vals.append(self.avgValue(next, level))
            else:
                self.cur = 0;
                vals.append(self.maxValue(next, level))

        return sum(vals) / float(len(vals))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: We check distance to closest food, amount of food left, pod distance, ghost distance, and scared timer. We give each a different value
      based on it's impact to the score
    """

    current_pos = currentGameState.getPacmanPosition()

    #get food and capsules
    food_list = currentGameState.getFood().asList()
    cap_list = currentGameState.getCapsules()

    #nubmer of foods left
    food_left = len(food_list)

    #number of capsules left
    capsules_left = len(currentGameState.getCapsules())

    #distance to closest food
    food_distance = sys.maxint
    for cur_cap in cap_list:
        tf_distance = util.manhattanDistance(current_pos, cur_cap)
        if tf_distance < food_distance:
            food_distance = tf_distance
    for cur_food in food_list:
        tf_distance = util.manhattanDistance(current_pos, cur_food)
        if tf_distance < food_distance:
            food_distance = tf_distance


    scared_ghosts = 0
    normal_ghosts = 0

    #check if there are scared ghosts and normal ghosts
    for ghost in currentGameState.getGhostStates():
        if ghost.scaredTimer:
            scared_ghosts = 1
        else:
            normal_ghosts = 1

    #set arbitrary distance accordingly
    if scared_ghosts == 1:
        vul_ghost_distance = sys.maxint
    else:
        vul_ghost_distance = 0

    if normal_ghosts == 1:
        reg_ghost_distance = sys.maxint
    else:
        reg_ghost_distance = 0

    #look at all the ghosts
    for ghost in currentGameState.getGhostStates():
        #found a scared ghost
        if ghost.scaredTimer:
            #get the distance to that scared ghost and check if it is closer than already found scared ghost
            t_vul_ghost_distance = util.manhattanDistance(current_pos, ghost.getPosition())
            if t_vul_ghost_distance < vul_ghost_distance:
                vul_ghost_distance = t_vul_ghost_distance

        #ghost is not scared
        else:
            #get the distance to that normal ghost and check if it is closer than already found ghost
            t_reg_ghost_distance = util.manhattanDistance(current_pos, ghost.getPosition())
            if t_reg_ghost_distance < reg_ghost_distance:
                reg_ghost_distance = t_reg_ghost_distance

    #add weights too all of these values to make pacman prioritize different states
    total = currentGameState.getScore() #base score
    total += (2 / food_distance) #travel to food (prioritize closer food)
    total += (7 * food_left) #prioritize collecting food
    total += (50 * capsules_left) #pick it up
    total += (2 * vul_ghost_distance) #chase scared ghosts
    total += (10 * (reg_ghost_distance / 100))  #dont want to go there
    return total

# Abbreviation
better = betterEvaluationFunction
