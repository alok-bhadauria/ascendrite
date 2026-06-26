# Ascendrite Content Quality Checklist

This document details the mandatory Quality Assurance (QA) checklist that every topic, module, and subject map must pass before being merged and published.

---

## 1. Document Purpose and Scope

To maintain the reputation of Ascendrite as a premium technical publisher, all content must be validated against a unified set of criteria. This checklist is executed by human editors, peer reviewers, and automated auditing agents.

---

## 2. Structural and Grammatical QA

Checks targeting readability, grammar, and alignment with the editorial style.

### Editorial and Grammar
*   [ ] The tone is objective, authoritative, and analytical.
*   [ ] Active voice is utilized; filler conversational phrasing is eliminated.
*   [ ] No emojis are present in any section.

### Terminology and Consistency
*   [ ] Every technical term matches the spelling and context of the centralized glossary.
*   [ ] Cross-references point to correct Topic IDs.

---

## 3. Technical and Mathematical QA

Checks targeting code, calculations, and mathematical rigor.

### Mathematics and Derivations
*   [ ] All inline math uses single dollar signs ($) and block math uses double dollar signs ($$).
*   [ ] Mathematical derivations display all critical algebraic steps clearly.
*   [ ] Variables correspond to standard conventions (italicized scalars, bold matrices, etc.).

### Engineering Accuracy and Industry Relevance
[Placeholder: Checklist for assessing architecture layouts, systems claims, and production benchmarks.]

### Code Quality
*   [ ] Code is PEP-8/idiomatically formatted and syntactically valid (no syntax errors).
*   [ ] No placeholder comments (e.g., `// TODO`) are present.
*   [ ] Time and Space Complexity are explicitly documented.

---

## 4. Assessment and Pedagogical QA

Checks targeting quizzes, exercises, and progression paths.

### Learning Outcomes and Difficulty Progression
[Placeholder: Verifying that objectives align with Bloom's Taxonomy and that difficulty scales appropriately.]

### Interview and Revision Coverage
[Placeholder: Verifying that mock interview questions are structured properly and that revision cards capture core points.]

### Example Quality and Diagram Quality
[Placeholder: Reviewing examples for real-world applicability and verifying diagrams conform to palette standards.]

---

## 5. Platform, RAG, and Publishing Readiness

Checks targeting parsing, rendering, and distribution formatting.

*   [ ] **JSON Validation:** All JSON configurations pass strict schema checks (validated using JSON parsers, with double-escaped LaTeX strings).
*   [ ] **RAG Readiness:** Headings are semantic, clear, and contextually self-contained for semantic chunking.
*   [ ] **Platform Readiness:** Relative links are valid; page-break indicators conform to PDF printing engines.
*   [ ] **Publishing Readiness:** Licensing, copyright metadata, and watermarks are configured inside `book-metadata.json`.
