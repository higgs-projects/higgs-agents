from os import getenv

from agno.playground import Playground

# Import agents
from agents.basic import get_basic_agent
from controllers.service_api import service_api_router

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
if getenv("RUNTIME_ENV") == "dev":
    playground.register_app_on_platform()

playground_router = playground.get_router()
service_api_router.include_router(playground_router)