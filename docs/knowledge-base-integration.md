# Knowledge Base Integration: Parsing Pipelines and Asset Validation

---

## 1. Decentralized Ingestion Pipeline
Ascendrite implements a portable, git-friendly content database architecture. The entire curriculum resides in `knowledge-base/` using structured JSON templates. 

During API server startup, an ingestion parser scans the categories:

```
[Server Startup]
  |
  +-- Read subject folder directories (ai/, core-cs/, web-development/, etc.)
  +-- Locate and validate 'syllabus.json' structures
  +-- Parse subject-metadata, subject-map, and knowledge-assets
  +-- Load and parse notes, revision, interview, example, practice, quiz, and diagrams JSON files
  +-- Compile into an in-memory curriculum cache (hash-map search indices)
```

By keeping the curriculum cache in-memory, content searches and lesson routing runs at $O(1)$ lookup time, entirely bypassing database latency.

---

## 2. Subject Metadata & Relationship Mapping
*   **`syllabus.json`**: Structures the hierarchy (Modules -> Topics -> Subtopics) using strict unique ID vectors.
*   **`subject-metadata.json`**: Customizes client theme color codes, course levels, and learning budgets.
*   **`subject-map.json`**: Implements topological sorting to map prerequisite path constraints:
    ```json
    {
      "topic_id": "cn-m3-t1",
      "prerequisites": ["cn-m2-t5", "cn-m2-t4"]
    }
    ```
    The client evaluates user progress records against this map to lock/unlock downstream lessons.

---

## 3. Dynamic Diagram & Source Code Embedding
Since all curriculum assets are JSON, structural visual diagrams and running code strings are represented using serialization formatting:
*   **Diagrams (`diagrams/*.json`)**: Contain a `code` string block mapped using Mermaid format. The web client reads this block and compiles the syntax into a responsive SVG diagram.
*   **Examples (`examples/*.json`)**: Contain executable scripts wrapped in JSON blocks. The API server serves these strings, enabling the web client to render them inside a custom editor widget.

---

## 4. Content Validation Suite (`validate_ai_notes.py`)
To prevent invalid formatting in production bundles, an automation runner enforces compilation checks before git commits:
1.  **JSON Validation:** Parses files through native Python `json.loads` to catch trailing commas or escape errors.
2.  **Emoji Verification:** Rejects files containing any Unicode emoji blocks, ensuring an academic tone.
3.  **Local Path Safety:** Validates string fields against absolute paths and protocol leaks.
4.  **Schema Consistency:** Confirms that all JSON files contain the exact key layout defined in the styling guides.
