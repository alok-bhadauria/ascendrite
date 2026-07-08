# Editorial Style Guide

## Document Metadata
*   **Purpose**: Outlines global writing standards, voice, tone, formatting conventions, and glossary mappings.
*   **Scope**: Governs all technical writing, descriptions, and metadata schemas inside the platform.
*   **Intended Audience**: Human authors, editors, review panels, and AI content generation agents.
*   **Related Documents**:
    *   [Educational Philosophy](educational-philosophy.md)
    *   [Content Authoring Guide](content-authoring-guide.md)
*   **Ownership**: Head of Editorial Division & Lead Educational Systems Designer

---

## 1. Vision and Educational Alignment

The editorial vision of Ascendrite enforces three core standards across all educational materials:
*   **Intuition Before Formalism**: Concepts must be motivated by real-world engineering bottlenecks prior to introducing formal mathematical definitions, hardware details, or code.
*   **Technical Accuracy**: Content must remain mathematically and architecturally accurate. Authors must avoid oversimplifying concepts to the point of introducing inaccuracies.
*   **Industrial Applicability**: Curriculum modules must culminate in practical system execution and optimization strategies.

---

## 2. Pedagogy & Writing Standards

### 2.1 Tone and Voice
*   **Tone**: Objective, analytical, and authoritative. Write in the style of professional technical specifications.
*   **Voice**: Third-person perspective only. Avoid conversational prefaces (e.g., "In this chapter, we will learn...").
*   **No Emojis**: The use of emojis is strictly prohibited in all user-facing content, documentation, and JSON metadata.

### 2.2 Content Density
*   Eliminate editorial fluff.
*   Maintain a high ratio of information to prose. Focus on system limits, resource tradeoffs, performance bottlenecks, and design decisions.

---

## 3. Formatting & Typography Conventions

*   **Code Syntax**: Wrap variable names, database collections, functions, file paths, API endpoints, and console commands in backticks (e.g., `api/v1/auth`, `user_id`).
*   **Emphasis**: Highlight key technical terms in **boldface** on their first occurrence within a topic.
*   **Mathematical Formulations**: Format all mathematical expressions using KaTeX. Wrap inline math in single dollar signs (e.g. $f(x) = y$) and block equations in double dollar signs (e.g. $$\nabla^2 \Phi = 0$$).

---

## 4. Chapter & Topic Structuring Rules

Every curriculum topic must populate the following sections defined in Pydantic data schemas:
1.  **Learning Objectives**: List 3-5 measurable objectives using verbs from Bloom's Taxonomy (e.g. "Derive", "Analyze", "Optimize").
2.  **Introduction & Motivation**: Establish the engineering problem being solved.
3.  **Theoretical Foundation**: Detail the mathematical definitions, hardware behaviors, and system schemas.
4.  **Reference Implementation**: Provide runnable, commented code examples without placeholders.
5.  **Scaling & Tradeoffs**: Document time/space complexity (Big-O) and resource limits.
6.  **Summary & Review**: Highlight key takeaways and formulas.

---

## 5. Glossary & Terminology Standards

To prevent naming collisions and RAG model lookup confusion:
*   **Term Format**: Standardize glossary term names as singular, lowercase nouns where applicable.
*   **Acronyms & Abbreviations**: Resolve abbreviations to their full names (e.g., map "PCA" to "Principal Component Analysis").
*   **Definitions**: Begin definitions with a concise sentence stating the term's classification, followed by its mathematical or architectural context.
*   **Namespace Isolation**: Segregate subject-specific terminology inside `knowledge-assets.json` to prevent collisions between disciplines (e.g., "Kernel" in Operating Systems vs. Machine Learning).
