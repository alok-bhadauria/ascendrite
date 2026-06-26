# Ascendrite Mathematical Style Guide

This document defines the mathematical formatting conventions, notations, LaTeX rules, and typographical standards for all technical content across the Ascendrite platform.

---

## 1. Document Purpose and Scope

This style guide establishes a uniform language for mathematical expression. By standardizing notation, variables, symbols, proofs, and equations, we ensure that students can transition between topics and subjects (e.g., from machine learning to digital signal processing or algorithms) without encountering notation mismatches.

---

## 2. Mathematical Notation and Conventions

This section defines the mathematical representations across different data structures.

### Variable Naming Conventions
*   **Scalars:** Represented by lowercase, italicized letters (e.g., $x, y, a, b$).
*   **Vectors:** Represented by lowercase, boldface, non-italicized letters (e.g., $\mathbf{x}, \mathbf{y}, \mathbf{w}$).
*   **Matrices:** Represented by uppercase, boldface, non-italicized letters (e.g., $\mathbf{A}, \mathbf{B}, \mathbf{X}$).
*   **Tensors:** Represented by uppercase, boldface, sans-serif or calligraphic letters (e.g., $\mathsf{T}$ or $\mathcal{T}$).
*   **Sets:** Represented by uppercase calligraphic or double-struck letters (e.g., $\mathcal{S}$ or $\mathbb{S}$).

### Greek Symbols
[Placeholder: Guidelines for standard use of Greek letters (e.g., $\alpha$ for learning rates, $\beta$ for weights/biases, $\theta$ for parameters).]

### Matrix, Vector, and Tensor Notations
[Placeholder: Matrix dimensions, indexing styles, operations like transpose $\mathbf{A}^{\top}$, trace $\text{Tr}(\mathbf{A})$, determinant $\det(\mathbf{A})$, and tensor contractions.]

---

## 3. Advanced Calculus and Optimization

Guidelines for representing multivariate calculus and optimization formulations.

### Calculus Notation
[Placeholder: Derivatives $\frac{dy}{dx}$, partial derivatives $\frac{\partial f}{\partial x}$, gradients $\nabla f(\mathbf{x})$, Jacobians $\mathbf{J}$, and Hessians $\mathbf{H}$.]

### Optimization Notation
[Placeholder: Arguing operators $\operatorname{argmin}$, $\operatorname{argmax}$, objective constraints, duality, Lagrangian formulations, and KKT conditions.]

---

## 4. Probability and Complexity

Guidelines for statistical, probabilistic, and computational complexity notation.

### Probability Notation
[Placeholder: Expectation $\mathbb{E}[X]$, variance $\text{Var}(X)$, probability density functions $p(x)$, and conditional distributions $P(A \mid B)$.]

### Complexity Notation
[Placeholder: Big-O $O(n)$, Big-Omega $\Omega(n)$, Big-Theta $\Theta(n)$, small-o $o(n)$ notation, and recurrent relation analysis formatting.]

---

## 5. Theorem, Proof, and Derivation Formatting

Standards for structuring mathematical logical reasoning.

### Theorem Formatting
[Placeholder: Standard templates for Theorems, Lemmas, Corollaries, and Definitions.]

### Proof Formatting
[Placeholder: Logical sequence structure, step justifications, and Q.E.D. symbols.]

### Equation Derivation Philosophy
[Placeholder: Step-by-step guidance on showing intermediate mathematical steps rather than omitting them, ensuring algebraic clarity.]

---

## 6. KaTeX and LaTeX Conventions

Strict formatting conventions for LaTeX syntax in Markdown files.

### Syntax Rules
*   **Inline Equations:** Use single dollar signs: `$equation$`.
*   **Block Equations:** Use double dollar signs: `$$equation$$`.
*   **Escaping in JSON:** Double-escape backslashes in JSON-nested strings (e.g., `\\alpha`, `\\mathbb{R}`).

### Multi-Line Equation Formatting
[Placeholder: Guidelines for using `\begin{aligned}` for multi-line equation alignment.]

---

## 7. Numerical Precision, Units, and Consistency Rules

Guidelines for numerical representations.

*   **Numerical Precision:** Standardize to a specific number of decimal places (e.g., four decimal places for probability, two for percentages) unless context demands exact representations.
*   **Unit Notation:** Guidelines for metric, imperial, and system-specific units.
*   **Mathematical Consistency Rules:** Platform-wide rules to prevent conflicting notations between different authors.
