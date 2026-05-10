# Codex Skills / Codex 技能库

This repository stores reusable Codex skills. Each skill is a self-contained folder with a `SKILL.md` file and optional scripts, references, or assets.

本仓库用于存放可复用的 Codex 技能。每个技能都是一个独立文件夹，包含 `SKILL.md`，并可附带脚本、参考资料或资源文件。

## Repository Purpose / 仓库用途

- Keep personal or project-specific Codex skills in one place.
- Version skill changes with Git and GitHub.
- Reuse stable workflows across future Codex sessions.

- 集中保存个人或项目专用的 Codex 技能。
- 使用 Git 和 GitHub 管理技能版本。
- 在之后的 Codex 会话中复用稳定的工作流。

## Structure / 目录结构

```text
codex-skills/
  skills/
    wechat-send-message/
      SKILL.md
      agents/openai.yaml
      scripts/send_wechat_message.py
      references/wechat-ui-notes.md
```

## Included Skills / 已包含技能

### wechat-send-message / 微信发送消息

Safely operate the Windows WeChat/Weixin desktop client to search for a recipient, confirm the target with screenshots, and send a short text message.

安全操作 Windows 微信桌面客户端：搜索收件人、通过截图确认目标，并发送短文本消息。

Key safeguards:

关键保护机制：

- Search first, send second.
- Confirm the recipient visually before sending.
- Stop if the result is a group, official account, file, or ambiguous chat record.
- Use clipboard paste for Chinese text to avoid input encoding issues.

- 先搜索，再发送。
- 发送前必须通过截图确认收件人。
- 如果结果是群聊、公众号、文件或不明确的聊天记录，则停止发送。
- 中文文本通过剪贴板粘贴，避免输入编码问题。

## Install Locally / 本地安装

Copy a skill folder into your Codex skills directory:

将技能文件夹复制到 Codex 技能目录：

```powershell
Copy-Item -Recurse .\skills\wechat-send-message "$env:USERPROFILE\.codex\skills\wechat-send-message"
```

## Validate / 校验

Run the Codex skill validator:

运行 Codex 技能校验工具：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\skills\wechat-send-message
```

## Notes / 备注

This repository is intended for skill source files only. Runtime screenshots, temporary logs, and generated archives should not be committed.

本仓库仅用于保存技能源文件。运行时截图、临时日志和生成的压缩包不应提交。
