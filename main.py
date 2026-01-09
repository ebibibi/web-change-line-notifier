#!/usr/bin/env python3
"""
Web Change LINE Notifier
Webサイトの変更を検知してLINEに通知するスクリプト
"""

import hashlib
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# 環境変数
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")
TARGET_URL = os.getenv("TARGET_URL")
STATE_FILE = os.getenv("STATE_FILE", "state.json")


def send_line_message(message: str) -> bool:
    """LINEにメッセージを送信する"""
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message}],
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"LINE通知送信成功")
        return True
    else:
        print(f"LINE通知送信失敗: {response.status_code} {response.text}")
        return False


def get_page_content(url: str) -> str | None:
    """Webページの内容を取得する"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"ページ取得エラー: {e}")
        return None


def get_content_hash(content: str) -> str:
    """コンテンツのハッシュを計算する"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def load_state() -> dict:
    """前回の状態を読み込む"""
    state_path = Path(STATE_FILE)
    if state_path.exists():
        with open(state_path, "r") as f:
            return json.load(f)
    return {}


def save_state(state: dict) -> None:
    """状態を保存する"""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def main():
    # 環境変数チェック
    if not all([LINE_CHANNEL_ACCESS_TOKEN, LINE_USER_ID, TARGET_URL]):
        print("エラー: 必要な環境変数が設定されていません")
        print("LINE_CHANNEL_ACCESS_TOKEN, LINE_USER_ID, TARGET_URL を確認してください")
        sys.exit(1)

    print(f"監視対象: {TARGET_URL}")

    # ページ内容を取得
    content = get_page_content(TARGET_URL)
    if content is None:
        print("ページの取得に失敗しました")
        sys.exit(1)

    # ハッシュを計算
    current_hash = get_content_hash(content)
    print(f"現在のハッシュ: {current_hash[:16]}...")

    # 前回の状態と比較
    state = load_state()
    previous_hash = state.get(TARGET_URL)

    if previous_hash is None:
        # 初回実行
        print("初回実行: 状態を保存します")
        state[TARGET_URL] = current_hash
        save_state(state)
        print("初回実行のため通知はスキップします")
    elif previous_hash != current_hash:
        # 変更検知
        print("変更を検知しました！")
        message = f"練馬Jazz祭りのサイトに変更がありました！\n\n{TARGET_URL}"
        send_line_message(message)
        state[TARGET_URL] = current_hash
        save_state(state)
    else:
        # 変更なし
        print("変更はありません")


if __name__ == "__main__":
    main()
