# Curriculum Framework

## Document Metadata
*   **Purpose**: Outlines the educational database taxonomy, metadata structures, and curriculum dependency models.
*   **Scope**: Governs the file schemas under `knowledge-base/schemas/` and structural mapping scripts.
*   **Intended Audience**: Knowledge engineers, content authors, database managers, and AI indexing agents.
*   **Related Documents**:
    *   [Knowledge Base Integration](../docs/architecture/knowledge-base-integration.md)
    *   [Repository Structure](../docs/development/repository-structure.md)
*   **Ownership**: Knowledge Systems Architect & Head of Editorial Division

---

## 1. Educational Taxonomy Hierarchy

Syllabus content is organized using a strict hierarchical structure, ensuring modular data indexing and query parsing:

```
[Domain] (e.g., Artificial Intelligence)
   └── [Discipline] (e.g., Machine Learning)
         └── [Subject] (e.g., Deep Learning)
               └── [Module] (e.g., Convolutional Neural Networks)
                     └── [Topic] (e.g., Spatial Convolutions)
                           └── [Concept] (e.g., Stride, Padding)
                                 └── [Asset] (Notes, Revision, Interview, Code)
```

---

## 2. Metadata Schema Mapping

Every entity in the taxonomy must carry a corresponding JSON schema definition:
*   **`subject.schema.json`**: Defines name, identifier, learning outcomes, and references.
*   **`curriculum.schema.json`**: Houses module listings, topic sequences, and execution ordering maps.
*   **`topic.schema.json`**: Restricts content structures, matching concepts, practice hooks, and visualization parameters.
*   **`practice.schema.json`**: Governs coding challenges, input/output validation cases, and testing criteria.

---

## 3. Dependency Modeling

Prerequisite relationships must be declared explicitly in JSON metadata to coordinate study flows:
*   **Hard Prerequisites**: Modules or topics that must be completed before starting the target module.
*   **Soft Recommendations**: Suggested review materials for background context.
*   **Validation Rules**: No circular dependencies are permitted. The database build pipeline must validate that the syllabus remains a Directed Acyclic Graph (DAG).
