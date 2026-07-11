# Ascendrite Blueprint

Welcome to the architectural blueprint repository for the Ascendrite platform. This directory contains the complete technical architecture, decision records, implementation plans, domain definitions, and contribution checklists.

---

## Purpose

The documents in this directory define the permanent structural boundaries, guidelines, and engineering foundations of Ascendrite. They exist to prevent architectural drift, coordinate development across human engineers and AI agents, and ensure the platform scales modularly.

---

## Reading Priority

1. **[Ascendrite Master Blueprint](ascendrite-master-blueprint.md)**: Read this document first. It is the primary constitutional source of truth, describing the complete architecture, governance, and long-term vision of the platform.
2. **[Implementation Roadmap](implementation-roadmap.md)**: Details the phased development sequence from local setup to production release.
3. **[Architectural Decision Records](architectural-decision-records.md)**: Tracks the historical and current design choices made throughout the platform's lifecycle.
4. **[Domain Reference](domain-reference.md)**: Summarizes essential terminology, definitions, and domain ownership.
5. **[Engineering Checklists](engineering-checklists.md)**: Provides operational checklists that must be completed during development and code reviews.

---

## Directory Relationships

The Ascendrite repository separates concerns across distinct documentation directories:

```
Ascendrite Root
├── blueprint/      # Core technical architecture, ADRs, roadmaps, and engineering guides.
├── docs/           # Product vision, system philosophy, and high-level platform design.
├── editorial/      # Language guidelines and standards for all platform documentation.
└── knowledge-base/ # Syllabus schemas, educational metadata structures, and asset lists.
```

- **`blueprint/`**: Serves as the technical and operational companion to `docs/`, outlining *how* the system is structured and implemented at an engineering level.
- **`docs/`**: Captures *why* specific product and system decisions are made, focusing on long-term philosophy independent of immediate technology.
- **`editorial/`**: Establishes writing standards to ensure consistency across both platform documentation and learning assets.
- **`knowledge-base/`**: Hosts the concrete metadata schemas, subject maps, and JSON files that power the learning catalog.

---

## Contribution Guidelines

Future developers, AI subagents, and content contributors must adhere to the following rules:

* **Conformity**: All implementation tasks, schema designs, and pull requests must align with the specifications defined in [ascendrite-master-blueprint.md](ascendrite-master-blueprint.md).
* **Process**: Before committing code, verify your changes against the relevant checklists in [engineering-checklists.md](engineering-checklists.md).
* **Decisions**: Any changes modifying platform boundaries or introducing new architectural patterns must be proposed and documented via a new Architectural Decision Record in [architectural-decision-records.md](architectural-decision-records.md).
