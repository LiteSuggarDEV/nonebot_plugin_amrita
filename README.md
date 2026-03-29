# LibAmritaCore

**LibAmritaCore：把下一代高性能 Agent 内核，带入 NoneBot2 生态。**

## 介绍

此插件为 NoneBot2 生态提供 **AmritaCore** 原生支持。
AmritaCore 是一套开源、轻量、高性能的下一代 Agent 运行时内核，提供可中断、可自省、可恢复的现代化 AI 执行环境。

了解更多：

- 📖 [官方文档](https://amrita-core.suggar.top/zh)
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

## 特别说明（重要）

1. **AmritaCore 与 NoneBot2 DI 系统不兼容**
   两者为完全独立的依赖注入设计。
   AmritaCore 注入属于 **Agent 运行时内核层**，与 NoneBot2 无关。

2. **本插件数据库与 AmritaBot 完全隔离**
   不共享表名、不共享数据、不互相依赖，仅同源设计，迁移成本极低。

3. **本插件不依赖 AmritaBot**
   可独立安装、独立运行、独立部署。

### 开发者说明

请注意，在 NoneBot2 环境中使用本插件时，Session 应被当作用户唯一标识使用（即通过 `event.get_session_id()` 获取），而非某个 Session 归档的 ID，避免因标识混淆导致的用户数据错乱。
