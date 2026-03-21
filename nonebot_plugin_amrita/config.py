
from typing import Literal

from amrita_core.config import random_alnum_string
from pydantic import BaseModel, Field


class Config(BaseModel):
    #  CookieConfig
    amrita_cookie_enable: bool = False
    amrita_cookie: str = Field(default_factory=lambda: random_alnum_string(16))
    # FunctionConfig
    amrita_mcp_enable: bool = False
    amrita_mcp_clients: list[str] = Field(default_factory=list)
    amrita_tool_call_limit: int = 15
    # LLMConfig
    amrita_memory_token_limit: int = 2048
    amrita_memory_length: int = 50
    amrita_prompt_token_limit: int = 256
    # BuiltinAgentConfig
    amrita_agent_mode:Literal["agent", "rag", "none"] = "agent"
    amrita_agent_thought_mode: Literal[
        "reasoning", "chat", "reasoning-required", "reasoning-optional"
    ] = "reasoning"
