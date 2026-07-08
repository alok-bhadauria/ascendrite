# Ascendrite Code Style Guide

## Document Metadata
*   **Purpose**: Standardizes coding styles, naming conventions, formatting guidelines, and architectural expectations for curriculum programming examples.
*   **Scope**: Governs all code blocks, code exercises, examples, and practice skeletons inside the knowledge base.
*   **Intended Audience**: All curriculum authors, code coordinators, and code review agents.
*   **Related Documents**:
    *   [Editorial Style Guide](editorial-style-guide.md)
    *   [Platform Philosophy](../docs/governance/platform-philosophy.md)
*   **Ownership**: Quality Assurance Lead & Head of Platform Engineering

---

## 1. Supported Languages and Environments

### 1.1 Primary Languages
*   **Python**: Used for Data Science, Machine Learning, and scripting. Code must target Python 3.10+ and comply with PEP-8.
*   **TypeScript/JavaScript**: Used for Web Development and Node.js runtimes. Must use strict typing and ES6+ features.
*   **Go**: Used for distributed systems and concurrency models. Must comply with `gofmt` and idiomatic Go guidelines.
*   **Rust**: Used for systems programming and memory safety. Must follow `rustfmt` guidelines.

### 1.2 Secondary Languages
*   **SQL**: Keywords must be written in uppercase (e.g. `SELECT`, `INSERT`, `WHERE`). Queries must use clear aliases.
*   **HTML/CSS**: Must use semantic HTML5 elements. CSS must map to theme variables.
*   **Shell Scripts**: Must use `bash` compatibility syntax and start with a proper shebang (e.g. `#!/usr/bin/env bash`).
*   **C++**: Must target C++17 or C++20, utilizing smart pointers (`std::unique_ptr`, `std::shared_ptr`) to ensure memory safety.

---

## 2. Formatting & Naming Conventions
*   **Line Length Bounds**: Code blocks must not exceed 80 characters per line. This prevents text wrapping in web viewports and printed PDF sheets.
*   **Indentation**:
    *   Python, TypeScript, Go: 4 spaces indentation.
    *   HTML, CSS, JSON: 2 spaces indentation.
    *   Tabs are strictly prohibited; spaces must be used instead.
*   **Naming Conventions**:
    *   `snake_case`: Python variables, functions, and file paths.
    *   `camelCase`: TypeScript variables and functions.
    *   `PascalCase`: Class names in all object-oriented contexts.

---

## 3. Commenting & Explanation Guidelines
*   **Inline Comments**: Comments must describe *why* an action happens rather than *what* the code does. Standard operations (e.g., iterating a list) must not have comments.
*   **Markdown Explanations**: Long code blocks must be broken down and explained in the surrounding markdown prose using numbered lists, rather than writing massive comment blocks inside the code.
*   **Docstrings**: All public functions and classes must contain a structured docstring defining arguments, types, return variables, and possible raises.

---

## 4. Best Practices & Performance
*   **Resource Allocation**: Code examples must explicitly close all allocated resources (e.g. database connections, file handlers, network sockets) using standard wrappers (like Python’s `with` context blocks or Go’s `defer` statements).
*   **No Placeholders**: Example scripts must be fully functional. The use of `pass`, `...`, or `// TODO` placeholder comments is prohibited.
*   **Complexity Annotations**: Every major algorithm block must document its time and space complexity using Big-O notation.
*   **Error Handling**: Code must handle exceptions explicitly (using try-except/catch blocks) rather than swallowing errors or returning blank outputs.
