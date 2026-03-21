# nonebot_plugin_amrita

Add AmritaCore support for NoneBot2

## 介绍

此插件为 NoneBot2 添加了 AmritaCore 支持， AmritaCore 是一个开源的轻量级高性能Agent框架，见 [文档](https://amrita-core.suggar.top/zh) 与 [Github](https://github.com/AmritaBot/AmritaCore) 了解详情。

## 快速开始

### 安装插件

```bash
nb plugin install nonebot_plugin_amrita
```

### 配置插件

在 NoneBot2 的配置文件中添加以下配置项：

#### Cookie 配置

| 配置项                 | 类型   | 默认值                 | 说明                            |
| ---------------------- | ------ | ---------------------- | ------------------------------- |
| `amrita_cookie_enable` | `bool` | `False`                | 是否启用 Cookie 功能            |
| `amrita_cookie`        | `str`  | 随机16位字母数字字符串 | Cookie 值，当启用 Cookie 时使用 |

#### 功能配置

| 配置项                   | 类型        | 默认值  | 说明                                             |
| ------------------------ | ----------- | ------- | ------------------------------------------------ |
| `amrita_mcp_enable`      | `bool`      | `False` | 是否启用 MCP (Model Context Protocol) 客户端功能 |
| `amrita_mcp_clients`     | `list[str]` | `[]`    | MCP 客户端脚本列表                               |
| `amrita_tool_call_limit` | `int`       | `15`    | 工具调用次数限制                                 |

#### LLM 配置

| 配置项                      | 类型  | 默认值 | 说明                   |
| --------------------------- | ----- | ------ | ---------------------- |
| `amrita_memory_token_limit` | `int` | `2048` | 记忆窗口的 token 限制  |
| `amrita_memory_length`      | `int` | `50`   | 记忆长度限制           |
| `amrita_prompt_token_limit` | `int` | `256`  | Prompt 的最大 token 数 |

#### 内置 Agent 配置

| 配置项                      | 类型                                                                       | 默认值        | 说明                                                                                                                                                      |
| --------------------------- | -------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `amrita_agent_mode`         | `Literal["agent", "rag", "none"]`                                          | `"agent"`     | Agent 模式，可选值：`agent`（智能Agent模式）、`rag`（检索增强生成模式）、`none`（无特殊模式）                                                             |
| `amrita_agent_thought_mode` | `Literal["reasoning", "chat", "reasoning-required", "reasoning-optional"]` | `"reasoning"` | Agent 思考模式，可选值：<br>- `reasoning`：推理模式<br>- `chat`：聊天模式<br>- `reasoning-required`：强制推理模式<br>- `reasoning-optional`：可选推理模式 |

#### 配置示例

在 `.env` 文件中配置：

```env
AMRITA_COOKIE_ENABLE=true
AMRITA_COOKIE=your-custom-cookie
AMRITA_MCP_ENABLE=true
AMRITA_MCP_CLIENTS=["client1","client2"]
AMRITA_TOOL_CALL_LIMIT=20
AMRITA_MEMORY_TOKEN_LIMIT=3072
AMRITA_MEMORY_LENGTH=100
AMRITA_PROMPT_TOKEN_LIMIT=512
AMRITA_AGENT_MODE=agent
AMRITA_AGENT_THOUGHT_MODE=reasoning
```

## 特别说明

AmritaCore的依赖注入系统与NoneBot2的依赖注入系统**并不兼容**，它们不是同一套系统。AmritaCore的依赖注入系统是**Agent运行时**的核心模块，与NoneBot2的依赖注入系统**无关**。
