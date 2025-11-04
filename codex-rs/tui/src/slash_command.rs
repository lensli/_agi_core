use strum::IntoEnumIterator;
use strum_macros::AsRefStr;
use strum_macros::EnumIter;
use strum_macros::EnumString;
use strum_macros::IntoStaticStr;

/// Commands that can be invoked by starting a message with a leading slash.
#[derive(
    Debug, Clone, Copy, PartialEq, Eq, Hash, EnumString, EnumIter, AsRefStr, IntoStaticStr,
)]
#[strum(serialize_all = "kebab-case")]
pub enum SlashCommand {
    // DO NOT ALPHA-SORT! Enum order is presentation order in the popup, so
    // more frequently used commands should be listed first.
    Model,
    Approvals,
    Review,
    New,
    Init,
    Compact,
    Undo,
    Diff,
    Mention,
    Status,
    Mcp,
    Logout,
    Quit,
    Exit,
    Feedback,
    Rollout,
    TestApproval,
}

impl SlashCommand {
    /// User-visible description shown in the popup.
    pub fn description(self) -> &'static str {
        match self {
            // SlashCommand::Feedback => "send logs to maintainers",
            // SlashCommand::New => "start a new chat during a conversation",
            // SlashCommand::Init => "create an AGENTS.md file with instructions for Codex",
            // SlashCommand::Compact => "summarize conversation to prevent hitting the context limit",
            // SlashCommand::Review => "review my current changes and find issues",
            // SlashCommand::Undo => "ask Codex to undo a turn",
            // SlashCommand::Quit | SlashCommand::Exit => "exit Codex",
            // SlashCommand::Diff => "show git diff (including untracked files)",
            // SlashCommand::Mention => "mention a file",
            // SlashCommand::Status => "show current session configuration and token usage",
            // SlashCommand::Model => "choose what model and reasoning effort to use",
            // SlashCommand::Approvals => "choose what Codex can do without approval",
            // SlashCommand::Mcp => "list configured MCP tools",
            // SlashCommand::Logout => "log out of Codex",
            // SlashCommand::Rollout => "print the rollout file path",
            // SlashCommand::TestApproval => "test approval request",
            SlashCommand::Feedback => "发送日志给维护者",
            SlashCommand::New => "在对话中开始新聊天",
            SlashCommand::Init => "创建包含 Codex 说明的 AGENTS.md 文件",
            SlashCommand::Compact => "总结对话以防止超过上下文限制",
            SlashCommand::Review => "查看当前更改并发现问题",
            SlashCommand::Undo => "要求 Codex 撤销一步操作",
            SlashCommand::Quit | SlashCommand::Exit => "退出 Codex",
            SlashCommand::Diff => "显示 git diff（包括未跟踪的文件）",
            SlashCommand::Mention => "提及一个文件",
            SlashCommand::Status => "显示当前会话配置和令牌使用情况",
            SlashCommand::Model => "选择要使用的模型和推理工作量级别",
            SlashCommand::Approvals => "选择 Codex 可以在无需批准的情况下执行的操作",
            SlashCommand::Mcp => "列出已配置的 MCP 工具",
            SlashCommand::Logout => "从 Codex 退出登录",
            SlashCommand::Rollout => "打印推出文件路径",
            SlashCommand::TestApproval => "测试批准请求",
        }
    }

    /// Command string without the leading '/'. Provided for compatibility with
    /// existing code that expects a method named `command()`.
    pub fn command(self) -> &'static str {
        self.into()
    }

    /// Whether this command can be run while a task is in progress.
    pub fn available_during_task(self) -> bool {
        match self {
            SlashCommand::New
            | SlashCommand::Init
            | SlashCommand::Compact
            | SlashCommand::Undo
            | SlashCommand::Model
            | SlashCommand::Approvals
            | SlashCommand::Review
            | SlashCommand::Logout => false,
            SlashCommand::Diff
            | SlashCommand::Mention
            | SlashCommand::Status
            | SlashCommand::Mcp
            | SlashCommand::Feedback
            | SlashCommand::Quit
            | SlashCommand::Exit => true,
            SlashCommand::Rollout => true,
            SlashCommand::TestApproval => true,
        }
    }

    fn is_visible(self) -> bool {
        match self {
            SlashCommand::Rollout | SlashCommand::TestApproval => cfg!(debug_assertions),
            _ => true,
        }
    }
}

/// Return all built-in commands in a Vec paired with their command string.
pub fn built_in_slash_commands() -> Vec<(&'static str, SlashCommand)> {
    SlashCommand::iter()
        .filter(|command| command.is_visible())
        .map(|c| (c.command(), c))
        .collect()
}
