# P3: AI / ML Basics Track

Full project spec: `references/projects.md` → "AI/ML Basics Project: agent.py"

## L1: OpenAI API Client

**Concept:** The OpenAI API takes a list of messages and returns a completion. `chat.completions.create()` is the main call. The `OPENAI_API_KEY` environment variable authenticates you — never hardcode keys in source files.

**Task:** Install the openai library. Write `chat.py` that sends a single user message and prints the assistant's reply.

```bash
pip install openai
export OPENAI_API_KEY=sk-...   # or set in .env
python chat.py
```

```python
# Minimal working example to build on:
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say hello in 5 words."}]
)
print(response.choices[0].message.content)
```

**Acceptance criteria:** Script runs and prints a response. `OPENAI_API_KEY` read from environment (not hardcoded). `openai.APIError` caught and printed cleanly.

**Common mistakes:** Hardcoding the API key in the file. Not checking `response.choices[0]` — empty choices list causes an IndexError. Using a deprecated `openai.ChatCompletion.create()` call (old SDK v0 style).

---

## L2: Prompt Engineering

**Concept:** The system prompt shapes the assistant's persona and constraints. Temperature controls randomness (0 = deterministic, 1 = creative). Max tokens limits response length. Keeping conversation history in a list enables multi-turn dialogue.

**Task:** Upgrade `chat.py` to a multi-turn Q&A assistant. Add a system prompt that defines a persona (e.g., "You are a Python tutor. Answer concisely."). Loop to collect user input, append to history, call the API, print response.

**Acceptance criteria:** Assistant maintains context across turns. System prompt visibly shapes behavior. `quit` or `exit` breaks the loop cleanly.

**Common mistakes:** Not appending the assistant's reply to history — next turn loses context. Setting temperature above 1.5 — causes API error. Printing `response` directly instead of `.choices[0].message.content`.

---

## L3: Tool Use / Function Calling

**Concept:** The model can call functions you define. You describe tools as JSON schemas; the model decides when to call them. Your code detects the tool call, runs the function, sends the result back. The model then incorporates it into its reply.

**Task:** Create `tools.py` with two functions:
- `read_file(path)` → returns file contents as a string
- `write_file(path, content)` → writes content, returns "written"

Define them as OpenAI tool schemas. Update `chat.py` to handle tool calls in the response loop.

**Acceptance criteria:** "Read the file students.csv" triggers `read_file`. "Write a note to notes.txt saying hello" triggers `write_file`. Both tool results are sent back to the model and incorporated into its reply.

**Common mistakes:** Not checking `response.choices[0].finish_reason == "tool_calls"` before trying to parse tool calls. Sending tool results without the `role: "tool"` message — API rejects it.

---

## L4: Simple Agent Loop

**Concept:** An agent loop repeatedly: takes user input → calls the model → checks if the model wants to use a tool → if yes, runs it and loops → if no, prints the reply. Add persistence to make it remember across sessions.

**Task:** Rename `chat.py` to `agent.py`. Add:
- `list_files(directory)` tool — returns list of files
- Loop that handles tool calls automatically until the model produces a final reply
- Save conversation history to `memory.json` on exit, reload on start

```bash
python agent.py
# You: summarize the file students.csv
# Agent: [calls read_file] Here are the students...
# You: quit
# Conversation saved.
```

**Acceptance criteria:** Agent handles multi-step tasks requiring multiple tool calls. History persists across sessions. `quit` saves and exits. All API errors handled gracefully.

**Common mistakes:** Infinite loop if model keeps calling tools — add a max-iterations guard (e.g., 10). Not serializing the full message list to JSON — datetime objects aren't JSON-serializable by default.
