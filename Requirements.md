# <span style="color:#1f65ff">Requirements Specification: Personal Dietitian Bot (Version 2.0)</span>

## <span style="color:#00b37e">1. Project Overview</span>
Version 2.0 transitions the Personal Dietitian Bot from a localized prototype into a production-ready, cloud-native serverless microservice. This iteration expands tracking capabilities from basic calories to full macronutrient profiling (carbohydrates, fats, proteins), integrates Telegram user profile resolution, implements a dual-tier storage ecosystem (Firestore + BigQuery), and introduces real-time transaction-level cost tracking with scale-to-zero infrastructure guardrails.

---

## <span style="color:#00b37e">2. Functional Requirements (User Stories)</span>

### <span style="color:#e83e8c">2.1 Advanced Nutrition Ingestion</span>
* **FR-1.1: Full Macronutrient Profiling**
  * **As a** health-conscious user,
  * **I want** the bot to extract carbohydrates, fats, and proteins (measured in grams) alongside total calories from my food descriptions,
  * **So that** I can track my exact macronutrient balance to reach my specific fitness goals.

### <span style="color:#e83e8c">2.2 Reporting & Automation Engine</span>
* **FR-2.1: On-Demand Progress Summaries**
  * **As a** user tracking my daily consumption,
  * **I want** to execute a `/summary` command at any point in time,
  * **So that** I can view a structured timeline showing exactly when I ate, what I ate, total calories, and the full macro breakdown for the current calendar day.

* **FR-2.2: Automated Midnight Reviews**
  * **As a** busy individual,
  * **I want** to automatically receive a complete dietary summary message at midnight,
  * **So that** I can review my daily metrics and compliance trends without needing to manually prompt the system.

### <span style="color:#e83e8c">2.3 Profile & Identity Mapping</span>
* **FR-3.1: Telegram Profile Resolution**
  * **As a** system operator,
  * **I want** the webhook gateway to automatically extract the user's Telegram first name, last name, and username from incoming message metadata,
  * **So that** application logs and data records clearly associate real user identities with platform activity logs over time.

### <span style="color:#e83e8c">2.4 Cloud Scaling & Storage Architecture</span>
* **FR-4.1: Event-Driven 24/7 Availability**
  * **As a** user logging meals at irregular hours,
  * **I want** the bot to operate on a serverless webhook architecture that wakes up instantly on request,
  * **So that** the system remains responsive 24/7 without long-polling latencies or downtime from server crashes.

* **FR-4.2: Long-Term Analytics Warehousing**
  * **As an** analyst tracking my health patterns over months or years,
  * **I want** every single logged entry to be streamed directly into an analytical data warehouse immediately after ingestion,
  * **So that** I can securely store long-term metrics and connect them to business intelligence tools like Looker Studio for historical dashboarding.

### <span style="color:#e83e8c">2.5 Consumption & Cost Management</span>
* **FR-5.1: Zero-Traffic Cost Elimination (Scale-to-Zero)**
  * **As a** project owner,
  * **I want** the underlying cloud infrastructure to scale completely down to zero compute power when no messages are being received,
  * **So that** the application incurs zero active runtime or hosting costs during idle periods.

* **FR-5.2: Per-Query Transaction Cost Auditing**
  * **As a** product owner,
  * **I want** the application to capture the precise prompt, completion, and total token count counts from the GenAI API response,
  * **So that** the system can instantly calculate the exact financial cost of each individual user query and log it into the data warehouse.

---

## <span style="color:#00b37e">3. Non-Functional Requirements (NFR)</span>

### <span style="color:#e83e8c">3.1 Availability, Scaling & Performance</span>
* **NFR-1.1 Infrastructure Uptime:** The webhook API engine MUST maintain a 99.9% uptime baseline by deploying as a stateless container within Google Cloud Run.
* **NFR-1.2 Scale-to-Zero Guardrail:** The compute tier MUST be configured with `min-instances = 0` to guarantee that no billing costs accumulate for CPU/RAM allocation while the bot is not actively processing a webhook request.
* **NFR-1.3 Response Latency:** The system MUST completely process an incoming text payload, commit records to both storage tiers, and generate a reply within a 3.0-second threshold.

### <span style="color:#e83e8c">3.2 Data Engineering & Storage Architecture</span>
* **NFR-2.1 Dual-Tier Storage Separation:** The system data pipeline MUST bifurcate data operations:
  * **Operational Tier:** Google Cloud Firestore handles low-latency, active daily session lookups and immediate `/summary` commands.
  * **Analytical Tier:** Google BigQuery receives real-time data streaming for permanent, historical record archiving.
* ***NFR-2.2 Optimization & Partitioning:** The destination BigQuery table MUST be partitioned by day using the incoming transaction timestamp to optimize query execution and minimize data scanning costs during historical reports.

### <span style="color:#e83e8c">3.3 Financial Governance & Auditing Precision</span>
* **NFR-3.1 API Token Capture:** The core runtime engine MUST extract the structured `usage_metadata` payload natively from the `google-genai` SDK response for every processing transaction.
* **NFR-3.2 Financial Line-Item Logging:** The analytics ingestion pipeline MUST calculate a precision floating-point value (`calculated_cost_usd`) derived from active model price sheets (Cost per 1M Input Tokens / Cost per 1M Output Tokens) and append it to the corresponding BigQuery log row.
