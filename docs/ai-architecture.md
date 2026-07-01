# AI Architecture: RAG Pipelines, Semantic Search, and Agent Workflows

---

## 1. Architectural Strategy for AI Services
The Ascendrite platform incorporates artificial intelligence as a core service. The AI subsystem focuses on three main capabilities:
1.  **Personalized AI Tutor:** A chatbot capable of answering complex learner questions using curriculum materials as context.
2.  **Semantic Search:** Vector-based search allowing students to query topics by concepts rather than exact keywords.
3.  **Adaptive Assessments:** Dynamic generator loops that create personalized practice tests based on student progress anomalies and weak topics.

---

## 2. Retrieval-Augmented Generation (RAG) Ingestion
To prevent the LLM from generating hallucinatory explanations, all tutor queries pass through a local **RAG Pipeline**:

```
[JSON Knowledge Base] --> [Parser] --> [Chunking (by Topic/Callout)]
                                             |
                                             v
[LLM Prompt Synthesis] <-- [Retrieve] <-- [Vector Store (e.g. Pinecone/pgvector)]
```

### Ingestion Flow
1.  **Parsing:** The pipeline parses notes, revision, and interview JSON documents.
2.  **Chunking:** Content is chunked by topics and callout blocks, maintaining context tags.
3.  **Embeddings:** Chunks are converted into 1536-dimensional vectors using an embedding model (e.g., `text-embedding-3-small`).
4.  **Vector Storage:** Vectors and JSON source pointers are indexed in a vector store database.

### Query and Synthesis Flow
When a user asks a question, the API server:
1.  Embeds the user's query into a vector representation.
2.  Performs a cosine similarity search on the vector store to fetch the top 3 matching chunks.
3.  Injects the query and matching JSON chunks into a system prompt template and passes it to the LLM (e.g. GPT-4o) to synthesize the response.

---

## 3. Semantic Search Architecture
Traditional keyword search fails when users search for concepts (e.g., searching for \"heap performance\" returns nothing if the title is \"Binary Heap Complexity\").
*   Semantic search embeds search strings and scans the vector store.
*   Results return the most conceptually relevant notes, revision cards, and mock interview sections, ranked by similarity scores.

---

## 4. AI Agent Workflows
To support active learning, autonomous agents manage specific student lifecycles:
*   **Adaptive Profiler Agent:** Analyzes quiz submissions and mistake logs. If it detects key gaps in user performance, it generates a custom review module, mapping prerequisites using the `subject-map.json` dependencies.
*   **Code Reviewer Agent:** Scans practice submissions, compiles code in a safe sandbox, evaluates unit tests, and provides line-by-line feedback.

---

## 5. Prompt Engineering Constitution
All system prompts must follow the templates stored in `editorial/prompt-library.md`.

### Prompt Constraints
*   **Context Grounding:** The prompt must instruct the model to answer *only* based on the retrieved context, returning \"I do not know\" if the answer is not present in the curriculum logs.
*   **Formatting:** Enforce clean markdown responses, matching KaTeX math styling, and enclosing code blocks in proper syntax tags.
*   **JSON-Schema Enforcement:** To ensure the API server parses agent responses successfully, the system prompt must require JSON-structured outputs validated against a defined schema.
