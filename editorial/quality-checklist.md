# Ascendrite Content Quality Checklist

This document details the mandatory Quality Assurance (QA) checklist that every topic, module, and subject map must pass before being merged and published.

---

## 1. Document Purpose and Scope
*   **Purpose**: Standardizes the review and validation gates for all educational assets and subject mapping profiles.
*   **Scope**: Governs peer reviews, editorial reviews, and automated commit-validation runners.
*   **Intended Audience**: Human editors, content reviewers, and automated auditing agents.
*   **Related Documents**:
    *   [Editorial Style Guide](editorial-style-guide.md)
    *   [Platform Philosophy](../docs/governance/platform-philosophy.md)
*   **Ownership**: Head of Editorial Division & Quality Assurance Lead

---

## 2. Structural & Grammatical QA
*   [ ] **Voice & Tone**: The narrative must remain objective, formal, and written in the third person or inclusive first-person plural ("we"). Conversational filler is eliminated.
*   [ ] **No Emojis**: The content must contain zero Unicode emojis.
*   [ ] **Terminology Consistency**: Terms must match centralized definitions. Cross-topic relative references must use verified IDs (e.g. `machine-learning-m1-t1`).

---

## 3. Technical & Mathematical QA

### 3.1 Mathematics and Derivations
*   [ ] **Formatting**: All inline math must use single dollar signs (`$`) and block math must use double dollar signs (`$$`).
*   [ ] **KaTeX Compatibility**: Math syntax must render correctly in both client-side engines and static engines (Pandoc, WeasyPrint).
*   [ ] **Derivation Steps**: Complex equations must document intermediate algebraic transformations, rather than leaping directly to final results.

### 3.2 Engineering Accuracy & Complexity
*   [ ] **Production Context**: Explanations must address real-world systems bottlenecks (e.g. memory alignment, serialization overhead, cache lines, I/O wait states).
*   [ ] **Complexity Annotation**: Every major algorithm block and query must document its Big-O time and space complexity in docstrings.
*   [ ] **Reference Implementations**: Python, JavaScript, and shell code examples must be zero-dependency, containing no placeholder parameters, `pass` directives, or `// TODO` statements.

---

## 4. Assessment & Diagram QA

### 4.1 Quizzes and Mock Interviews
*   [ ] **Bloom's Taxonomy Alignment**: Learning objectives must use measurable verbs (e.g. Analyze, Derive, Design).
*   [ ] **Distractor Soundness**: Quizzes must contain exactly four options, with realistic wrong answers representing common traps. Detailed explanations must be written for all options.
*   [ ] **Dialogue Structure**: Mock interviews must use the standard Candidate-Interviewer dialogue structure, including common mistakes, correct answers, and final code.

### 4.2 Code Examples & Visual Diagrams
*   [ ] **Mermaid Diagram Quality**: Diagrams must use standardized flow charts and clear node names, rendering cleanly on both dark and light UI canvases.
*   [ ] **Syntax Validation**: Diagrams must compile without syntax errors. All node shapes must use standard bracket notation (e.g., `["Label"]` instead of HTML wrappers).
