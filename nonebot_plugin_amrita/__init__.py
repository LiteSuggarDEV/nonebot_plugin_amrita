import asyncio
import contextlib
import sys

from nonebot import require

require("nonebot_plugin_localstore")
require("nonebot_plugin_orm")

import amrita_core
from amrita_core import ChatManager, ChatObject, minimal_init
from amrita_core.config import (
    AmritaConfig,
    BuiltinAgentConfig,
    CookieConfig,
    FunctionConfig,
    LLMConfig,
)
from nonebot import get_driver, logger
from nonebot import log as nb_log
from nonebot.plugin import PluginMetadata

from . import agent, database, dirty, memory
from . import config as conf_module
from .config import Config
from .database import InsightsModel, UserDataExecutor
from .memory import CachedUserDataRepository, MemorySchema

__plugin_meta__ = PluginMetadata(
    name="LibAmritaCore",
    description="Add AmritaCore (a high performance agent core) support to nonebot2",
    usage="View `https://amrita-core.suggar.top/zh` for details.",
    type="library",
    homepage="https://github.com/LiteSuggarDEV/nonebot_plugin_amrita",
    config=Config,
    supported_adapters=None,
)


def _patch_logger():
    amrita_core.logging.logger.remove()

    amrita_core.logging.logger_id.value = amrita_core.logger.add(
        sys.stdout,
        level=0,
        diagnose=False,
        filter=nb_log.default_filter,
        format=nb_log.default_format,
    )


_patch_logger()  # 为了规范化日志输出，我们把AmritaCore的本身的logger替换掉（它是独立的logger对象）。


def replace_config(config: Config):

    if not isinstance(config, Config):
        raise TypeError("config must be Config")
    conf_module._config = config


@get_driver().on_startup
async def init():
    _config = conf_module._config
    am_cookie_conf = CookieConfig(
        enable_cookie=_config.amrita_cookie_enable, cookie=_config.amrita_cookie
    )
    am_function_conf = FunctionConfig(
        agent_mcp_client_enable=_config.amrita_mcp_enable,
        agent_mcp_server_scripts=_config.amrita_mcp_clients,
        agent_tool_call_limit=_config.amrita_tool_call_limit,
    )
    am_builtin_conf = BuiltinAgentConfig(
        tool_calling_mode=_config.amrita_agent_mode,
        agent_thought_mode=_config.amrita_agent_thought_mode,
    )
    am_llm_conf = LLMConfig(
        memory_length_limit=_config.amrita_memory_length,
        session_tokens_windows=_config.amrita_memory_token_limit,
        max_tokens=_config.amrita_prompt_token_limit,
    )
    am_conf = AmritaConfig(
        cookie=am_cookie_conf,
        function_config=am_function_conf,
        builtin=am_builtin_conf,
        llm=am_llm_conf,
    )
    await minimal_init(am_conf)


@get_driver().on_shutdown
async def shutdown():
    logger.info("Shutting down AmritaCore...")

    async def kill_all(objs: list[ChatObject]):
        for obj in objs:
            with contextlib.suppress(Exception):
                obj.terminate()

    await asyncio.gather(
        *[kill_all(objs) for objs in ChatManager().running_chat_object.values()],
        return_exceptions=True,
    )


__all__ = [
    "CachedUserDataRepository",
    "ChatManager",
    "ChatObject",
    "InsightsModel",
    "MemorySchema",
    "UserDataExecutor",
    "agent",
    "database",
    "dirty",
    "memory",
]
