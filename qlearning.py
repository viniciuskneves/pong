import random, ast
from math import copysign

class QLearning:
    def __init__(self, ball, paddle):
        self.ball = ball
        self.paddle = paddle

        self.actions = [-1, 0, 1]
        self.epsilon = 1 # Exploration factor
        #self.epsilon = 0 # Exploration factor
        self.epsilonDecrement = 0.0000001
        self.epsilonMin = 0.1
        self.alpha = 1 # Learning factor
        self.alphaDecrement = 0.0000001
        self.gamma = 0.9
        self.previousLine = None
        self.previousColumn = None
        self.q = {}
        #with open('states7', 'r') as f:
            #val = f.read()
            #self.q = ast.literal_eval(val)

        self.ball_centery = ball.centery
        self.paddle_centery = paddle.centery

    def setLearning(self, state, action, reward, newState):
        if self.alpha > 0.01:
            self.alpha -= self.alphaDecrement

        maxQ = max([self.q.get((newState, a), 0) for a in self.actions])
        previousWeight = self.q.get((state, action), 0)

        nextWeight = previousWeight + self.alpha * (reward + (self.gamma * maxQ - previousWeight))
        self.q[(state, action)] = nextWeight

    def getReward(self):
        old_distance = abs(self.paddle_centery - self.ball_centery)
        paddle_centery = self.paddle.centery
        ball_centery = self.ball.centery
        new_distance = abs(paddle_centery - ball_centery)
        if new_distance < old_distance:
            reward = 1
        else:
            reward = -1
        self.paddle_centery = paddle_centery
        self.ball_centery = ball_centery
        return reward

    def getAction(self, state):
        if (self.epsilon > self.epsilonMin):
            self.epsilon -= self.epsilonDecrement

        if random.random() < self.epsilon: # Exploration
            return random.choice(self.actions)
        else:
            return max([self.q.get((state, a), 0) for a in self.actions])

    def getPaddleLine(self):
        return self.paddle.centery / 25

    def getBallLine(self):
        return self.ball.centery / 25 # 6 lines

    def getState(self, direction_y):
        line = self.getBallLine()
        position = self.getPaddleLine() # Paddle position
        return (line, position, direction_y)

    def printQ(self):
        print self.q
