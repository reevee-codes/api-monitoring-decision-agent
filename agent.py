from dataclasses import dataclass
from decision.llm_decision import llm_decide
from environment import check_api

@dataclass
class AgentState:
    steps: int = 0
    ok_count: int = 0
    error_count: int = 0
    timeout_count: int = 0

class Agent:
    def __init__(self, goal):
        self.goal = goal
        self.state = AgentState()

    def observe(self):
        self.state.steps += 1
        status = check_api()
        print(f"[OBSERVE] API status: {status}")
        if status == "OK":
            self.state.ok_count += 1
        elif status == "ERROR":
            self.state.error_count += 1
        elif status == "TIMEOUT":
            self.state.timeout_count += 1
        return status

    def decide(self, observation):
        state_of_api = {"ok_count": self.state.ok_count,
                 "error_count": self.state.error_count,
                 "timeout_count": self.state.timeout_count,
                 "last_observation": observation}
        try:
            llm_return =  llm_decide(state_of_api)
            return llm_return["decision"]
        except Exception:
            pass
        if self.state.ok_count == 3:
            return "STOP"
        if self.state.error_count == 3:
            return "STOP"
        else:
            return "CONTINUE"

    def act(self, decision):
        print(
            f"Step {self.state.steps}, "
            f"ok: {self.state.ok_count}, "
            f"errors: {self.state.error_count}, "
            f"timeouts: {self.state.timeout_count}, "
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
