class Agent:
    def __init__(self, goal):
        self.goal = goal
        self.steps = 0

    def observe(self):
        self.steps += 1
        return "OK"

    def decide(self, observation):
        return "STOP"

    def act(self, decision):
        print(f"Decision: {decision}")
        return True

    def run(self):
        while True:
            observation = self.observe()
            decision = self.decide(observation)
            done = self.act(decision)

            if done:
                break
