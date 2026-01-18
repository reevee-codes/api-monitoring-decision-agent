from environment import check_api


class Agent:
    def __init__(self, goal):
        self.goal = goal
        self.steps = 0
        self.ok_count = 0
        self.error_count = 0
        self.timeout_count = 0

    async def observe(self):
        self.steps += 1
        status = await check_api()
        print(f"[OBSERVE] API status: {status}")
        if status == "OK":
            self.ok_count += 1
        elif status == "ERROR":
            self.error_count += 1
        elif status == "TIMEOUT":
            self.timeout_count += 1
        return status

    def decide(self, observation):
        if self.ok_count == 3:
            return "STOP"
        if self.error_count == 3:
            return "STOP"
        else:
            return "CONTINUE"

    def act(self, decision):
        print(
            f"Step {self.steps}, "
            f"ok: {self.ok_count}, "
            f"errors: {self.error_count}, "
            f"timeouts: {self.timeout_count}, "
            f"decision: {decision}"
        )
        if decision == "STOP":
            return True
        else:
            return False

    def run(self):
        while True:
            observation = self.observe()
            decision = self.decide(observation)
            done = self.act(decision)

            if done:
                break
