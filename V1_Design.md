# System Design Document: Personal Dietitian Bot (Version 1.0)

## 1. High-Level Architecture

Version 1.0 is an asynchronous, single-process monolithic application designed for local execution. It handles real-time polling updates from the Telegram Bot API, orchestrates media processing via local disk operations, and aggregates nutritional insights using the Google GenAI SDK and a embedded relational database.

```mermaid
graph TD
    A[Telegram Client App] <-->|Async Long Polling| B[aiogram Bot Engine]
    
    B -->|Text Event| C[Text Router]
    B -->|Photo Event| D[Photo Router]
    B -->|Voice Event| E[Voice Router]
    
    C -->|Raw String| F[Core Calorie Engine<br/>process_user_intake]
    D -->|Write temp.jpg| F
    E -->|Write temp.ogg| F
    
    F <-->|JSON Payload / Config| G[Google GenAI SDK<br/>gemini-2.5-flash]
    F <-->|SQL Queries| H[(SQLite Database<br/>diet_bot.db)]
    
    style B fill:#1f65ff,stroke:#fff,stroke-width:2px,color:#fff
    style F fill:#00b37e,stroke:#fff,stroke-width:2px,color:#fff
    style G fill:#f4b400,stroke:#fff,stroke-width:2px,color:#333
    style H fill:#e83e8c,stroke:#fff,stroke-width:2px,color:#fff
