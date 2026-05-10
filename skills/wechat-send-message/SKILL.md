---
name: wechat-send-message
description: Safely operate the Windows WeChat/Weixin desktop client to search for a recipient and send a short text message through UI automation. Use when Codex is asked to send a WeChat message, search WeChat contacts, message File Transfer Assistant, or repeat a message to a named WeChat contact from the desktop app.
---

# WeChat Send Message

## Overview

Use this skill to send short text messages in the Windows WeChat/Weixin desktop client with screenshot confirmation. Treat live messaging as sensitive: confirm the target chat visually before sending, and stop if the search result is ambiguous.

## Workflow

1. Open or focus WeChat/Weixin.
2. Search the requested recipient with `scripts/send_wechat_message.py --action search`.
3. Inspect the screenshot. Confirm that the intended target is a single contact or the exact chat the user requested.
4. Run `scripts/send_wechat_message.py --action send` with the clicked result coordinates from the confirmed screenshot.
5. Inspect the after-send screenshot and report whether the outgoing message bubble is visible.

Never send to a group, official account, search-history result, or file result unless the user explicitly requested that exact target.

## Quick Commands

Install dependencies if Python cannot import them:

```powershell
python -m pip install --user pywinauto pyautogui pyperclip
```

Search and capture a confirmation screenshot:

```powershell
python .\scripts\send_wechat_message.py --recipient "RECIPIENT" --message "MESSAGE" --action search
```

Send after visually confirming the recipient row. Use the row coordinates from the screenshot:

```powershell
python .\scripts\send_wechat_message.py --recipient "RECIPIENT" --message "MESSAGE" --action send --result-x 1070 --result-y 372
```

## Target Confirmation Rules

- Prefer a result under a visible "Contacts" section for named people.
- For File Transfer Assistant, confirm the chat title or selected chat is the File Transfer Assistant conversation.
- If the search result only shows chat records, group chats, files, mini-programs, or official accounts, do not send.
- If multiple people have similar names, ask the user which one to use.
- Use clipboard paste for Chinese and other non-ASCII text; direct keystroke simulation may degrade non-ASCII input into question marks.

## Practical Notes

- The Windows app may appear as `Weixin.exe`, `WeChat.exe`, or with a Chinese WeChat window title.
- WeChat UI automation is coordinate-sensitive. Capture a screenshot before sending whenever the active window, scaling, or layout may have changed.
- If a floating chat window opens unexpectedly, close it and restart from search.
- If the message appears in the input box but does not send, click the text input area and press Enter again, then verify with a screenshot.

## Resources

- `scripts/send_wechat_message.py`: Focuses WeChat, searches a recipient, captures screenshots, and sends only after a confirmed result coordinate is supplied.
- `references/wechat-ui-notes.md`: Notes from the observed Windows WeChat layout and failure modes.
