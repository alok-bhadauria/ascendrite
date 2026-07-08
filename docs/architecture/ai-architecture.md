# AI Architecture: RAG Pipelines, Semantic Search, and Agent Workflows

## Document Metadata
*   **Purpose**: Details the RAG pipeline mechanics, vector embedding layouts, guardrails, agent lifecycles, and inference topologies.
*   **Scope**: Governs backend LLM connections, embedding generators, agent task queues, and guardrail middlewares.
*   **Intended Audience**: AI engineers, backend developers, and systems integrators.
*   **Related Documents**:
    *   [AI Philosophy](../governance/ai-philosophy.md)
    *   [System Design HLD](system-architecture-hld.md)
    *   [Prompt Library](../../editorial/prompt-library.md)
*   **Ownership**: AI Engineering Division Lead

---

## 1. Retrieval-Augmented Generation (RAG) Architecture
To ensure high factual precision, all natural language tutor queries shall run through a localized RAG ingestion pipeline.

```
[JSON Content Files] --> [Document Parser] --> [Chunking by Section/Callout]
                                                      |
                                                      v
[Prompt Synthesis] <-- [Similarity Search] <-- [Vector Repository]
```

### 1.1 Ingestion Specifications
*   **Parsing**: The system parser must read the raw curriculum files (notes, revisions, and interviews) stored in the Knowledge Base.
*   **Chunking**: Documents must be chunked based on logical markdown boundaries (e.g. content sections, headers, callouts). Chunks shall not cross different topic IDs to prevent context mixing.
*   **Vectorization**: Chunks shall be converted into vector embeddings using the configured embedding model. The embedding dimensions are defined by the model selection and abstracted at the interface layer.
*   **Vector Storage**: Vectors, along with their text content, topic IDs, and relative paths, shall be indexed in the database via the Vector Repository interface.

### 1.2 Retrieval & Generation Loop
When a learner requests clarification:
1.  The client sends the query via a REST call to the API.
2.  The server must generate a vector embedding of the query using the configured embedding model.
3.  The server shall execute a similarity search on the Vector Repository to extract the top matching document chunks.
4.  The server must inject the retrieved chunks and the user's query into the system prompt template.
5.  The prompt is sent to the LLM to generate the final response.


---

## 2. Multi-Agent System Scopes and Boundaries
Ascendrite utilizes a decoupled multi-agent architecture where agents own specific operational boundaries. The agents shall interact strictly via contract-first APIs and message queues.

### 2.1 Agent Definition
*   **Learning Assistant**: Resolves user queries regarding subject notes, derivations, and code exercises.
*   **Navigation Assistant**: Converts natural language queries into semantic searches and maps the optimal learning route through the concept graph.
*   **Knowledge Authoring Agent**: Scans and pre-validates new curriculum files submitted by contributors.
*   **Knowledge Review Agent**: Performs semantic checks across subject maps to find logical holes or missing links.
*   **Personalization Engine**: Analyzes learner progress logs and schedules dynamic review intervals.
*   **Admin Assistant**: Monitors server logs, flags security anomalies, and checks rate-limiting violations.

### 2.2 Agent Lifecycle Management
Agents must operate within a deterministic lifecycle state machine:
*   **Idle**: Agent sits in a queue waiting for event-driven triggers.
*   **Initializing**: Loads configuration schemas, parameters, and telemetry profiles.
*   **Executing**: Actively processes tasks (e.g., code analysis or semantic search verification).
*   **Evaluating**: Audits output accuracy against structural schemas and semantic rules.
*   **Terminal**: Cleans up run resources, releases connection handlers, and writes outcomes to log databases.

---

## 3. Online vs. Offline Inference Model

To optimize latency and control operating costs, AI tasks are split across two execution pipelines:
*   **Online Inference (Real-time)**: High-complexity tasks requiring immediate response loop completion.
    *   *Tutor Conversations*: Dynamic student Q&A interactions and system design feedback.
    *   *Code Evaluation*: Semantic testing and coding challenge syntax reviews.
    *   *Interactive Recommendations*: Real-time subject recommendations calculated during active user sessions.
*   **Offline Inference (Batch Processing)**: Low-urgency, high-throughput verification tasks running asynchronously.
    *   *Syllabus Validation*: Automated content review, link consistency checks, and graph validation pipelines.
    *   *Personalization Logs*: Batch processing user telemetry events to optimize spaced-repetition schedules.
    *   *Model Improvement*: Analytical evaluation of previous logs to refine retrieval priority matrices.

---

## 4. Input & Output Guardrails

AI services must implement strict guardrails to prevent hallucinations, formatting errors, or security leak vulnerabilities:
*   **Strict Context Grounding**: System prompts must explicitly limit models to answer *only* based on the retrieved text vectors, returning "I do not know" if context is missing.
*   **Structural Parsing Constraints**: Outputs must be requested in structured JSON format and programmatically validated against schemas. Non-compliant outputs must trigger retries.
*   **Input/Output Filtering Middleware**: Input filters must sanitize queries to block prompt injection attacks. Output filters must scan for sensitive leak keywords before response delivery.

---

## 5. Recommendation Engine

The platform utilizes a multi-tiered recommendation system to customize user paths, highlight community engagement, and adapt workspaces:

### 5.1 Learning Recommendations
*   **Next Topic**: Recommends the next optimal topic node in the curriculum graph using the student's current mastery metrics.
*   **Revision**: Schedules spaced-repetition flashcards based on concept difficulty logs and retention histories.
*   **Practice & Projects**: Suggests practice skeletons or system design challenges targeting diagnosed skill gaps.

### 5.2 Platform Recommendations
*   **Content Discovery**: Recommends new subjects or external references aligned with active academic tags.
*   **Connections**: Suggests peer connections, trending workspaces, and specialized learning communities based on common domain interests.

### 5.3 Personalization Recommendations
*   **Dashboard Components**: Reorders workspace cards based on active usage frequencies (e.g., placing the code editor upfront during active coding challenges).
*   **User Preferences**: Automates layout shifts and tool configurations by identifying student workspace interaction patterns.

