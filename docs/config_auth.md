## 配置

Codex 配置给予你对模型、执行环境和 CLI 可用集成的细粒度控制。在学习本指南时，请同时参考 `codex exec` 中的工作流程、沙箱和批准中的防护栏，以及 AGENTS.md 发现中的项目指导。

### 快速导航
- 模型选择
- 执行环境
- MCP 集成
- 可观测性和遥测
- 配置文件和覆盖
- 参考表

Codex 支持多种设置配置值的机制：

1. **配置特定的命令行标志**（优先级最高），例如 `--model o3`

2. **通用 `-c` / `--config` 标志**，接受键值对，例如 `--config model="o3"`
   - 键可以包含点号以设置更深层的值，例如 `--config model_providers.openai.wire_api="chat"`
   - 为了与 `config.toml` 保持一致，值是 TOML 格式的字符串而不是 JSON 格式，所以使用 `key='{a = 1, b = 2}'` 而不是 `key='{"a": 1, "b": 2}'`
   - 值周围的引号是必要的，没有它们你的 shell 会在空格处分割配置参数，导致 `codex` 接收到额外的（无效的）参数
   - 值可以包含任何 TOML 对象，例如 `--config shell_environment_policy.include_only='["PATH", "HOME", "USER"]'`
   - 如果 `value` 不能被解析为有效的 TOML 值，它会被当作字符串值处理。这意味着 `-c model='"o3"'` 和 `-c model=o3` 是等价的
   - 在第一种情况中，值是 TOML 字符串 `"o3"`，在第二种情况中，值是 `o3`，这不是有效的 TOML，因此被当作 TOML 字符串 `"o3"` 处理
   - 因为引号由你的 shell 解释，`-c key="true"` 将被正确地解释为 TOML 中的 `key = true`（布尔值）而不是 `key = "true"`（字符串）。如果你由于某些原因需要字符串 `"true"`，你需要使用 `-c key='"true"'`（注意两组引号）

3. **配置文件** 
   - 其中环境值默认为 `$CODEX_HOME/config.toml`
   - 注意 `$CODEX_HOME` 也是存储日志和其他 Codex 相关信息的位置
   - `--config` 标志和文件都支持以下选项

---

## 模型选择

### `model`
Codex 应该使用的模型。

```toml
model = "gpt-5"  # 覆盖默认值（macOS/Linux 上为 "gpt-5-codex"，Windows 上为 "gpt-5"）
```

### `model_providers`
此选项允许你添加到 Codex 附带的默认模型提供商集合中。地图键变成你用 `model_provider` 选择提供商时使用的值。

**注意**：当你重复使用内置提供商的键时，不会覆盖内置提供商。你添加的条目仅在键是新的时才生效；例如，`[model_providers.openai]` 会保持原始的 OpenAI 定义不变。要自定义捆绑的 OpenAI 提供商，请优先使用专用的调整旋钮（例如 `OPENAI_BASE_URL` 环境变量）或注册新的提供商键并指向它。

**示例**：如果你想添加一个通过聊天完成 API 使用 OpenAI 4o 模型的提供商，你可以添加以下配置：

```toml
# 回忆在 TOML 中，根键必须在表之前列出
model = "gpt-4o"
model_provider = "openai-chat-completions"

[model_providers.openai-chat-completions]
# 在 Codex UI 中显示的提供商名称
name = "OpenAI using Chat Completions"
# 路径 `/chat/completions` 将被追加到此 URL 以发起聊天完成的 POST 请求
base_url = "https://api.openai.com/v1"
# 如果设置了 `env_key`，标识一个在使用此提供商的 Codex 时必须设置的环境变量
# 环境变量的值必须非空，并将用于 POST 请求的 `Bearer TOKEN` HTTP 头中
env_key = "OPENAI_API_KEY"
# wire_api 的有效值是 "chat" 和 "responses"。如果省略，默认为 "chat"
wire_api = "chat"
# 如果必要，需要添加到 URL 的额外查询参数
query_params = {}
```

**注意**：这使得可以使用 Codex CLI 与非 OpenAI 模型，只要它们使用与 OpenAI 聊天完成 API 兼容的 wire API。例如，你可以定义以下提供商来使用 Codex CLI 与本地运行的 Ollama：

```toml
[model_providers.ollama]
name = "Ollama"
base_url = "http://localhost:11434/v1"
```

或第三方提供商（使用 API 密钥的不同环境变量）：

