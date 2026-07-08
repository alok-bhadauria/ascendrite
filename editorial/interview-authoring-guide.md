# Interview Authoring Guide

## Document Metadata
*   **Purpose**: Outlines criteria for drafting platform technical interview prep materials and system design questions.
*   **Scope**: Applies to all interview preparation files and mock recitations in the curriculum database.
*   **Intended Audience**: Interview prep writers, technical recruiters, and AI content agents.
*   **Related Documents**:
    *   [Content Authoring Guide](content-authoring-guide.md)
    *   [Examples Style Guide](examples-style-guide.md)
*   **Ownership**: Head of Editorial Division & Lead Technical Recruiter

---

## 1. Industry Standard Alignment

Interview prep materials must prepare learners for senior-level engineering interviews at global technology firms:
*   **Theoretical Questions**: Focus on deep runtime, memory, and compiler mechanics (e.g. how garbage collection algorithms function, JVM memory boundaries).
*   **Practical Coding Problems**: Require clean implementations of algorithms, emphasizing optimal time/space complexity optimizations.
*   **System Design Challenges**: Focus on large-scale distributed architectures, rate limiting, consensus protocols, database scaling, and message queue integration.

---

## 2. Interview Card Structure

Every interview preparation module must include:
*   **Primary Question**: A clear, industry-aligned engineering prompt.
*   **Optimal Response Strategy**: A structured breakdown explaining how to approach the answer.
*   **Technical Explanation**: The core explanation, supported by diagrams or code blocks where appropriate.
*   **Follow-Up Scenarios**: 3-5 progressive follow-up questions that probe deeper scaling tradeoffs.

---

## 3. System Design Expectations

When authoring system design questions, writers must format solutions around:
*   **Requirements Gathering**: Functional and non-functional requirements (e.g., QPS targets, latency budgets).
*   **System Architecture Diagrams**: Describing components, load balancers, caching tiers, and write paths.
*   **Detailed Bottlenecks**: Quantifying system scaling limits and failure scenarios (e.g., split-brain, cache stampedes, network partitions).
