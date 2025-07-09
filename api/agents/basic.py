from typing import Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage

from models.engine import engine

basic_agent_storage = PostgresStorage(table_name="higgs-agents", db_engine=engine, auto_upgrade_schema=True)


def get_basic_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="Basic Agent",
        role="Basic agent",
        agent_id="basic-agent",
        session_id=session_id,
        user_id=user_id,
        model=OpenAIChat(
            id="deepseek-ai/DeepSeek-V3",
            base_url="https://api.siliconflow.cn/v1",
            api_key="sk-unrimqakwitrchsegggqcewjroabvtljztfosyavwgpkvohs",
            max_tokens=8192,
            temperature=0.6,
        ),
        storage=basic_agent_storage,
        add_history_to_messages=True,
        num_history_responses=5,
        add_datetime_to_instructions=True,
        markdown=True,
        debug_mode=debug_mode,
    )
