#!/usr/bin/env python3
"""用 Python 调一次大模型 —— 只用标准库,不装任何第三方包。

    python3 02_chat.py "什么是复利"

和 01-first-call.sh 干的是同一件事。区别在于:shell 适合快速试,
Python 适合把调用逻辑放进程序里(比如批量提问、接到网页上、存进数据库)。
"""

import json
import os
import sys
import urllib.error
import urllib.request

API_URL = os.environ.get("API_URL", "https://text.pollinations.ai/openai")
MODEL = os.environ.get("MODEL", "openai")
KEY = os.environ.get("LLM_API_KEY", "")


def ask(question: str) -> dict:
    """发一次请求,返回解析后的 JSON 字典。"""
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "你是一个用中文回答的助手,回答不超过 50 字。"},
            {"role": "user", "content": question},
        ],
    }

    headers = {"Content-Type": "application/json"}
    if KEY:
        headers["Authorization"] = f"Bearer {KEY}"

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # 401 = 钥匙不对;402/429 = 额度用完或被限流;500 = 服务端问题
        body = e.read().decode("utf-8", "replace")
        print(f"[HTTP {e.code}] {body[:300]}", file=sys.stderr)
        raise SystemExit(1)


def main() -> None:
    question = " ".join(sys.argv[1:]) or "用一句话解释什么是 token"
    data = ask(question)

    print("问:", question)
    print("答:", data["choices"][0]["message"]["content"])

    usage = data.get("usage") or {}
    print(f"用量: 输入 {usage.get('prompt_tokens')} + 输出 {usage.get('completion_tokens')}"
          f" = {usage.get('total_tokens')} tokens")


if __name__ == "__main__":
    main()
