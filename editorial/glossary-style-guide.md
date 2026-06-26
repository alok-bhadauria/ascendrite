# Ascendrite Glossary Style Guide

This document defines the management rules, formatting structures, and architectural standards for the centralized glossary, abbreviations, and acronyms across the Ascendrite platform.

---

## 1. Document Purpose and Scope

Terminology confusion hinders learning. This guide details how to construct, link, and maintain terms in the centralized glossary database (`knowledge-assets.json`) to guarantee structural and contextual consistency across all technical subjects.

---

## 2. Term Naming and Definitions

Standards for designating terms and writing lexicographical entries.

*   **Term Naming:** Standardize names to singular, lowercase nouns where applicable. Avoid jargon or colloquial terms when standard industry terminology exists.
*   **Definition Standards:** Definitions must start with a concise sentence describing the term's classification and core function, followed by its mathematical or architectural context.

---

## 3. Reference Management

Rules for linking terms across topics and files.

*   **Cross References:** Explain how to link terms to related glossary words (e.g., "See also: **Eigenvalue**").
*   **Aliases, Abbreviations, and Acronyms:** Standardize how alternative names are mapped (e.g., mapping "PCA" to "Principal Component Analysis" and "SVM" to "Support Vector Machine").

---

## 4. Subject-Specific vs. Platform-Wide Terminology

Guidelines for resolving namespace collisions.

*   **Subject-Specific Terminology:** Define terms within the specific context of a subject (e.g., "Kernel" in Operating Systems vs. "Kernel" in Support Vector Machines).
*   **Platform-Wide Terminology:** Establish unified terms for concepts that span multiple disciplines (e.g., "Matrix," "Array," "Graph").
*   **Namespace Resolution:** Guidelines for segregating shared names within the `knowledge-assets.json` databases to prevent client rendering or RAG model lookup confusion.
