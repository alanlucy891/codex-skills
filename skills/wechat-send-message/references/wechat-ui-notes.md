# WeChat UI Notes

Use these notes when the Windows WeChat/Weixin desktop UI behaves unexpectedly.

## Observed Workflow

- `Ctrl+F` may fail to target the WeChat search box if another window has focus.
- Clicking the left-panel search box directly is more reliable.
- Chinese text should be pasted through the clipboard. Simulated typing may turn it into `???`.
- Search results may be grouped as frequent use, contacts, group chats, chat records, and files.
- A person should normally appear under the contacts section before sending a one-to-one message.
- If the app opens a floating mini chat window or the wrong group, close it and restart from search.

## Verification

- Capture a screenshot after search and before sending.
- Capture another screenshot after sending.
- Report success only when the outgoing message bubble is visible in the intended chat.

## Known Coordinates From Prior Session

These are examples only; always prefer current screenshot coordinates.

- Search box in a 1320x980 WeChat window: about `left + 250`, `top + 85`.
- Message input area: about `left + 0.58 * width`, `top + 0.86 * height`.
- First single contact result under "Contacts" may appear near screen coordinates like `(1070, 372)` on a 2560x1600 display.
