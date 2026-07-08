# Ascendrite Domain Reference

**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture & Governance Division
**Last Updated:** 2026-07-09

### Reference Context
This document is derived directly from the constitutional source of truth, the [Ascendrite Master Blueprint](file:///E:/Projects/Ascendrite/blueprint/ascendrite-master-blueprint.md). For detailed operational checks and development standards associated with these domains, refer to the [Engineering Checklists](file:///E:/Projects/Ascendrite/blueprint/engineering-checklists.md).

---

## Actor
- **Explanation**: A distinct entity interacting with the platform. Actors include Guest, Learner, Author, Moderator, Administrator, and System. Each actor is bound to a defined role and security policy.
- **Ownership**: Identity Domain
- **Related Domains**: Workspace, Event

## Agent
- **Explanation**: A specialized, autonomous AI processing unit orchestrating specific cognitive tasks. Examples include the Learning Agent (guiding learning paths) and the Navigation Agent (answering structural queries).
- **Ownership**: Intelligence Domain
- **Related Domains**: Metadata, RAG, State Machine

## Assessment
- **Explanation**: An educational evaluation asset designed to assess concept comprehension. Assessments are classified as quizzes, coding exercises, or projects, and are versioned alongside the knowledge base.
- **Ownership**: Practice Domain
- **Related Domains**: Knowledge, Workspace

## Dashboard
- **Explanation**: The default layout grid within a workspace, dynamically displaying data providers and widget widgets based on the active actor's metadata config.
- **Ownership**: Workspace Domain
- **Related Domains**: Theme, Actor, Personalization

## Domain
- **Explanation**: A high-level logical division of the platform representing a distinct business area (such as Knowledge or Identity). Domains maintain strict interface separation.
- **Ownership**: Platform Domain
- **Related Domains**: State Machine, Metadata

## Event
- **Explanation**: A record of a discrete action or state change within the platform. Events are published to event handlers or collected by log collectors for audit trails.
- **Ownership**: Operations Domain
- **Related Domains**: Telemetry, Actor

## Knowledge
- **Explanation**: The collective educational database of the platform, structured hierarchically through Domains, Disciplines, Subjects, Modules, Topics, Concepts, and Assets.
- **Ownership**: Knowledge Domain
- **Related Domains**: Metadata, Assessment

## Metadata
- **Explanation**: Structural data defining relations, validation rules, and layout configurations. It controls how content renders, assets relate, and visual components display.
- **Ownership**: Platform Domain
- **Related Domains**: Knowledge, Theme

## Notification
- **Explanation**: Messages delivered to users regarding system events, moderation queue changes, or community updates. Notifications can be persistent (stored) or transient (toasts).
- **Ownership**: Platform Domain
- **Related Domains**: Event, Actor

## Personalization
- **Explanation**: The runtime customization of the learning experience (such as custom dashboards, widget configurations, and learning paces) tailored to learner metrics.
- **Ownership**: Workspace Domain
- **Related Domains**: Actor, Theme

## Recommendation
- **Explanation**: Algorithmic suggestions recommending next steps in a syllabus or specific practice problems based on a learner's progress telemetry.
- **Ownership**: Intelligence Domain
- **Related Domains**: Knowledge, Personalization

## Search
- **Explanation**: The platform search engine providing indexing and query resolution across knowledge bases, workspaces, files, and community discussions.
- **Ownership**: Platform Domain
- **Related Domains**: Knowledge, Workspace

## State Machine
- **Explanation**: A system component controlling entity lifecycles (such as workspaces or agents) via defined states, inputs, transitions, and transition guards.
- **Ownership**: Platform Domain
- **Related Domains**: Workspace, Agent

## Telemetry
- **Explanation**: The pipeline responsible for capturing, collecting, and exporting metrics, API latency logs, error rates, and model inference statistics.
- **Ownership**: Operations Domain
- **Related Domains**: Event, Telemetry

## Theme
- **Explanation**: Visual styling metadata (such as color values, typography rules, spacing scales) parsed at runtime to configure UI views and accessibility settings.
- **Ownership**: Platform Domain
- **Related Domains**: Metadata, Dashboard

## Workspace
- **Explanation**: The stateful client interface where authenticated learners perform all activities, unifying dashboards, files, scratchpads, and AI conversations.
- **Ownership**: Workspace Domain
- **Related Domains**: Actor, State Machine

## Capability
- **Explanation**: A specific platform action or access right (e.g., Read, Write, Approve, Publish) granted to an actor to operate on a targeted system resource.
- **Ownership**: Identity Domain
- **Related Domains**: Actor, Permission

## Knowledge Service
- **Explanation**: The core platform layer coordinating data retrieval, caching, authorization verification, index compilation, and metadata validation.
- **Ownership**: Knowledge Domain
- **Related Domains**: Knowledge, Metadata, Knowledge Storage

## Knowledge Storage
- **Explanation**: The private, secure datastore housing proprietary educational assets (Notes, Revision, Interview, Code examples, and assessments).
- **Ownership**: Knowledge Domain
- **Related Domains**: Knowledge, Knowledge Service

## Permission
- **Explanation**: The individual authorization token assigned to actors, supporting hierarchical inheritance down the curriculum taxonomy nodes.
- **Ownership**: Identity Domain
- **Related Domains**: Actor, Capability

