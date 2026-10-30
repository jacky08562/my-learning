#!/usr/bin/env bash
# 最小可运行示例:用一条 curl 命令调用大模型
#
#   ./01-first-call.sh                  # 用默认问题
#   ./01-first-call.sh "什么是复利"      # 用你自己的问题
#
# 换成本地/其他厂商:改下面三个变量即可(接口格式是通用的 OpenAI 格式)
#   API_URL=https://api.deepseek.com/chat/completions MODEL=deepseek-chat LLM_API_KEY=sk-xxx ./01-first-call.sh

set -euo pipefail

API_URL="${API_URL:-https://text.pollinations.ai/openai}"
MODEL="${MODEL:-openai}"
KEY="${LLM_API_KEY:-}"
QUESTION="${1:-用一句话解释什么是 token}"

# ${KEY:+-H "..."} 的意思是:KEY 非空时才带上这个请求头
curl -sS --max-time 60 "$API_URL" \
  -H "Content-Type: application/json" \
  ${KEY:+-H "Authorization: Bearer $KEY"} \
  -d "{
    \"model\": \"$MODEL\",
    \"messages\": [
      {\"role\": \"system\", \"content\": \"你是一个用中文回答的助手,回答不超过 50 字。\"},
      {\"role\": \"user\",   \"content\": \"$QUESTION\"}
    ]
  }" \
| python3 -c '
import json, sys
d = json.load(sys.stdin)
print("回答:", d["choices"][0]["message"]["content"])
print("模型:", d.get("model"))
print("用量:", d.get("usage"))
'
