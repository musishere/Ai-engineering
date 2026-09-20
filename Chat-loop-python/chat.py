"""Simple terminal chat loop against the Groq API. Stdlib only (urllib)."""
import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.groq.com/openai/v1/chat/completions"

# load KEY=value pairs from a .env file next to this script, if present
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b")
API_KEY = os.environ.get("GROQ_API_KEY")

if not API_KEY:
    sys.exit("Set GROQ_API_KEY in your environment.")

MAX_HISTORY_TOKENS = 500  # trim history once the estimate crosses this

# full conversation so far, sent in full on every turn (no server-side memory)
history = []


def estimate_tokens(messages):
    # no tokenizer lib available: ~4 chars/token is the standard rough estimate
    return sum(len(m["content"]) for m in messages) // 4


def trim_history():
    dropped = 0
    while len(history) > 1 and estimate_tokens(history) > MAX_HISTORY_TOKENS:
        history.pop(0)  # oldest first, keep the most recent messages
        dropped += 1
    if dropped:
        print(f"[history] dropped {dropped} oldest message(s) to stay under {MAX_HISTORY_TOKENS} tokens")


def ask(messages):
    body = json.dumps({"model": MODEL, "messages": messages}).encode()
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            # default urllib UA gets flagged as a bot by Groq's Cloudflare front door
            "User-Agent": "Mozilla/5.0",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()}")


print("Chat loop. Ctrl+C or 'exit' to quit.")
while True:
    try:
        user_input = input("you: ").strip()
    except (KeyboardInterrupt, EOFError):
        break
    if user_input.lower() in ("exit", "quit"):
        break
    if not user_input:
        continue

    history.append({"role": "user", "content": user_input})
    trim_history()
    reply = ask(history)

    answer = reply["choices"][0]["message"]["content"]
    usage = reply["usage"]  # prompt_tokens, completion_tokens, total_tokens
    history.append({"role": "assistant", "content": answer})

    print(f"bot: {answer}")
    print(
        f"[tokens] prompt={usage['prompt_tokens']} "
        f"completion={usage['completion_tokens']} total={usage['total_tokens']}"
    )