```toml
[model_providers.mistral]
name = "Mistral"
base_url = "https://api.mistral.ai/v1"
env_key = "MISTRAL_API_KEY"
```

还可以配置提供商以包含带请求的额外 HTTP 头。这些可以是硬编码值（`http_headers`）或从环境变量读取的值（`env_http_headers`）：

```toml
[model_providers.example]
# name, base_url, ...

# 这将向模型提供商的每个请求添加值为 `example-value` 的 HTTP 头 `X-Example-Header`
http_headers = { "X-Example-Header" = "example-value" }

# 这将向模型提供商的每个请求添加值为 `EXAMPLE_FEATURES` 环境变量值的 HTTP 头 `X-Example-Features`
# （如果环境变量已设置且其值非空）
env_http_headers = { "X-Example-Features" = "EXAMPLE_FEATURES" }
```

### Azure 模型提供商示例

注意 Azure 要求 `api-version` 作为查询参数传递，所以在定义 Azure 提供商时确保将其指定为 `query_params` 的一部分：

```toml
[model_providers.azure]
name = "Azure"
# 确保为此 URL 设置适当的子域
base_url = "https://YOUR_PROJECT_NAME.openai.azure.com/openai"
env_key = "AZURE_OPENAI_API_KEY"  # 或 "OPENAI_API_KEY"，使用你的为准
query_params = { api-version = "2025-04-01-preview" }
wire_api = "responses"
```

在启动 Codex 前导出你的密钥：`export AZURE_OPENAI_API_KEY=…`

### 每个提供商的网络调优

以下可选设置控制每个模型提供商的重试行为和流式空闲超时。它们必须在 `config.toml` 中对应的 `[model_providers.<id>]` 块内指定。（较早的版本接受顶级键；这些现在被忽略。）

**示例**：

```toml
[model_providers.openai]
name = "OpenAI"
base_url = "https://api.openai.com/v1"
env_key = "OPENAI_API_KEY"
# 网络调优覆盖（全部可选；使用内置默认值）
request_max_retries = 4            # 重试失败的 HTTP 请求
stream_max_retries = 10            # 重试断开的 SSE 流
stream_idle_timeout_ms = 300000    # 5m 空闲超时
```

#### `request_max_retries`
Codex 将重试对模型提供商的失败 HTTP 请求的次数。默认为 `4`。

#### `stream_max_retries`
当流式响应中断时，Codex 尝试重新连接的次数。默认为 `5`。

#### `stream_idle_timeout_ms`
Codex 在将流式响应上的连接视为丢失前等待活动的时间。默认为 `300_000`（5 分钟）。

### `model_provider`
从 `model_providers` 地图中标识要使用的提供商。默认为 `"openai"`。你可以通过 `OPENAI_BASE_URL` 环境变量覆盖内置提供商的 `base_url`。

**注意**：如果你覆盖 `model_provider`，那么你可能也想覆盖 `model`。例如，如果你在本地运行带有 Mistral 的 ollama，那么你需要在配置中添加以下内容，以及在地图中添加新的条目：

```toml
model_provider = "ollama"
model = "mistral"
```

### `model_reasoning_effort`
如果选定的模型已知支持推理（例如：`o3`、`o4-mini`、`codex-*`、`gpt-5`、`gpt-5-codex`），在使用 Responses API 时推理默认启用。如 OpenAI 平台文档所述，这可以设置为：

- `"minimal"`
- `"low"`
- `"medium"`（默认）
- `"high"`

**注意**：要最小化推理，选择 `"minimal"`。

### `model_reasoning_summary`
如果模型名称以 `"o"` 开头（如 `"o3"` 或 `"o4-mini"`）或 `"codex"`，在使用 Responses API 时推理默认启用。如 OpenAI 平台文档所述，这可以设置为：

- `"auto"`（默认）
- `"concise"`
- `"detailed"`

要禁用推理总结，在配置中将 `model_reasoning_summary` 设置为 `"none"`：

```toml
model_reasoning_summary = "none"  # 禁用推理总结
```

### `model_verbosity`
在使用 Responses API 时控制 GPT-5 系列模型上的输出长度/详细程度。支持的值：

- `"low"`
- `"medium"`（省略时的默认值）
- `"high"`

设置时，Codex 在请求负载中包含 `text` 对象，配置有详细程度，例如：`"text": { "verbosity": "low" }`

**示例**：

```toml
model = "gpt-5"
model_verbosity = "low"
```

**注意**：这仅适用于使用 Responses API 的提供商。聊天完成提供商不受影响。

