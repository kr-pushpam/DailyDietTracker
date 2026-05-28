# Requirements Specification: Personal Dietitian Bot (Version 1.0)

## 1. Project Overview
The Personal Dietitian Bot is a localized, asynchronous Telegram application that acts as a real-time health companion. It enables users to log their daily food intake seamlessly through multiple modalities (text, photos, and voice notes) and automatically tracks their remaining daily calorie allowances using generative AI.

## 2. Functional Requirements (FR)

### 2.1 User Onboarding & Profiles
* **FR-1.1:** The system MUST initialize a user profile upon receiving the `/start` command.
* **FR-1.2:** The system MUST assign a default daily goal of 1500 calories to new users if no target exists.
* **FR-1.3:** The system MUST persist the user's unique Telegram ID to prevent duplicate entry generation.

### 2.2 Multimodal Intake Ingestion
* **FR-2.1 Text Logging:** Users MUST be able to log meals by typing natural language descriptions (e.g., "I had a bowl of oatmeal with bananas").
* **FR-2.2 Visual Logging:** Users MUST be able to upload images/photos of their plates.
* **FR-2.3 Voice Logging:** Users MUST be able to send voice messages describing what they ate.

### 2.3 Intelligent Calorie Analysis (The Calorie Engine)
* **FR-3.1 AI Processing:** The system MUST route all intake modalities to the Google GenAI `gemini-2.5-flash` model.
* **FR-3.2 Structured Extraction:** The AI model MUST analyze the input and return a strict JSON payload with exactly two keys: `food` (string description) and `calories` (integer evaluation).
* **FR-3.3 Fallback Graceful Failure:** If the system cannot parse the meal or if the model payload fails validation, it MUST catch the exception and return a user-friendly error message without crashing.

### 2.4 Data Aggregation & Progress Calculations
* **FR-4.1 Storage:** The system MUST log every parsed meal with the corresponding User ID, current timestamp (YYYY-MM-DD), food item description, and calculated calorie value.
* **FR-4.2 Progress Reporting:** Following every successful log, the system MUST compute:
  * Total calories consumed today.
  * Remaining calories left against the user's daily target (floored at 0).
* **FR-4.3 Output Generation:** The system MUST respond with a cleanly formatted Markdown status card displaying the logged item, individual item calories, and the updated daily balance.

---

## 3. Non-Functional Requirements (NFR)

### 3.1 Architecture & Performance
* **NFR-3.1 Asynchronous Execution:** The bot framework MUST execute fully asynchronously (`aiogram` + `asyncio`) to ensure the polling loop remains non-blocking during API wait states.
* **NFR-3.2 Local Dependencies:** Version 1.0 is engineered to run as a single-process application native to a local machine environment.

### 3.2 Data & Resource Management
* **NFR-4.1 Ephemeral File Lifecycle:** Any binary media asset downloaded to disk (e.g., `.jpg` or `.ogg` files) MUST be immediately deleted upon completing the GenAI API call execution pipeline to minimize local disk footprint.
* **NFR-4.2 Thread Isolation:** The database connection configuration MUST permit safe execution context handling across concurrent async event loops.
