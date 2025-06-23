# MCP‑Powered Insurance Voice Agent 🎙️🤖

An end-to-end modular voice agent built using the OpenAI Agents SDK and the Model Context Protocol (MCP). This framework demonstrates how to construct robust, voice-enabled conversational agents that orchestrate tools like RAG, web search, and SQLite via MCP.

---

## 🌐 Overview

This project showcases how to leverage the open-source **Model Context Protocol (MCP)**—a standardized middleware for LLM-tool interoperability—to build a voice assistant capable of:

- Decoupling agent logic from tool backends
- Managing context securely and dynamically
- Orchestrating tool usage via a planner agent
- Scaling with plug‑and‑play tool services
- Operating with voice input/output using STT and TTS models

You’ll learn how to:

1. Capture and transcribe voice input
2. Use a Planner agent to determine tool calls
3. Invoke MCP-managed services (RAG, web search, SQLite)
4. Synthesize the agent’s response and convert it to audio
5. Stream voice responses back to the user

---

## 🔧 Features

- **MCP Tool Framework**: Standardized communication between agents and microservices
- **Voice Flow**: Chained STT → Planner → MCP tool-calling → Response synthesis → TTS
- **Tools Included**:
  - Custom RAG (Retrieval-Augmented Generation)
  - Web search agent powered by OpenAI
  - Built-in SQLite database agent
- **Insurance Demo**: Insurance-advisory agent showcases real-world context
- **Low Latency Voice Models**: Uses `gpt-4o-transcribe` (STT) and `gpt-4o-mini-tts` (TTS) by default

---

## 📦 Installation

```bash
# Python dependencies
pip install asyncio ffmpeg ffprobe mcp openai openai-agents pydub scipy sounddevice uv nest_asyncio python-dotenv --quiet
pip install "openai-agents[voice]" --quiet
````

---

## ⚙️ Setup

1. Set your OpenAI API key in env file:

   ```
   OPENAI_API_KEY=**your opeanai api key**
   ```

2. Ensure `ffmpeg` is available on your system PATH.

---

## 🚀 Running the Voice Agent

Run the `main()` voice pipeline:

```bash
python main.py
```

It will:

1. Launch both MCP tool servers (RAG + web search, SQLite)
2. Capture streaming microphone input
3. Transcribe via STT
4. Plan tool calls and gather information
5. Synthesize a voice response via TTS
6. Stream audio back to the user

Interrupt with `Ctrl+C` to exit gracefully.

---

## 🧭 Architecture

```
[Microphone] → STT (gpt‑4o‑transcribe)
        ↓
    [Planner Agent]
        ↓ invokes MCP tools → [RAG / WebSearch / SQLite]
        ↓
    Synthesizes response → TTS (gpt‑4o‑mini‑tts)
        ↓
     [Speakers]
```

---

## 🧪 Example

> **User (voice):** “Can you tell me what’s covered under my home insurance policy?”
> **Agent (voice):** “Sure. Your policy covers fire damage, theft, and water damage up to \$150,000… \[continues]”

---

## 📄 License

MIT License — see the [LICENSE](LICENSE) file.

---

## 📚 References

* MCP-powered voice agent tutorial from OpenAI Cookbook ([cookbook.openai.com][3])
* Model Context Protocol details&#x20;
* Related tutorial: “Building a Voice Assistant with the Agents SDK” ([cookbook.openai.com][4])

---

## 🚩 Getting Help

Got questions or feedback? Open an issue or pull request—we’d love your input!
