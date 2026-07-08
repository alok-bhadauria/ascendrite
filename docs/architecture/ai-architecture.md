# AI Architecture: RAG Pipelines, Semantic Search, and Agent Workflows

## Document Metadata
*   **Purpose**: Details the RAG pipeline mechanics, vector embedding layouts, and the boundaries of the multi-agent AI framework.
*   **Scope**: Governs backend LLM connections, embedding generators, and agent task queues.
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
[Prompt Synthesis] <-- [Similarity Search] <-- [Vector Store (pgvector)]
```

### 1.1 Ingestion Specifications
*   **Parsing**: The system parser must read the raw curriculum files (notes, revisions, and interviews) stored in `knowledge-base/`.
*   **Chunking**: Documents must be chunked based on logical markdown boundaries (e.g. content sections, headers, callouts). Chunks shall not cross different topic IDs to prevent context mixing.
*   **Vectorization**: Chunks shall be converted into 1536-dimensional vectors using the specified embedding model.
*   **Vector Storage**: Vectors, along with their text content, topic IDs, and relative paths, shall be indexed in the vector store database.

### 1.2 Retrieval & Generation Loop
When a learner requests clarification:
1.  The client sends the query via a REST call to the API.
2.  The server must generate a vector embedding of the query using the same embedding model.
3.  The server shall execute a cosine similarity search on the vector store to extract the top 3 matching document chunks.
4.  The server must inject the retrieved chunks and the user's query into the system prompt template.
5.  The prompt is sent to the LLM to generate the final response.

---

## 2. Multi-Agent System Scopes and Boundaries
Ascendrite utilizes a decoupled multi-agent architecture where agents own specific operational boundaries. The agents shall interact strictly via contract-first APIs and message queues.

### 2.1 Learning Assistant
*   **Responsibility**: Resolves user queries regarding subject notes, derivations, and code exercises.
*   **Boundaries**: Must operate strictly within the context of retrieved RAG documents. It shall not generate content beyond the verified knowledge-base.
*   **Ownership**: AI Engineering Division

### 2.2 Navigation Assistant
*   **Responsibility**: Converts natural language queries into semantic searches and maps the optimal learning route through the concept graph.
*   **Boundaries**: Must interact with `knowledge-graph.json` to find conceptual nodes and prerequisites.
*   **Ownership**: Platform Engineering & AI Engineering

### 2.3 Knowledge Authoring Agent
*   **Responsibility**: Scans and pre-validates new curriculum files submitted by contributors.
*   **Boundaries**: Must validate files against the JSON Schema specifications. It shall reject files containing formatting or schema errors.
*   **Ownership**: Developer Experience (DX) & Editorial Division

### 2.4 Knowledge Review Agent
*   **Responsibility**: Performs semantic checks across subject maps to find logical holes or missing links.
*   **Boundaries**: Scans all taxonomies and mappings to flag logical inconsistencies.
*   **Ownership**: Editorial Division & AI Engineering

### 2.5 Personalization Engine
*   **Responsibility**: Analyzes learner progress logs and schedules dynamic review intervals.
*   **Boundaries**: Queries user logs and updates recommendation vectors. It shall not modify course contents.
*   **Ownership**: Platform Engineering

### 2.6 Admin Assistant
*   **Responsibility**: Monitore server logs, flags security anomalies, and checks rate-limiting violations.
*   **Boundaries**: Read-only access to system telemetry logs and database metrics.
*   **Ownership**: Operations & Security

---

## 3. Prompt Management Standards
All system prompts must follow the templates stored in `editorial/prompt-library.md`. Prompts shall enforce:
*   **Context Grounding**: Instructing the model to answer *only* using the provided text.
*   **Formatting Rules**: Outputting structured JSON or clean markdown using LaTeX mathematical expressions.
