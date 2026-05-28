Markdown
# System Design Document: Personal Dietitian Bot (Version 1.0)

## 1. System Architecture Overview
Version 1.0 of the application is a lightweight, asynchronous monolithic application designed to run locally. It links the Telegram Bot API to Google Cloud’s Gemini vision-and-voice LLM models, relying on a localized transactional data layer.

              +-----------------------+
              |  Telegram Client App  |
              +-----------+-----------+
                          | (Polling)
                          v
              +-----------------------+
              |  aiogram Bot Engine   |
              +-----------+-----------+
                          |
     +--------------------+--------------------+
     | Text Intercept     | Photo Intercept    | Voice Intercept
     v                    v                    v
+----------------+   +----------------+   +----------------+
| Direct String  |   | Save temp.jpg  |   | Save temp.ogg  |
+--------+-------+   +--------+-------+   +--------+-------+
|                    |                    |
+--------------------+--------------------+
|
v
+-----------------------------+
| process_user_intake()       |
| (Core Engine Execution)     |
+--------------+--------------+
|
+---------------+---------------+
|                               |
v                               v
+---------------------+        +-----------------------+
| google-genai SDK    |        | SQLite 3 DB           |
| (gemini-2.5-flash)  |        | (diet_bot.db)         |
+---------------------+        +-----------------------+


---

## 2. Component Breakdown

### 2.1 Interface Layer (`aiogram` Router)
Manages the long-polling connection loop directly with Telegram servers. Handles incoming interaction packets, identifies data types, and orchestrates asynchronous background tasks:
* **Command Handler (`/start`):** Sets up user tracking baselines.
* **Text Message Handler (`F.text`):** Intercepts raw string descriptors.
* **Photo Message Handler (`F.photo`):** Isolation download mechanic that extracts the highest-resolution photo thumbnail into a local `temp.jpg` binary file.
* **Voice Message Handler (`F.voice`):** Intercepts audio notes and downloads them locally as a native `temp.ogg` file.

### 2.2 Core Logic Layer (Calorie Engine)
The centralized core runtime orchestrator (`process_user_intake`). It acts as the middleware controller which:
1. Fetches baseline targets from the database layer.
2. Formulates the multimodal content payload (`types.Part.from_bytes`) for binary streams.
3. Implements strict zero-shot system instructions to prevent LLM hallucinations outside of standard JSON envelopes.
4. Cleanses and transforms string returns back to internal system primitives.

### 2.3 Storage Layer (SQLite3 Engine)
A localized embedded file database (`diet_bot.db`). It operates under standard multi-thread permission overrides (`check_same_thread=False`).

#### Relational Data Schema:
