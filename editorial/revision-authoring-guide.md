# Revision Authoring Guide

## Document Metadata
*   **Purpose**: Outlines rules for authoring condensed revision flashcards, summaries, and exam-prep materials.
*   **Scope**: Governs all revision JSON models and spaced-repetition card decks in the knowledge base.
*   **Intended Audience**: Content authors, memory designers, and AI generation agents.
*   **Related Documents**:
    *   [Educational Philosophy](educational-philosophy.md)
    *   [Curriculum Framework](curriculum-framework.md)
*   **Ownership**: Head of Editorial Division & Lead Educational Systems Designer

---

## 1. Revision Philosophy

Revision cards exist to reinforce memory retention and facilitate rapid reference. They do not introduce new concepts or extensive explanations. Instead, they condense pre-studied topics into high-density formulas, code snippets, and direct question-answer pairs.

---

## 2. Card Formatting Rules

Every revision asset must conform to a standardized JSON schema and contain:
*   **Front (Prompt)**: A single, direct question, unfinished formula, or code validation challenge.
*   **Back (Answer)**: The correct definition, complete math formula, or correct code statement.
*   **Context Tags**: Association keys mapping the card to a specific subject topic or concept.

---

## 3. High-Density Formats

*   **Formulas**: Present only the canonical equation, defining variables inline (e.g. $E = mc^2$, where $E$ is energy, $m$ is mass, and $c$ is the speed of light).
*   **Code Skeletons**: Show short, 2-5 line code patterns demonstrating execution syntax.
*   **System Justifications**: Frame prompts around critical architectural tradeoffs (e.g. Front: "Why choose JWT over cookies?" Back: "Decentralized validation scaling, stateless operations, stateless sessions").
