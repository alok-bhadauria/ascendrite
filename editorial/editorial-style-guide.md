# Ascendrite Editorial Style Guide

This document is the master editorial standard and publishing constitution of the Ascendrite platform. Every contributor—whether human author, artificial intelligence agent, curriculum architect, editor, or reviewer—must adhere strictly to these guidelines.

---

## 1. Vision and Educational Alignment
The editorial vision of Ascendrite aligns with the [Project Vision](../docs/governance/project-vision.md) and [Product Philosophy](../docs/governance/product-philosophy.md).
*   **Intuition Before Formalism**: Concepts must be motivated by a practical system bottleneck before introducing mathematical derivations or code.
*   **Rigorous Accuracy**: Contributors must not simplify concepts to the point of introducing technical inaccuracies. Mathematical representations and hardware mechanics must be presented exactly as they exist in professional systems.
*   **Industrial Alignment**: Every topic must culminate in actual engineering execution, focusing on real-world systems optimization.

---

## 2. Pedagogy & Writing Standards

### 2.1 The Dual-Loop Pedagogy
All curriculum contents must support the [Learning Philosophy](../docs/governance/learning-philosophy.md):
1.  **Conceptual Loop**: Translates high-level intuition into formal mathematical and theoretical models.
2.  **Practical Loop**: Translates theoretical models into executable, production-grade code and system architectures.

### 2.2 Knowledge Density and Prose
The writing tone must remain objective and analytical. Contributors shall write in the style of authoritative engineering specifications rather than blog posts:
*   **Decluttered Prose**: Authors must avoid conversational fluff, conversational prefaces (e.g., "In this section, we will..."), and first-person singular viewpoints.
*   **No Emojis**: The use of emojis is strictly prohibited across all content layers to preserve a textbook-like aesthetic.
*   **Technical Neutrality**: Writers should present system limits, tradeoffs, and metrics objectively, without declaring specific frameworks as "best" or "worst" unless backed by benchmarks.

---

## 3. Vocabulary and Typography Specifications
*   **Code Formatting**: Variables, class names, functions, files, directories, API paths, and console commands must be wrapped in backticks (e.g., `git merge`, `main()`, `/path/to/project`).
*   **Key Terms**: Technical terms must be highlighted in **boldface** on their first occurrence.
*   **Mathematical Notation**: All mathematical expressions must use KaTeX/LaTeX syntax. Wrap inline math in single dollar signs (e.g. $x \in \mathbb{R}$) and block equations in double dollar signs (e.g. $$\mathbf{A}\mathbf{x} = \lambda\mathbf{x}$$).

---

## 4. Chapter & Topic Structuring Rules
Every topic file (stored as structured JSON) must follow the standard keys defined in `topic.schema.json`:
1.  **Learning Objectives**: A list of 3-5 measurable outcomes using Bloom's Taxonomy verbs (e.g. Analyze, Derive, Design).
2.  **Introduction & Historical Context**: Short background framing the engineering challenge.
3.  **Theoretical Architecture / Mathematical Foundation**: Core formulas, proofs, diagrams, and explanations.
4.  **Reference Implementation**: Complete, documented code blocks with input/output examples.
5.  **Design Trade-Offs & Scaling**: Detailed analysis of time/space complexity, hardware constraints, and failure modes.
6.  **Revision & Synthesis**: Takeaway concepts, quick reference equations, and review lists.

---

## 5. Contributor & AI Agent Guidelines

### 5.1 Human Contributor Checklist
Before submitting a pull request, contributors must run:
1.  `python scratch/validate_knowledge_integrity.py` to check for orphaned IDs or broken links.
2.  `python scratch/validate_ai_notes.py` to ensure JSON format and syntax correctness.
3.  Verify that all code snippets execute cleanly with zero placeholder blocks.

### 5.2 AI Agent Ingestion Rules
Autonomous agents authoring or modifying curriculum files must comply with these constraints:
*   **Strict Schema Compliance**: All output JSON objects must validate against Draft 2020-12 schemas under `knowledge-base/schemas/`.
*   **No Narrative Prefaces**: AI agents shall generate only the requested JSON/markdown payload directly, without conversational intros or comments.
*   **Non-Hallucination**: Agents must verify library API versions, mathematical facts, and code syntax before writing.
