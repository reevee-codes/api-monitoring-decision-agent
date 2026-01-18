from decision.llm_decision import llm_decide
from environment import check_api


class Agent:
    def __init__(self, goal):
        self.goal = goal
        self.steps = 0
        self.ok_count = 0
        self.error_count = 0
        self.timeout_count = 0

    def observe(self):
        self.steps += 1
        status = check_api()
        print(f"[OBSERVE] API status: {status}")
        if status == "OK":
            self.ok_count += 1
        elif status == "ERROR":
            self.error_count += 1
        elif status == "TIMEOUT":
            self.timeout_count += 1
        return status

    def decide(self, observation):
        state = {"ok_count": self.ok_count,
                 "error_count": self.error_count,
                 "timeout_count": self.timeout_count,
                 "last_observation": observation}
        try:
            llm_return =  llm_decide(state)
            return llm_return["decision"]
        except Exception:
            pass
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
