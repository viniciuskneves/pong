import qlearn, math

class Learner:

    def __init__(self, ball, paddle_right):
        self.qlearner = qlearn.QLearn(actions=[1, -1])
        self.ball = ball
        self.paddle_right = paddle_right
        self.lastAction = None
        self.lastState = self.getState()
        self.lastScore = 0

    def learn(self, score):
        state = self.getState()
        reward = 0

        if score > self.lastScore: # Opponent scored
            reward = -10
        elif self.paddle_right.left == self.ball.right and self.paddle_right.top <= self.ball.top and self.paddle_right.bottom >= self.ball.bottom: # Paddle hitted the ball
            reward = 1

        self.qlearner.learn(self.lastState, self.lastAction, reward, state)

        direction = self.qlearner.chooseAction(state)
        print direction

        self.lastScore = score
        self.lastState = state
        return self.qlearner.chooseAction(state)

    def getState(self):
        line = 1 + (self.ball.y / 50) # Line state
        column = 1 + (self.ball.x / 20) # Column state (Max: 20)
        return (column, line) # (x, y)