### `model_supports_reasoning_summaries`
默认情况下，`reasoning` 仅在已知支持它们的 OpenAI 模型的请求上设置。要强制在当前模型的请求上设置 `reasoning`，你可以通过在 `config.toml` 中设置以下内容来强制此行为：

```toml
model_supports_reasoning_summaries = true
```

### `model_context_window`
模型的上下文窗口大小，单位为令牌。

通常，Codex 知道最常见的 OpenAI 模型的上下文窗口，但如果你使用的是新模型而 Codex CLI 是旧版本，那么你可以使用 `model_context_window` 来告诉 Codex 在对话期间确定剩余上下文时使用什么值。

### `model_max_output_tokens`
这类似于 `model_context_window`，但是用于模型的最大输出令牌数。

---

## 执行环境

### `approval_policy`
确定用户何时应被提示批准 Codex 是否可以执行命令：

```toml
# Codex 有硬编码逻辑定义了一组"受信任"的命令。
# 将 approval_policy 设置为 `untrusted` 意味着 Codex 将在运行不在"受信任"集合中的命令前提示用户。
#
# 参见 https://github.com/openai/codex/issues/1260 了解计划以使最终用户能够定义自己的受信任命令。
approval_policy = "untrusted"
```

如果你想在命令失败时被通知，使用 `"on-failure"`：

```toml
# 如果命令在沙箱中运行失败，Codex 询问权限以在沙箱外重试该命令。
approval_policy = "on-failure"
```

如果你想让模型运行直到它决定需要请求提升的权限，使用 `"on-request"`：

```toml
# 模型决定何时升级
approval_policy = "on-request"
```

或者，你可以让模型运行直到它完成，永远不要求运行带提升权限的命令：

```toml
# 用户永远不会被提示：如果命令失败，Codex 将自动尝试其他方法。
# 注意 `exec` 子命令始终使用此模式。
approval_policy = "never"
```

### `sandbox_mode`
Codex 在 OS 级沙箱内执行模型生成的 shell 命令。

在大多数情况下，你可以使用单个选项选择所需的行为：

```toml
# 与 `--sandbox read-only` 相同
sandbox_mode = "read-only"
```

默认策略是 `read-only`，这意味着命令可以读取磁盘上的任何文件，但尝试写入文件或访问网络的行为会被阻止。

更宽松的策略是 `workspace-write`。指定时，Codex 任务的当前工作目录将可写（在 macOS 上也是如此 `$TMPDIR`）。注意 CLI 默认使用生成它的目录作为 `cwd`，尽管这可以使用 `--cwd/-C` 覆盖。

在 macOS（很快也是 Linux）上，所有包含作为直接子目录的可写根（包括 `cwd`）将配置文件夹为只读，而 Git 仓库的其余部分将可写。这意味着像 `git commit` 这样的命令默认会失败（因为它涉及写入 `.git/`），并且将需要 Codex 请求权限。

```toml
# 与 `--sandbox workspace-write` 相同
sandbox_mode = "workspace-write"

# 只在 `sandbox = "workspace-write"` 时适用的额外设置。
[sandbox_workspace_write]
# 默认情况下，Codex 会话的 cwd 将可写，以及 $TMPDIR（如果设置）和 /tmp（如果存在）。
# 将各自的选项设置为 `true` 将覆盖这些默认值。
exclude_tmpdir_env_var = false
exclude_slash_tmp = false

# 可选的 _额外_ 可写根的列表，超越 $TMPDIR 和 /tmp。
writable_roots = ["/Users/YOU/.pyenv/shims"]

# 允许在沙箱内运行的命令发起出站网络请求。默认禁用。
network_access = false
```

要完全禁用沙箱，指定如下：

```toml
# 与 `--sandbox danger-full-access` 相同
sandbox_mode = "danger-full-access"
```

如果 Codex 在提供其自身沙箱的环境中运行（例如 Docker 容器），这样做是合理的，使得进一步的沙箱是不必要的。

虽然如果你尝试在环境中使用 Codex，其中其本地沙箱机制不受支持（例如较旧的 Linux 内核或 Windows），也可能需要此选项。

### `tools.*`
使用可选的 `[tools]` 表来切换代理可能调用的内置工具。`web_search` 除非你主动选择，否则保持关闭，而 `view_image` 现在默认启用：

```toml
[tools]
web_search = true   # 允许 Codex 在不提示你的情况下发起第一方 web 搜索
view_image = false  # 禁用图像上传（默认启用）
```

