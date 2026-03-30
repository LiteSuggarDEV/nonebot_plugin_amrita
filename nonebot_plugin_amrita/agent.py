from __future__ import annotations

import typing

from amrita_core import (
    AgentRuntime as AmRuntime,
)
from amrita_core import (
    AmritaConfig,
    ModelPreset,
    PresetManager,
    SessionsManager,
    get_config,
)
from amrita_core.types import Message
from nonebot.adapters import Event

from nonebot_plugin_amrita.database import make_id
from nonebot_plugin_amrita.memory import AwaredMemory, CachedUserDataRepository


class AgentSession(AmRuntime):
    @classmethod
    async def load_from(
        cls,
        id_or_event: Event | str,
        train: Message[str] | dict[str, str],
        config: AmritaConfig | None = None,
        preset: ModelPreset | None = None,
        **kwargs,
    ) -> AgentSession:
        uni_id = make_id(id_or_event)
        dm = CachedUserDataRepository()
        memory = await dm.get_memory(uni_id)
        config = config or get_config()
        preset = preset or PresetManager().get_default_preset()
        SessionsManager().init_session(uni_id)
        session = SessionsManager().get_session_data(uni_id)
        session.memory = memory.memory_json
        return cls(config, preset, train, session=session, **kwargs)

    async def save_context(self):
        session_id = self.session_id
        dm = CachedUserDataRepository()
        context: AwaredMemory = typing.cast(AwaredMemory, self.context)
        mem = await dm.get_memory(session_id)
        mem.memory_json = context
        await dm.update_memory_data(mem)
