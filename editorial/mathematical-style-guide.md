# Ascendrite Mathematical Style Guide

This document defines the mathematical formatting conventions, notations, LaTeX rules, and typographical standards for all technical content across the Ascendrite platform.

---

## 1. Document Purpose and Scope
*   **Purpose**: Standardizes mathematical notation, LaTeX symbols, derivations, and complexity analysis formatting.
*   **Scope**: Governs all mathematical formulations, derivations, LaTeX strings, and proofs inside the knowledge base.
*   **Intended Audience**: All curriculum authors, academic editors, and content review agents.
*   **Related Documents**:
    *   [Editorial Style Guide](editorial-style-guide.md)
    *   [Learning Philosophy](../docs/governance/learning-philosophy.md)
*   **Ownership**: Lead Educational Systems Designer & Mathematical Reviewer

---

## 2. Mathematical Notation & Conventions

### 2.1 Variable Naming Standards
To maintain cross-topic continuity, mathematical symbols must adhere to the following standards:
*   **Scalars**: Represented by lowercase, italicized letters (e.g., $x, y, a, b$).
*   **Vectors**: Represented by lowercase, boldface, non-italicized letters (e.g., $\mathbf{x}, \mathbf{y}, \mathbf{w}$). Vectors shall be assumed to be column vectors unless transposed.
*   **Matrices**: Represented by uppercase, boldface, non-italicized letters (e.g., $\mathbf{A}, \mathbf{B}, \mathbf{X}$).
*   **Sets**: Represented by uppercase calligraphic or double-struck letters (e.g., $\mathcal{S}$ or $\mathbb{S}$). Real numbers must be represented as $\mathbb{R}$.

### 2.2 Standard Parameters
Writers must use standard parameter names:
*   **Learning Rate**: Represented by $\alpha$.
*   **Regularization Coefficient**: Represented by $\lambda$.
*   **Weights and Biases**: Represented by $\mathbf{w}$ (weights vector) and $b$ (bias scalar).
*   **System Parameters**: Represented by $\theta$.

### 2.3 Operations and Indexes
*   **Transposition**: Matrix transposition must be represented as $\mathbf{A}^{\top}$ (using `^{\top}`).
*   **Trace and Determinant**: Traces and determinants must use roman operators: $\text{Tr}(\mathbf{A})$ and $\det(\mathbf{A})$.
*   **Matrix Indexing**: Element in row $i$ and column $j$ of matrix $\mathbf{A}$ must be represented as $A_{ij}$ or $A_{i,j}$.

---

## 3. Calculus and Optimization Notations
*   **Derivatives**: Standard derivatives must be written as $\frac{dy}{dx}$. Partial derivatives must be written as $\frac{\partial f}{\partial x}$.
*   **Gradients and Jacobians**: The gradient vector of function $f$ must be written as $\nabla f(\mathbf{x})$. Jacobians must be written as bold $\mathbf{J}$, and Hessians must be written as bold $\mathbf{H}$.
*   **Argmin/Argmax**: Optimization arguments must use standard operator names: $\operatorname{argmin}_{\mathbf{x}}$ and $\operatorname{argmax}_{\mathbf{x}}$.

---

## 4. Probability and Complexity Notations
*   **Expectation and Variance**: Expectations must be represented as $\mathbb{E}[X]$ and variances as $\text{Var}(X)$.
*   **Probability Distributions**: Probability densities must use lowercase $p(x)$ or $f(x)$, and conditional distributions must be written as $P(A \mid B)$ (using `\mid` instead of a raw pipe character).
*   **Complexity Bounds**: Algorithmic complexity bounds must use standard notations: $O(n)$ for upper bounds, $\Omega(n)$ for lower bounds, and $\Theta(n)$ for tight bounds.
