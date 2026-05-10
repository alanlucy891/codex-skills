#!/usr/bin/env python
"""Safely search and send text in Windows WeChat/Weixin via UI automation.

The script intentionally separates search from send. Search first, inspect the
screenshot, then run send with the coordinates of the confirmed recipient row.
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import sys
import time


def require_modules():
    missing = []
    for module in ("pyautogui", "pyperclip", "pywinauto"):
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    if missing:
        names = " ".join(missing)
        raise SystemExit(
            f"Missing Python modules: {', '.join(missing)}\n"
            f"Install with: python -m pip install --user {names}"
        )


require_modules()

import pyautogui  # noqa: E402
import pyperclip  # noqa: E402
from pywinauto import Desktop  # noqa: E402


def find_wechat_window(title_pattern: str | None = None):
    desktop = Desktop(backend="uia")
    candidates = []
    for window in desktop.windows():
        try:
            title = window.window_text()
            rect = window.rectangle()
        except Exception:
            continue
        if not title:
            continue
        title_hit = ("微信" in title) or ("Weixin" in title) or ("WeChat" in title)
        if title_pattern:
            title_hit = title_pattern.lower() in title.lower()
        if title_hit and rect.width() > 600 and rect.height() > 400:
            candidates.append((window, rect.width() * rect.height()))
    if not candidates:
        raise SystemExit("Could not find a visible WeChat/Weixin window.")
    candidates.sort(key=lambda item: item[1], reverse=True)
    window = candidates[0][0]
    window.set_focus()
    time.sleep(0.4)
    return window


def shot(out_dir: Path, label: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = out_dir / f"wechat-{label}-{stamp}.png"
    pyautogui.screenshot().save(path)
    return path


def paste_text(text: str):
    pyperclip.copy(text)
    time.sleep(0.1)
    pyautogui.hotkey("ctrl", "v")


def click_search_box(rect):
    # Coordinates are relative to the main desktop WeChat layout observed on
    # Windows: search box in the left chat list, near the top.
    pyautogui.click(rect.left + 250, rect.top + 85)


def search_recipient(window, recipient: str):
    rect = window.rectangle()
    click_search_box(rect)
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "a")
    paste_text(recipient)
    time.sleep(1.1)


def open_confirmed_result(x: int, y: int):
    pyautogui.click(x, y)
    time.sleep(1.0)


def click_message_input(window):
    rect = window.rectangle()
    # Input box is the large lower-right text area in normal WeChat layout.
    pyautogui.click(rect.left + int(rect.width() * 0.58), rect.top + int(rect.height() * 0.86))
    time.sleep(0.2)


def send_message(window, message: str):
    click_message_input(window)
    paste_text(message)
    time.sleep(0.25)
    pyautogui.press("enter")
    time.sleep(1.0)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipient", required=True, help="WeChat contact/chat name to search.")
    parser.add_argument("--message", required=True, help="Text message to send.")
    parser.add_argument(
        "--action",
        choices=("search", "send"),
        default="search",
        help="Use search first; use send only after screenshot confirmation.",
    )
    parser.add_argument("--result-x", type=int, help="Screen x coordinate of confirmed search result row.")
    parser.add_argument("--result-y", type=int, help="Screen y coordinate of confirmed search result row.")
    parser.add_argument("--title-pattern", help="Optional visible window title substring.")
    parser.add_argument(
        "--screenshot-dir",
        default=".",
        help="Directory for confirmation screenshots.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = Path(args.screenshot_dir).resolve()
    window = find_wechat_window(args.title_pattern)

    if args.action == "search":
        search_recipient(window, args.recipient)
        path = shot(out_dir, "search")
        print(f"Search screenshot: {path}")
        print("Inspect the screenshot. If the target is correct, rerun with --action send and --result-x/--result-y.")
        return 0

    if args.result_x is None or args.result_y is None:
        raise SystemExit("--action send requires --result-x and --result-y from a confirmed screenshot.")

    search_recipient(window, args.recipient)
    before = shot(out_dir, "before-send")
    print(f"Before-send screenshot: {before}")
    open_confirmed_result(args.result_x, args.result_y)
    send_message(window, args.message)
    after = shot(out_dir, "after-send")
    print(f"After-send screenshot: {after}")
    print("Inspect the after-send screenshot and confirm the outgoing message bubble is visible.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
