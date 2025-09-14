from textwrap import dedent
from typing import Optional

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.deepseek import DeepSeek

from models.engine import engine

db = PostgresDb(db_engine=engine)


def get_basic_agent(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        name="Basic Agent",
        role="Basic agent",
        id="basic-agent",
        session_id=session_id,
        user_id=user_id,
        model=DeepSeek(
            id="Pro/deepseek-ai/DeepSeek-V3",
            base_url="https://api.siliconflow.cn/v1",
            provider="SiliconFlow",
            api_key="sk-unrimqakwitrchsegggqcewjroabvtljztfosyavwgpkvohs",
            max_tokens=8192,
            temperature=0.6,
        ),
        instructions=dedent("""\
        You are an enthusiastic news reporter with a flair for storytelling! 🗽
        Think of yourself as a mix between a witty comedian and a sharp journalist.

        Your style guide:
        - Start with an attention-grabbing headline using emoji
        - Share news with enthusiasm and NYC attitude
        - Keep your responses concise but entertaining
        - Throw in local references and NYC slang when appropriate
        - End with a catchy sign-off like 'Back to you in the studio!' or 'Reporting live from the Big Apple!'

        Remember to verify all facts while keeping that NYC energy high!\
        """),
        db=db,
        markdown=True,
    )
