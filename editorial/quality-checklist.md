# Quality Checklist

## Document Metadata
*   **Purpose**: Outlines operational checklists that must be completed before publishing curriculum assets.
*   **Scope**: Governs all pre-publication validation, PR reviews, and AI audits for knowledge base files.
*   **Intended Audience**: Content authors, editors, QA reviewers, and AI auditing agents.
*   **Related Documents**:
    *   [Quality Assurance Framework](quality-assurance-framework.md)
    *   [Publishing Workflow](publishing-workflow.md)
*   **Ownership**: Head of Editorial Division & Quality Assurance Lead

---

## 1. Notes Checklist
- [ ] **Motivation**: The note begins with a real-world system bottleneck or engineering motivation.
- [ ] **Bloom Alignment**: Mapped to 3-5 learning objectives using measurable verbs (e.g. Derive, Analyze).
- [ ] **Typography**: Variable names, file layouts, and API paths are wrapped in backticks.
- [ ] **Formatting**: No Unicode emojis are present in the text body.
- [ ] **Tone**: Prose is written in an objective, third-person perspective with zero conversational filler.

---

## 2. Revision Checklist
- [ ] **Conciseness**: The content contains only high-density summaries, key formulas, and quick references.
- [ ] **Card Structure**: Every card contains a defined Prompt (Front) and Answer (Back).
- [ ] **Formula Explanations**: Equations define variables inline rather than leaving them implicit.
- [ ] **Schema Conformance**: Validates against the `revision.schema.json` configuration template.

---

## 3. Interview Checklist
- [ ] **Difficulty**: Question represents a typical L6+ engineering or system design challenge.
- [ ] **Response Guide**: Includes an optimal response strategy detailing step-by-step problem resolution.
- [ ] **Follow-ups**: Mapped to 3-5 progressive follow-up questions testing trade-offs and constraints.
- [ ] **Design Aspects**: Solutions cover scaling boundaries, message queues, and partition strategies.

---

## 4. Assessment Checklist
- [ ] **Quiz Options**: Every MCQ has exactly four options.
- [ ] **Plausible Distractors**: Incorrect answers reflect common engineering misconceptions or logical traps.
- [ ] **Explanatory Depth**: Explanations cover why the correct answer is correct and why each distractor is incorrect.
- [ ] **State Validation**: Coding exercises define clear test input structures and target output assertions.

---

## 5. Examples Checklist
- [ ] **Archetype**: Classified as Educational, Real-World, Case Study, or Business Scenario.
- [ ] **Prerequisites**: Relies only on concepts that have been introduced in the current or prior topics.
- [ ] **Complexity**: Explanations specify time and space complexity using Big-O notation.
- [ ] **Trade-offs**: Explains alternative approaches (e.g., CPU vs. GPU, iterative vs. recursive) where applicable.

---

## 6. Diagrams Checklist
- [ ] **Mermaid Syntax**: Compiles without syntax errors. Labeled axes are present for plots.
- [ ] **Color Contrast**: Maintains WCAG AA contrast ratios (4.5:1 minimum) in light and dark canvas views.
- [ ] **Styling Rules**: Distributes links using distinct line styles (e.g., dashed for optional, solid for required).
- [ ] **Clean Labeling**: Standard bracket notations are used for node labels without embedded HTML formatting.

---

## 7. Code Checklist
- [ ] **Syntax Integrity**: Code blocks compile and execute without exceptions or interpreter errors.
- [ ] **Line Limits**: Line length does not exceed 80 characters.
- [ ] **Comments**: Inline comments describe the *why* of actions, leaving basic logic self-documenting.
- [ ] **No Placeholders**: Script blocks contain no `TODO`, `pass`, `...`, or placeholder variables.
- [ ] **Resource Safety**: Uses context managers (e.g., `with` statements) or explicit close methods for I/O loops.

---

## 8. Publishing Checklist
- [ ] **Branch Naming**: Target branch matches branching naming rules (e.g. `feature/34-concept-indexing`).
- [ ] **Pre-commit Passes**: Local validator runners exit successfully with zero errors.
- [ ] **Schema Check**: Validates against JSON Schema Draft 2020-12 rules.
- [ ] **Graph Integrity**: All linked prerequisite concept IDs resolve to active, non-broken nodes in the graph.

---

## 9. AI Review Checklist
- [ ] **RAG Validation**: Model prompt inputs are enriched with authoritative context from vector stores.
- [ ] **Non-Hallucination**: Verifies library API versions and academic equations against verified docs.
- [ ] **Citations**: Claims are backed by links to canonical RFCs, standards, or documentation.
- [ ] **Attribute Tags**: Mapped to metadata fields tracking model type, prompt version, and verifying editor ID.