`web_search` 也在遗留名称 `web_search_request` 下识别。切换很有用，当你想从你的仓库中包含屏幕截图或图表而无需手动粘贴它们。Codex 仍然尊重沙箱：它只能附加你允许的工作空间根内的文件。

### `approval_presets`
Codex 提供三个主要批准预设：

- **只读**：Codex 可以读取文件和回答问题；编辑、运行命令和网络访问需要批准。
- **自动**：Codex 可以在工作空间内读取文件、进行编辑和运行命令而无需批准；要求在工作空间外或网络访问批准。
- **完全访问**：完全磁盘和网络访问无提示；极度危险。

你可以使用 `--ask-for-approval` 和 `--sandbox` 选项在命令行进一步自定义 Codex 的运行方式。

参见沙箱和批准了解深入的示例和平台特定的行为。

### `shell_environment_policy`
Codex 生成子进程（例如当执行助手建议的工具调用时）。默认情况下，它现在将你的完整环境传递给这些子进程。你可以通过 `config.toml` 中的 `shell_environment_policy` 块调整这种行为：

```toml
[shell_environment_policy]
# inherit 可以是 "all"（默认）、"core" 或 "none"
inherit = "core"
# 设置为 true 以*跳过* `"*KEY*"` 和 `"*TOKEN*"` 的过滤
ignore_default_excludes = false
# 排除模式（不区分大小写的 glob）
exclude = ["AWS_*", "AZURE_*"]
# 力制设置/覆盖值
set = { CI = "1" }
# 如果提供，*仅* 与这些模式匹配的变量被保留
include_only = ["PATH", "HOME"]
```

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `inherit` | 字符串 | all | 环境的起始模板：`all`（克隆完整父环境）、`core`（`HOME`、`PATH`、`USER` 等）或 `none`（开始为空）。|
| `ignore_default_excludes` | 布尔值 | false | 当为 false 时，Codex 在其他规则运行前删除任何名称包含 `KEY`、`SECRET` 或 `TOKEN` 的变量（不区分大小写）。|
| `exclude` | 数组 | [] | 默认过滤后要删除的不区分大小写的 glob 模式。示例：`"AWS_*"`、`"AZURE_*"`。|
| `set` | 表<字符串,字符串> | {} | 显式键/值覆盖或添加——总是赢过继承的值。|
| `include_only` | 数组 | [] | 如果非空，一个模式白名单；仅匹配一个模式的变量存活最后一步。（通常与 `inherit = "all"` 一起使用。）|

模式是 glob 风格，不是完整的正则表达式：`*` 匹配任意数量的字符，`?` 匹配恰好一个，字符类如 `[A-Z]` 或 `[^0-9]` 被支持。匹配总是不区分大小写。此语法在代码中记录为 `EnvironmentVariablePattern`（参见 `core/src/config_types.rs`）。

如果你只需要一个干净的状态和一些自定义条目，你可以写：

```toml
[shell_environment_policy]
inherit = "none"
set = { PATH = "/usr/bin", MY_FLAG = "1" }
```

当前，`CODEX_SANDBOX_NETWORK_DISABLED=1` 也被添加到环境中，假设网络被禁用。这不可配置。

---

## MCP 集成

### `mcp_servers`
你可以配置 Codex 以使用 MCP 服务器为 Codex 提供对外部应用程序、资源或服务的访问。

#### 服务器配置

##### STDIO
STDIO 服务器是你可以通过计算机上的命令直接启动的 MCP 服务器。

```toml
# 顶级表名必须是 `mcp_servers`
# 子表名（本示例中的 `server-name`）可以是你喜欢的任何内容。
[mcp_servers.server_name]
command = "npx"
# 可选的
args = ["-y", "mcp-server"]
# 可选：向 MVP 服务器传播额外的环境变量。
# 环境变量的默认白名单将传播到 MCP 服务器。
# https://github.com/openai/codex/blob/main/codex-rs/rmcp-client/src/utils.rs#L82
env = { "API_KEY" = "value" }
# 或
[mcp_servers.server_name.env]
API_KEY = "value"
# 可选：将在 MCP 服务器环境中白名单的环境变量的附加列表。
env_vars = ["API_KEY2"]

# 可选：命令将从中运行的 cwd
cwd = "/Users/<user>/code/my-server"
```

##### 可流式 HTTP
可流式 HTTP 服务器使 Codex 能够与通过 HTTP URL（在 localhost 或另一个域上）访问的资源通信。

