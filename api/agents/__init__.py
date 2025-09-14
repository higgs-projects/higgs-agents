from agents.basic import get_basic_agent


def get_agents() -> list:
    basic_agent = get_basic_agent(debug_mode=True)
    return [basic_agent]