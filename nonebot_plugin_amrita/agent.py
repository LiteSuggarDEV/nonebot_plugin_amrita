from __future__ import annotations

import typing

import typing_extensions
from amrita_core import (
    AgentRuntime as AmRuntime,
)
from amrita_core import (
    AgentStrategy,
    AmritaConfig,
    ChatObject,
    ModelPreset,
    PresetManager,
    SessionsManager,
    get_config,
)
from amrita_core.builtins.agent import AmritaAgentStrategy
from amrita_core.consts import DEFAULT_TEMPLATE
from amrita_core.sessions import SessionData
from amrita_core.types import Content, Message
from jinja2 import Template
from nonebot.adapters import Event
from nonebot.params import Depends

from nonebot_plugin_amrita.database import InsightsModel, make_id
from nonebot_plugin_amrita.lock import lock_by_session
from nonebot_plugin_amrita.memory import (
    AwaredMemory,
    CachedUserDataRepository,
    add_usage,
)


class AgentSession(AmRuntime):
    chat_objs: list[ChatObject]

    def __init__(
        self,
        config: AmritaConfig,
        preset: ModelPreset,
        train: dict[str, str] | Message[str],
        strategy: type[AgentStrategy] = AmritaAgentStrategy,
        template: Template | str = DEFAULT_TEMPLATE,
        session: SessionData | str | None = None,
        no_session: bool = False,
    ):
        super().__init__(config, preset, train, strategy, template, session, no_session)
        self.chat_objs = []

    async def __aenter__(self) -> typing_extensions.Self:
        return self

    async def __aexit__(self, exc_type, exc, tb):
        del exc_type, exc, tb
        uni_id = self.session_id
        if not self.chat_objs:
            return
        async with lock_by_session(uni_id):  # Thread safe
            dm = CachedUserDataRepository()
            metadata = await dm.get_metadata(uni_id)
            insight = await InsightsModel.get()
            for chat_object in self.chat_objs:
                if chat_object.response.usage:
                    add_usage(metadata, chat_object.response.usage)
                    add_usage(insight, chat_object.response.usage)
            await insight.save()
            await dm.update_metadata(metadata)

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

    @typing_extensions.override
    def get_chatobject(
        self, user_input: typing.Sequence[Content] | str | None, **kwargs
    ) -> ChatObject:
        obj = super().get_chatobject(user_input, **kwargs)
        self.chat_objs.append(obj)
        return obj


def SessionDepends(
    train: Message[str] | dict[str, str],
    config: AmritaConfig | None = None,
    preset: ModelPreset | None = None,
    **kwargs,
):
    async def constructor(event: Event) -> AgentSession:
        return await AgentSession.load_from(event, train, config, preset, **kwargs)

    return Depends(constructor)
