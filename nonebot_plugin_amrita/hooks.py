from amrita_core import ChatObject, CompletionEvent, on_completion

from nonebot_plugin_amrita.database import InsightsModel
from nonebot_plugin_amrita.lock import lock_by_session
from nonebot_plugin_amrita.memory import CachedUserDataRepository, add_usage


@on_completion(block=False).handle()
async def usage_update(event: CompletionEvent):
    chat_object: ChatObject = event.chat_object
    uni_id: str = chat_object.session_id
    async with lock_by_session(uni_id): # Thread safe
        dm = CachedUserDataRepository()
        metadata = await dm.get_metadata(uni_id)
        insight  = await InsightsModel.get()
        if chat_object.response.usage:
            add_usage(metadata, chat_object.response.usage)
            add_usage(insight, chat_object.response.usage)
            await insight.save()
            await dm.update_metadata(metadata)
