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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        "*** YOUR CODE HERE ***"
        
        ghostDistances = []
        foodDistances = []
        score = 0
        
        for ghost in successorGameState.getGhostPositions():
            ghostDistances.append(util.manhattanDistance(ghost,newPos))
        
        for food in newFood.asList():
            foodDistances.append(util.manhattanDistance(food,newPos))

        for ghostDistance in ghostDistances:
            if ghostDistance < 3.5: score -= 1
            if ghostDistance < 1.5: score -= 20

        for foodDistance in foodDistances:
            if foodDistance < 3.5: score += 0.3
            if foodDistance < 1.5: score += 1.5
        

        return successorGameState.getScore() + score


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
        pValue = -float("inf")
        pAction = Directions.STOP
        
        for action in gameState.getLegalActions(0): 
            nextState = gameState.generateSuccessor(0,action)
            nextValue = self.getValue(nextState, 0 ,1)
            
            if nextValue > pValue:
                pValue = nextValue
                pAction = action
                
        return pAction
        
        
    def getValue (self,gameState ,currentDepth, agentIndex):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():   
            return self.evaluationFunction (gameState)
        elif agentIndex == 0:
            return self.getPacmanValue(gameState,currentDepth)
        else:   
            return self.getGhostValue(gameState, currentDepth, agentIndex)
        
    def getPacmanValue (self, gameState,currentDepth):
        pValue = -float("inf")
        for pAction in gameState.getLegalActions(0):
            pValue = max ( pValue, self.getValue(gameState.generateSuccessor(0,pAction),currentDepth,1))
        
        return pValue
    
    def getGhostValue (self, gameState,currentDepth,aIndex):
        gValue = float("inf")
        for gAction in gameState.getLegalActions(aIndex):
            lastAgent = gameState.getNumAgents() - 1
            if aIndex == lastAgent :
                gValue = min(gValue, self.getValue(gameState.generateSuccessor(aIndex,gAction) , currentDepth+1 ,0))
            else:
                gValue = min(gValue, self.getValue(gameState.generateSuccessor(aIndex,gAction) , currentDepth, aIndex+1))
        
        return gValue


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        pValue = - float("inf")
        pAction = Directions.STOP
        alpha = - float("inf")
        beta = float("inf")
        
        for action in gameState.getLegalActions(0): 
            nextState = gameState.generateSuccessor(0,action)
            nextValue = max(pValue,self.getValue(nextState, 0 ,1 ,alpha,beta))
            
            if nextValue > alpha:
                alpha = nextValue
                pAction = action
                
        return pAction
        
        
    def getValue (self,gameState ,currentDepth,agentIndex,alpha,beta):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():   
            return self.evaluationFunction (gameState)
        elif agentIndex == 0:
            return self.getPacmanValue(gameState,currentDepth,alpha,beta)
        else:   
            return self.getGhostValue(gameState, currentDepth, agentIndex,alpha,beta)
        
    def getPacmanValue (self, gameState,currentDepth,alpha,beta):
        pValue = -float("inf")
        for pAction in gameState.getLegalActions(0):
            pValue = max (pValue, self.getValue(gameState.generateSuccessor(0,pAction),currentDepth,1,alpha,beta))
        
            
            if pValue > beta: return pValue
            alpha = max(alpha,pValue)
            
            
        return pValue
    
    def getGhostValue (self, gameState,currentDepth,aIndex,alpha,beta):
        gValue = float("inf")
        lastAgent = gameState.getNumAgents() - 1

        if aIndex == lastAgent :
            d = currentDepth +1
            idx = 0
        else:
            d = currentDepth
            idx = aIndex+1
       
        for gAction in gameState.getLegalActions(aIndex):
            gValue = min(gValue, self.getValue(gameState.generateSuccessor(aIndex,gAction) , d , idx, alpha, beta))
            
            if gValue < alpha: return gValue
            beta = min (beta,gValue)
            
        return gValue

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
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
