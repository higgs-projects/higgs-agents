from agno.playground import Playground

# Import agents
from agents.basic import get_basic_agent
from configs import higgs_config

# Import workflows

# Import teams

######################################################
## Router for the agent playground
######################################################

basic_agent = get_basic_agent(debug_mode=True)

# Create a playground instance
playground = Playground(
    agents=[basic_agent],
)

# Log the playground endpoint with app.agno.com
if higgs_config.DEPLOY_ENV == "dev":
    playground.register_app_on_platform()

playground_router = playground.get_router()
