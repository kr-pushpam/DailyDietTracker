# Requirements Specification: Personal Dietitian Bot (Version 2.0)

## 1. Project Overview
Version 2.0 transitions the Personal Dietitian Bot from a localized prototype into a cloud-native, serverless microservice. This version upgrades the analytical scope from basic calorie tracking to deep macronutrient estimation (carbohydrates, fats, proteins) and introduces multi-tier data pipelining for real-time tracking and long-term analytical warehouse archiving.

---

## 2. Functional Requirements (User Stories)

### 2.1 Core Nutrition Analytics (Advanced Ingestion)
* **FR-1.1: Macronutrient Extraction**
  * **As a** health-conscious user,
  * **I want** the bot to extract carbohydrates, fats, and proteins (measured in grams) alongside total calories from my food inputs,
  * **So that** I can monitor my exact daily macronutrient split to reach my specific fitness goals.

### 2.2 Reporting & Automation Engine
* **FR-2.1: On-Demand Progress Summaries**
  * **As a** user tracking my day,
  * **I want** to execute a `/summary` command at any point in time,
  * **So that** I can view a structured timeline card showing exactly when I ate, what I ate, the caloric value, and the macro breakdown for that specific day.

* **FR-2.2: Automated Midnight Reviews**
  * **As a** busy individual,
  * **I want** to automatically receive a complete dietary digest message at midnight,
  * **So that** I can review my daily compliance trends without needing to manually prompt the system.

### 2.3 Identity & System Auditing
* **FR-3.1: Telegram Profile Identity Mapping**
  * **As a** system operator,
  * **I want** the gateway to extract the user's Telegram first name, last name, or username from the webhook payload,
  * **So that** the database can maintain a clear identity record linking real names to platform activity log events over time.

* **FR-3.2: Token Optimization & Cost Auditing**
  * **As a** product owner,
  * **I want** to capture the exact prompt, completion, and total token count values returned by Gemini for every single request,
  * **So that** I can monitor LLM usage efficiency and predict API operational billing metrics.

### 2.4 Cloud Scaling & Storage Architecture
* **FR-4.1: Event-Driven 24/7 Scalability**
  * **As a** user logging meals late at night or early in the morning,
  * **I want** the bot to run on a serverless webhook architecture that wakes up instantly on request,
  * **So that** the bot is accessible 24/7 without long-polling delays or single-point-of-failure server crashes.

* **FR-4.2: Long-Term Analytics Warehousing**
  * **As an** analyst tracking my long-term health trends,
  * **I want** every single logged entry to be streamed into BigQuery immediately after it is processed,
  * **So that** I can safely retain years of historical metrics and connect them to BI tools like Looker Studio for dashboarding.

---

## 3. Non-Functional Requirements (NFR)

### 3.1 Availability & Performance
* **NFR-1.1 24/7 Availability:** The system webhooks MUST maintain 99.9% uptime by leveraging Google Cloud Run managed containers.
* **NFR-1.2 Latency Threshold:** The core webhook response must process, save data, and reply to the user interface within 3 seconds for standard text inputs.

### 3.2 Data Engineering & Storage Architecture
* **NFR-2.1 Dual-Tier Storage Pipeline:** The system MUST split data routing into an operational tier (Google Cloud Firestore for low-latency active session state lookup) and an analytical tier (Google BigQuery for cost-effective long-term data preservation).
* **NFR-2.2 Storage Partitioning:** The analytical BigQuery schema MUST be partitioned by date using the request timestamp to optimize historical query performance and reduce operational costs.
