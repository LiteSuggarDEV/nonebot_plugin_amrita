# LibAmritaCore

**LibAmritaCore：把下一代高性能 Agent 内核，带入 NoneBot2 生态。**

## 介绍

此插件为 NoneBot2 生态提供 **AmritaCore** 原生支持。
AmritaCore 是一套开源、轻量、高性能的下一代 Agent 运行时内核，提供可中断、可自省、可恢复的现代化 AI 执行环境。

了解更多：

- 📖 [官方文档](https://core.amritabot.com/zh)
- 🧩 [GitHub](https://github.com/AmritaBot/AmritaCore)

---

## 快速开始

### 安装插件

```bash
nb plugin install nonebot_plugin_amrita
```

### 配置插件

配置均遵循 NoneBot2 标准的配置体系。

#### Cookie 配置

| 配置项                 | 类型   | 默认值         | 说明                               |
| ---------------------- | ------ | -------------- | ---------------------------------- |
| `amrita_cookie_enable` | `bool` | `False`        | 是否启用 Cookie 鉴权               |
| `amrita_cookie`        | `str`  | 随机16位字符串 | 插件内部安全密钥（启用后自动生成） |

#### 功能配置

| 配置项                   | 类型        | 默认值  | 说明                                   |
| ------------------------ | ----------- | ------- | -------------------------------------- |
| `amrita_mcp_enable`      | `bool`      | `False` | 是否启用 MCP（Model Context Protocol） |
| `amrita_mcp_clients`     | `list[str]` | `[]`    | MCP 客户端脚本路径列表                 |
| `amrita_tool_call_limit` | `int`       | `15`    | 单轮工具调用最大次数限制               |

#### LLM 内存配置

| 配置项                      | 类型  | 默认值 | 说明                    |
| --------------------------- | ----- | ------ | ----------------------- |
| `amrita_memory_token_limit` | `int` | `2048` | 对话记忆窗口 Token 上限 |
| `amrita_memory_length`      | `int` | `50`   | 最大保留对话条数        |
| `amrita_prompt_token_limit` | `int` | `256`  | 系统提示词 Token 上限   |

#### 内置 Agent 行为配置

| 配置项                      | 类型                     | 默认值      | 说明                                        |
| --------------------------- | ------------------------ | ----------- | ------------------------------------------- |
| `amrita_agent_mode`         | `agent / rag / none`     | `agent`     | 运行模式：智能体 / 检索生成 / 纯对话        |
| `amrita_agent_thought_mode` | `reasoning / chat / ...` | `reasoning` | 思考模式：推理 / 对话 / 强制推理 / 可选推理 |

#### 高性能缓存配置

| 配置项                       | 类型  | 默认值 | 说明                            |
| ---------------------------- | ----- | ------ | ------------------------------- |
| `amrita_metadata_cache_size` | `int` | `2048` | 用户元数据缓存大小              |
| `amrita_memory_cache_size`   | `int` | `512`  | 用户记忆缓存大小                |
| `amrita_lockpool_size`       | `int` | `1024` | 并发锁池大小（支持动态 resize） |

---

## 配置示例（.env）

```env
AMRITA_COOKIE_ENABLE=true
AMRITA_MCP_ENABLE=true
AMRITA_MCP_CLIENTS='["client1","client2"]'
AMRITA_TOOL_CALL_LIMIT=20
AMRITA_MEMORY_TOKEN_LIMIT=3072
AMRITA_MEMORY_LENGTH=100
AMRITA_PROMPT_TOKEN_LIMIT=512
AMRITA_AGENT_MODE=agent
AMRITA_AGENT_THOUGHT_MODE=reasoning
```

---

## 开发指南

### 基本使用

#### 导入核心组件

```python
from nonebot_plugin_amrita.agent import AgentSession, SessionDepends
from amrita_core import AmritaConfig, ModelPreset, PresetManager
from amrita_core.types import Message
```

#### 创建 Agent Session

有两种方式创建 `AgentSession`：

**方式一：使用依赖注入装饰器**

```python
from nonebot import on_command
from nonebot.params import Depends

matcher = on_command("chat")

@matcher.handle()
async def handle_chat(
    session: AgentSession = SessionDepends(
        train={"role": "system","content": "你是一个助手"},
        config=None,  # 使用默认配置或传入自定义 AmritaConfig
        preset=None,  # 使用默认预设或传入自定义 ModelPreset
    )
):
    async with session as agent:
        response = await agent.chat("你好")
        await matcher.send(response.content)
```

**方式二：手动加载**

```python
from nonebot.adapters import Event

@matcher.handle()
async def handle_chat(event: Event):
    async with await AgentSession.load_from(
        id_or_event=event,
        train={"role": "system","content": "你是一个助手"},
        config=None,
        preset=None,
    ) as agent:
        response = await agent.chat("你好")
        await matcher.send(response.content)
```

### 核心 API

#### AgentSession

`AgentSession` 继承自 `AmRuntime`，提供以下核心方法：

- **`load_from(id_or_event, train, config, preset, **kwargs)`**: 类方法，从事件或字符串 ID 加载会话
  - `id_or_event`: `Event` 对象或字符串 ID（推荐使用 `event.get_session_id()`）
  - `train`: 训练数据，可以是 `Message[str]` 或 `dict[str, str]`
  - `config`: AmritaCore 配置，为 `None` 时使用全局配置
  - `preset`: 模型预设，为 `None` 时使用默认预设

- **`chat(input, **kwargs)`**: 发送消息并获取响应
- **`save_context()`**: 手动保存上下文到数据库
- **`get_chatobject(input, **kwargs)`**: 获取 `ChatObject` 实例（内部使用）

#### SessionDepends

依赖注入辅助函数，用于在 NoneBot2 处理器中自动注入 `AgentSession` 实例。

参数与 `AgentSession.load_from` 相同。

### 数据持久化

插件自动管理以下数据的持久化：

1. **用户记忆 (Memory)**: 存储对话历史和上下文
2. **用户元数据 (Metadata)**: 记录 Token 使用量、调用次数等统计信息
3. **会话归档 (Sessions)**: 历史会话快照（保留最近 20 条）
4. **全局统计 (Insights)**: 每日全局使用情况

所有数据通过 `CachedUserDataRepository` 进行缓存，支持：

- LRU 缓存策略
- 线程安全的并发锁机制
- 脏标记追踪（仅保存变更数据）

### 并发控制

插件实现了多层锁机制确保数据一致性：

- **数据库锁**: 基于 `user_id` 的细粒度锁，防止并发写入冲突
- **Session 锁**: 基于 `session_id` 的操作锁，确保同一会话的串行化处理
- **动态锁池**: 使用 `WeakValueLRUCache` 实现可动态调整的锁池（默认容量 1024）

### 性能优化建议

1. **复用 Session**: 同一用户的多次请求应使用相同的 `session_id`，避免重复加载数据
2. **合理使用缓存**: 调整 `amrita_metadata_cache_size` 和 `amrita_memory_cache_size` 以平衡内存占用和性能
3. **批量操作**: `AgentSession` 的上下文管理器会在退出时批量保存使用量统计，建议使用 `async with` 语法
4. **限制工具调用**: 根据实际需求设置 `amrita_tool_call_limit`，避免过度消耗资源

### 监控与调试

#### 查看统计数据

```python
from nonebot_plugin_amrita.database import InsightsModel

# 获取今日统计
insights = await InsightsModel.get()
print(f"今日输入 Token: {insights.token_input}")
print(f"今日输出 Token: {insights.token_output}")
print(f"今日调用次数：{insights.usage_count}")

# 获取历史统计（最近 7 天）
all_insights = await InsightsModel.get_all(expire_days=7)
```

#### 查看用户使用排名

```python
from nonebot_plugin_amrita.database import UserDataExecutor

top_users = await UserDataExecutor.get_top_users(limit=10)
for user in top_users:
    print(f"用户：{user.user_id}, 调用次数：{user.called_count}")
```

### 常见问题

#### Q: 如何区分不同聊天场景？

A: 使用 `event.get_session_id()` 作为唯一标识。

#### Q: 如何清理用户数据？

A: 通过数据库操作清理（需自行引入 ORM）：

```python
from nonebot_plugin_orm import get_session
from nonebot_plugin_amrita.database import Memory, UserMetadata, MemorySessions

async with get_session() as session:
    # 删除特定用户的记忆
    await session.execute(delete(Memory).where(Memory.user_id == "user_id"))
    # 删除元数据
    await session.execute(delete(UserMetadata).where(UserMetadata.user_id == "user_id"))
    # 删除会话归档
    await session.execute(delete(MemorySessions).where(MemorySessions.user_id == "user_id"))
    await session.commit()
```

#### Q: 如何自定义模型预设？

A: 创建自定义 `ModelPreset` 并传入：

```python
from amrita_core import ModelPreset

custom_preset = ModelPreset(
    name="custom",
    model_name="gpt-4",
    # ... 其他参数
)

async with await AgentSession.load_from(
    event,
    train={"role": "system","content": "你是一个助手"},
    preset=custom_preset
) as agent:
    ...
```

---

## 特别说明（重要）

1. **AmritaCore 与 NoneBot2 DI 系统不兼容**
   两者为完全独立的依赖注入设计。
   AmritaCore 注入属于 **Agent 运行时内核层**，与 NoneBot2 无关。

2. **本插件数据库与 AmritaBot 同源**
   共享数据与表结构，不互相依赖，同源设计。

3. **本插件不依赖 AmritaBot**
   可独立安装、独立运行、独立部署。

### 开发者说明

请注意，在 NoneBot2 环境中使用本插件时，Session 应被当作用户唯一标识使用（即通过 `event.get_session_id()` 获取），而非某个 Session 归档的 ID，避免因标识混淆导致的用户数据错乱。
