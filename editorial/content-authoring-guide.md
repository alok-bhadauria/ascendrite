# Content Authoring Guide

## Document Metadata
*   **Purpose**: Outlines the guidelines for drafting primary reading materials, conceptual explanations, and technical notes.
*   **Scope**: Governs all markdown narratives, explanations, and code commentary inside topic directories.
*   **Intended Audience**: Content authors, technical editors, and AI writing assistants.
*   **Related Documents**:
    *   [Editorial Style Guide](editorial-style-guide.md)
    *   [Mathematical Style Guide](mathematical-style-guide.md)
*   **Ownership**: Head of Editorial Division & Lead Educational Systems Designer

---

## 1. Writing Quality & Progression

Core reading materials (Notes) must read like a premium, published textbook:
*   **Progressive Depth**: Topics start with fundamental intuition, transition into formal representations and algorithms, and conclude with advanced optimizations and scaling challenges.
*   **Concept-First Motivating**: Every note begins by highlighting a practical system constraint or bottleneck (e.g. why we need red-black tree balancing, why standard gradient descent fails on sparse datasets).
*   **Objective Explanations**: Focus on architectural mechanics, complexity limits, and design trade-offs. Avoid generic assumptions.

---

## 2. Text Formatting and Annotations

To ensure readability:
*   **Boldface**: Highlight core terminology on first mention.
*   **Backticks**: Wrap variable names, database keys, operations, routes, and file layouts.
*   **KaTeX Formulations**: Wrap math inline in `$ ... $` and blocks in `$$ ... $$`.

---

## 3. Callout Block Conventions

Use Markdown quote block syntax with bold alert headers to highlight specific engineering considerations. Do not place callouts consecutively:

> **[System Bottleneck]**
> When scaling write operations, unindexed collections force collections scanning operations, slowing query performance by $O(N)$ lookup costs.

---

## 4. Metadata Mappings

Notes files must link directly to their matching topic metadata schemas:
*   Confirm `topicId` values match their registered syllabus index parent exactly.
*   Tag concepts with related learning tags to support semantic lookup pipelines.
