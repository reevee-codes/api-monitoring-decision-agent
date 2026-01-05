from agent import Agent

def test_ok_count(mocker):
    mocker.patch("environment.check_api", return_value="OK")
    agent = Agent(goal="whatever")
    agent.run()
    assert agent.ok_count == 3