```toml
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
# 可选：包含用于身份验证的持有人令牌的环境变量
bearer_token_env_var = "ENV_VAR"
# 可选：具有硬编码值的头的映射。
http_headers = { "HEADER_NAME" = "HEADER_VALUE" }
# 可选：头的映射，其值将被环境变量替换。
env_http_headers = { "HEADER_NAME" = "ENV_VAR" }
```

可流式 HTTP 连接始终在底层使用实验性 Rust MCP 客户端，所以期望偶尔会出现粗糙的边缘。OAuth 登录流在标志后面：

```toml
experimental_use_rmcp_client = true
```

启用后，当服务器支持 OAuth 时运行 `codex mcp login <server-name>`。

#### 其他配置选项

```toml
# 可选：覆盖默认的 10s 启动超时
startup_timeout_sec = 20
# 可选：覆盖默认的 60s 每工具超时
tool_timeout_sec = 30
# 可选：禁用服务器而不移除它
enabled = false
# 可选：仅公开此服务器工具的子集
enabled_tools = ["search", "summarize"]
# 可选：隐藏特定工具（如果设置，在 `enabled_tools` 之后应用）
disabled_tools = ["search"]
```

当同时指定 `enabled_tools` 和 `disabled_tools` 时，Codex 首先限制服务器为允许列表，然后移除出现在拒绝列表中的任何工具。

#### 实验性 RMCP 客户端
此标志为可流式 HTTP 服务器启用 OAuth 支持。

```toml
experimental_use_rmcp_client = true

[mcp_servers.server_name]
…
```

#### MCP CLI 命令

```bash
# 列出所有可用命令
codex mcp --help

# 添加服务器（env 可以重复；`--` 分离启动程序命令）
codex mcp add docs -- docs-server --port 4000

# 列出配置的服务器（漂亮表格或 JSON）
codex mcp list
codex mcp list --json

# 显示一个服务器（表格或 JSON）
codex mcp get docs
codex mcp get docs --json

# 移除服务器
codex mcp remove docs

# 登录到支持 oauth 的可流式 HTTP 服务器
codex mcp login SERVER_NAME

# 从支持 oauth 的可流式 HTTP 服务器登出
codex mcp logout SERVER_NAME
```

#### 有用的 MCP 示例
有一个不断增长的有用 MCP 服务器列表，在使用 Codex 时可以帮助。

我们见过的一些最常见的 MCP 是：

- **Context7** —连接到广泛的最新开发者文档
- **Figma 本地和远程** - 访问你的 Figma 设计
- **Playwright** - 使用 Playwright 控制和检查浏览器
- **Chrome 开发者工具** — 控制和检查 Chrome 浏览器
- **Sentry** — 访问你的 Sentry 日志
- **GitHub** — 控制你的 GitHub 账户超越 git 允许的范围（如控制 PR、问题等）

---

## 可观测性和遥测

### `otel`
Codex 可以发出 OpenTelemetry 日志事件，描述每次运行：出站 API 请求、流式响应、用户输入、工具批准决定和每次工具调用的结果。导出默认禁用，所以本地运行保持自包含。通过添加 `[otel]` 表并选择导出器来选择加入。

```toml
[otel]
environment = "staging"   # 默认为 "dev"
exporter = "none"          # 默认为 "none"；设置为 otlp-http 或 otlp-grpc 以发送事件
log_user_prompt = false    # 默认为 false；除非明确启用，否则编辑提示文本
```

Codex 使用 `service.name = $ORIGINATOR`（发送在标头中的相同值，默认）、CLI 版本和一个属性来标记每个导出的事件，以便下游收集器可以区分 dev/staging/prod 流量。仅转发在 `codex_otel` crate 内生成的遥测——下面列出的事件——给导出器。

#### 事件目录
每个事件共享一组通用的元数据字段：`event.timestamp`、`conversation.id`、`app.version`、`auth_mode`、`user.account_id`（可用时）、`user.email`（可用时）、`terminal.type`（可用时）、`model`、`slug`。

启用 OTEL，Codex 发出以下事件类型（除了上面的元数据）：

##### `codex.conversation_starts`
- provider_name
- reasoning_effort（可选）
- reasoning_summary
- context_window（可选）
- max_output_tokens（可选）
- auto_compact_token_limit（可选）
- approval_policy
- sandbox_policy
- mcp_servers（逗号分隔列表）
- active_profile（可选）

##### `codex.api_request