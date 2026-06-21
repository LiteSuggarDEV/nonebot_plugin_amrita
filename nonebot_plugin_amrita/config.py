from amrita_core.config import random_alnum_string
from nonebot import get_plugin_config
from pydantic import BaseModel, Field


class Config(BaseModel):
    #  CookieConfig
    amrita_cookie_enable: bool = False
    amrita_cookie: str = Field(default_factory=lambda: random_alnum_string(16))
    # FunctionConfig
    amrita_mcp_enable: bool = False
    amrita_mcp_clients: list[str] = Field(default_factory=list)
    amrita_metadata_cache_size: int = 2048
    amrita_memory_cache_size: int = 512
    amrita_lockpool_size: int = 1024


_config = get_plugin_config(Config)


def config() -> Config:
    return _config
