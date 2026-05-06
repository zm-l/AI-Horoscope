# 🔮 Star Whisper: AI Horoscope Content Engine

> An interactive, stateful AI livestream simulator powered by Anthropic's Claude 4-5 model.

"Star Whisper" is a Python-based engine that acts as an AI astrologer in a simulated livestream room. It tackles the classic "LLM repetition" problem by using a local JSON database to track user history, structurally preventing the AI from reusing past themes, styles, and follow-up questions. 

By utilizing **Stateful RAG (Retrieval-Augmented Generation)**, the engine ensures that Day-5 veterans get deep, continuing narratives, while Day-1 newcomers receive welcoming, mysterious introductions.

## ✨ Features

- **Stateful RAG Architecture:** Tracks the last 3 days of user interactions (themes, styles, questions) to guarantee fresh content.
- **Dynamic Persona Branching:** Adapts the prompt context seamlessly based on the user's visit count and past interactions.
- **Provocative Hook Engine:** Forces the LLM to generate choice-based (A/B) or ego-bait follow-up questions designed to maximize chat engagement.
- **Robust JSON Parsing:** Custom extraction logic cleanly handles LLM markdown artifacts (like ````json) and safely parses the output.
- **Auto-Provisioning:** Automatically creates and saves new profiles (including Zodiac signs) for unrecognized usernames.
- **UTF-8 Safe:** Built to handle special characters, emojis, and Windows BOM formatting without crashing.

## 📂 Project Structure
```text
/star-whisper-engine
│
├── main.py              # Execution script, terminal UI, and state management
├── agent.py             # Claude 3 API logic, Prompt Engineering, and JSON parsing
├── user_db.json         # Local database for user profiles and history tracking
└── requirements.txt     # Python dependencies