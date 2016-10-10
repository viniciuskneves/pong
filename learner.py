import qlearn, math

class Learner:

    def __init__(self, ball, paddle_right):
        #self.qlearner = qlearn.QLearn(actions=[0, 1, 2, 3, 4, 5])

        self.qlearner = qlearn.QLearn(actions=[-1, 0, 1])
        self.ball = ball
        self.paddle_right = paddle_right
        self.lastAction = None
        self.lastState = (1 + ball.y / 50, 1 + ball.x / 20, None, None, 1 + (self.paddle_right.y / 50))
        self.lastScore = 0

    def learn(self, score, direction, i):
        state = self.getState(direction)
        
        if self.lastState <> state:
            reward = 0

            if score > self.lastScore: # Opponent scored
                reward = -100
            elif self.paddle_right.left == self.ball.right and self.paddle_right.top <= self.ball.top and self.paddle_right.bottom >= self.ball.bottom: # Paddle hitted the ball
                reward = 50

            self.qlearner.learn(self.lastState, self.lastAction, reward, state)

            action, q = self.qlearner.chooseAction(state, True);

            self.lastScore = score
            self.lastState = state
            self.lastAction = action

            return action
        elif direction == -1:
            return 0
        else:
            return self.lastAction

    def getState(self, direction):
        line_old = self.lastState[1]
        column_old = self.lastState[0]
        line = 1 + (self.ball.y / 50) # Line state
        column = 1 + (self.ball.x / 20) # Column state (Max: 20)
        paddle_position = 1 + (self.paddle_right.y / 50)
        if line_old == line and column_old == column:
            return self.lastState
        else:
            return (column, line, column_old, line_old, paddle_position)

    def printQ(self):
       print self.qlearner.getAllQ() 
