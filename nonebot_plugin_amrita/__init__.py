import asyncio
import contextlib
import sys

import amrita_core
from amrita_core import ChatManager, ChatObject, minimal_init
from amrita_core.config import (
    AmritaConfig,
    BuiltinAgentConfig,
    CookieConfig,
    FunctionConfig,
    LLMConfig,
)
from nonebot import get_driver, get_plugin_config, logger
from nonebot import log as nb_log
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="NoneBot2的AmritaCore支持库",
    description="Add AmritaCore support to nonebot",
    usage="View `https://amrita-core.suggar.top/zh` for details.",
    type="library",
    config=Config,
    supported_adapters=None,
)

_config = get_plugin_config(Config)


def _patch_logger():
    logger.remove()
    nb_log.logger_id = logger.add(
        sys.stdout,
        level=0,
        diagnose=False,
        filter=nb_log.default_filter,
        format=nb_log.default_format,
    )
    amrita_core.logging.logger_id = nb_log.logger_id


_patch_logger()  # AmritaCore会修改Loguru的配置，这里重置为NoneBot2的默认配置


def replace_config(config: Config):
    global _config
    if not isinstance(config, Config):
        raise TypeError("config must be Config")
    _config = config


@get_driver().on_startup
async def init():
    global _config
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
