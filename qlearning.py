import random

class QLearning:
    def __init__(self, ball, paddle):
        self.ball = ball
        self.paddle = paddle

        self.actions = [-1, 0, 1]
        self.epsilon = 1 # Exploration factor
        self.epsilonDecrement = 0.0000001
        self.epsilonMin = 0.1
        self.alpha = 1 # Learning factor
        self.alphaDecrement = 0.0000001
        self.gamma = 0.9
        self.previousLine = None
        self.previousColumn = None
        self.q = {}

    def setLearning(self, state, action, reward, newState):
        if self.alpha > 0.01:
            self.alpha -= self.alphaDecrement

        maxQ = max([self.q.get((newState, a), 0) for a in self.actions])
        previousWeight = self.q.get((state, action), 0)

        nextWeight = previousWeight + self.alpha * (reward + (self.gamma * maxQ - previousWeight))
        self.q[(state, action)] = nextWeight

    def getReward(self, previousScore, newScore, previousDirection, newDirection):
        if newScore > previousScore:
            return -10
        elif previousDirection <> newDirection:
            return 100
        else:
            ballLine = self.getBallLine()
            paddleLine = self.getPaddleLine()
            if ballLine == paddleLine:
                return 10
            else:
                return -1 * abs(ballLine - paddleLine)

    def getAction(self, state):
        if (self.epsilon > self.epsilonMin):
            self.epsilon -= self.epsilonDecrement

        if random.random() < self.epsilon: # Exploration
            return random.choice(self.actions)
        else:
            return max([self.q.get((state, a), 0) for a in self.actions])

    def getPaddleLine(self):
        #return self.paddle.centery / 50
        return self.paddle.centery / 25
        #return self.paddle.centery

    def getBallLine(self):
        #return self.ball.centery / 50 # 6 lines
        #return self.ball.centery / 25 # 6 lines
        return self.ball.centery / 25 # 6 lines
        #return self.ball.centery

    def getBallColumn(self):
        #return self.ball.centerx / 20 # 20 columns
        return self.ball.centerx / 10 # 20 columns
        #return self.ball.centerx

    def getState(self, direction_y):
        line = self.getBallLine()
        column = self.getBallColumn()
        position = self.getPaddleLine() # Paddle position
        return (line, column, position, direction_y)

    def printQ(self):
        print self.q
        print self.q.values()
