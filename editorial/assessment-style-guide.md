# Ascendrite Assessment Style Guide

## Document Metadata
*   **Purpose**: Defines pedagogical standards, question-writing guidelines, evaluation criteria, and difficulty progressions for assessments.
*   **Scope**: Governs quiz metadata files (`quiz/*.json`), practice tasks (`practice/*.json`), and mock interviews (`interview/*.json`).
*   **Intended Audience**: All curriculum authors, quiz writers, and review coordinators.
*   **Related Documents**:
    *   [Editorial Style Guide](editorial-style-guide.md)
    *   [Learning Philosophy](../docs/governance/learning-philosophy.md)
*   **Ownership**: Quality Assurance Lead & Head of Editorial Division

---

## 1. Supported Assessment Philosophies

### 1.1 Quiz Philosophy
*   **Purpose**: Rapid validation of conceptual definitions, structural dependencies, API parameters, and syntax.
*   **Format**: Multiple-choice, matching, and fill-in-the-blank questions.

### 1.2 Practice Philosophy
*   **Purpose**: Deepen analytical, mathematical, and coding skills through active execution.
*   **Format**: Multi-step analytical problems, coding challenges with test cases, and algorithmic optimization.

### 1.3 Interview Philosophy
*   **Purpose**: Prepare students for technical screens and system design reviews at top-tier organizations.
*   **Format**: Multi-stage mock conversations, edge-case evaluations, and trade-off discussions.

### 1.4 Revision Philosophy
*   **Purpose**: Compact summaries and flashcard-style reviews.
*   **Format**: Highly structured take-aways, quick-reference cheat sheets, and core checklists.

---

## 2. Pedagogical Design & Progression

### 2.1 Bloom's Taxonomy Alignment
Assessments must evaluate various levels of cognitive learning:
1.  **Remember & Understand (Level 1)**: Conceptual definitions and basic syntax quizzes.
2.  **Apply & Analyze (Level 2)**: Analytical computations, debugging exercises, and algorithm execution.
3.  **Evaluate & Create (Level 3)**: Performance optimization, architectural design, and complex problem-solving.

### 2.2 Difficulty Progression
*   **Easy**: Questions testing recall of basic terms, functions, or parameters. Solve time: under 2 minutes.
*   **Medium**: Application tasks testing intermediate operations, debugging lines, or tracing variables. Solve time: under 5 minutes.
*   **Hard**: High-level synthesis tasks testing mathematical proofs, algorithmic transformations, or multi-step optimizations. Solve time: under 15 minutes.

### 2.3 Adaptive Assessment Metadata Tagging
Every assessment item must be tagged with metadata attributes:
*   `difficulty`: Enum mapping to `Easy`, `Medium`, or `Hard`.
*   `concept_nodes`: Array listing the target concept node IDs from `knowledge-graph.json`.
*   `learning_outcomes`: Array of mapped Bloom's learning outcome indices.

---

## 3. Question Writing & Explanation Standards
*   **Explicit Context**: Questions must provide all required variables, configurations, or input states.
*   **Distractor Plausibility**: Incorrect answers must reflect logical errors or candidate traps, avoiding obvious non-answers.
*   **Explanatory Depth**: Explanations must detail *why* the correct answer is correct and *why* each distractor is incorrect.
