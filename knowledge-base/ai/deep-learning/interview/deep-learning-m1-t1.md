# Ascendrite Interview Prep: Neural Foundations

## Q1: Prove the Perceptron Convergence Theorem. Derive both the upper and lower bounds of the weight vector norm, and solve for the maximum number of weight updates.

### Standard Answer
To prove the Perceptron Convergence Theorem, we assume a training dataset that is linearly separable. This implies there exists an optimal unit vector $\mathbf{w}^*$ ($\lVert\mathbf{w}^*\rVert_2 = 1$) and a margin $\gamma > 0$ such that:
$$y_i (\mathbf{w}^{*\top} \mathbf{x}_i) \ge \gamma \quad \forall i$$
where $y_i \in \{-1, 1\}$. Let $R = \max_i \lVert\mathbf{x}_i\rVert_2$ be the maximum boundary of the input features. Starting from an initial weight vector $\mathbf{w}^{(0)} = \mathbf{0}$, we update the weights only when a sample is misclassified:
$$\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} + y_i \mathbf{x}_i$$

#### 1. Derivation of the Lower Bound
We take the inner product of the weight vector after $k$ updates with the optimal unit vector $\mathbf{w}^*$:
$$\mathbf{w}^{(t+1)\\top} \mathbf{w}^* = (\mathbf{w}^{(t)} + y_i \mathbf{x}_i)^{\top} \mathbf{w}^* = \mathbf{w}^{(t)\\top} \mathbf{w}^* + y_i \mathbf{w}^{*\\top} \mathbf{x}_i$$
Using the separating margin assumption ($y_i \mathbf{w}^{*\\top} \mathbf{x}_i \ge \gamma$):
$$\mathbf{w}^{(t+1)\\top} \mathbf{w}^* \ge \mathbf{w}^{(t)\\top} \mathbf{w}^* + \gamma$$
By induction, starting from $\mathbf{w}^{(0)} = \mathbf{0}$, we find:
$$\mathbf{w}^{(k)\\top} \mathbf{w}^* \ge k\gamma$$
Applying the Cauchy-Schwarz inequality ($\mathbf{w}^{(k)\\top}\mathbf{w}^* \le \lVert\mathbf{w}^{(k)}\rVert_2 \lVert\mathbf{w}^*\rVert_2$ where $\lVert\mathbf{w}^*\rVert_2 = 1$):
$$\lVert\mathbf{w}^{(k)}\rVert_2 \ge k\gamma$$

#### 2. Derivation of the Upper Bound
We evaluate the squared L2 norm of the weight vector after $t+1$ updates:
$$\lVert\mathbf{w}^{(t+1)}\rVert_2^2 = \lVert\mathbf{w}^{(t)} + y_i \mathbf{x}_i\rVert_2^2 = \lVert\mathbf{w}^{(t)}\rVert_2^2 + 2 y_i \mathbf{w}^{(t)\\top} \mathbf{x}_i + \lVert\mathbf{x}_i\rVert_2^2$$
Because an update was triggered, sample $i$ was misclassified by $\mathbf{w}^{(t)}$, which mathematically guarantees:
$$y_i \mathbf{w}^{(t)\\top} \mathbf{x}_i \le 0$$
Since $\lVert\mathbf{x}_i\rVert_2^2 \le R^2$, we can simplify:
$$\lVert\mathbf{w}^{(t+1)}\rVert_2^2 \le \lVert\mathbf{w}^{(t)}\rVert_2^2 + R^2$$
By induction, starting from $\mathbf{w}^{(0)} = \mathbf{0}$, we find:
$$\lVert\mathbf{w}^{(k)}\rVert_2^2 \le k R^2$$

#### 3. Solving for the Maximum Updates $k$
Comparing the squared lower bound with the upper bound:
$$k^2 \gamma^2 \le \lVert\mathbf{w}^{(k)}\rVert_2^2 \le k R^2$$
$$k^2 \gamma^2 \le k R^2 \implies k \le \frac{R^2}{\gamma^2}$$
Since the maximum number of weight updates $k$ is bounded by the constant $\frac{R^2}{\gamma^2}$, the Perceptron algorithm must converge in finite steps.

---

## Q2: Prove mathematically why a single-layer perceptron cannot solve the XOR function, and demonstrate how a Multi-Layer Perceptron (MLP) with a single hidden layer resolves this limitation.

### Standard Answer
The XOR logic gate inputs are $\mathbf{x} = [x_1, x_2]^{\top} \in \{0, 1\}^2$ and targets are:
- $x_1=0, x_2=0 \implies y=0$
- $x_1=0, x_2=1 \implies y=1$
- $x_1=1, x_2=0 \implies y=1$
- $x_1=1, x_2=1 \implies y=0$

#### 1. Mathematical Proof of Single Perceptron Failure
A single perceptron defines a linear decision boundary:
$$\mathbf{w}^{\top}\mathbf{x} + b \ge 0 \implies y=1$$
$$\mathbf{w}^{\top}\mathbf{x} + b < 0 \implies y=0$$
Substituting the XOR coordinates into these inequalities:
1.  For $(0,0) \implies b < 0$
2.  For $(0,1) \implies w_2 + b \ge 0 \implies w_2 > 0$ (since $b < 0$)
3.  For $(1,0) \implies w_1 + b \ge 0 \implies w_1 > 0$ (since $b < 0$)
4.  For $(1,1) \implies w_1 + w_2 + b < 0$

Summing inequalities 2 and 3 yields $w_1 + w_2 + 2b \ge 0$. Since $b < 0$, we have:
$$w_1 + w_2 + b > w_1 + w_2 + 2b \ge 0 \implies w_1 + w_2 + b > 0$$
This directly contradicts inequality 4 ($w_1 + w_2 + b < 0$). Thus, no real numbers $w_1, w_2, b$ can satisfy these inequalities simultaneously. The XOR function is non-linearly separable.

#### 2. Resolving XOR with an MLP Hidden Layer
We construct a simple MLP with 2 hidden units $a_1^{(1)}, a_2^{(1)}$ and a step activation function $f(z) = \mathbb{I}_{[0, \infty)}(z)$.
Let hidden unit 1 act as an OR gate:
$$z_1^{(1)} = x_1 + x_2 - 0.5 \implies a_1^{(1)} = \mathbb{I}[x_1 + x_2 \ge 0.5]$$
Let hidden unit 2 act as an AND gate:
$$z_2^{(1)} = x_1 + x_2 - 1.5 \implies a_2^{(1)} = \mathbb{I}[x_1 + x_2 \ge 1.5]$$
The output neuron combines them as:
$$z^{(2)} = a_1^{(1)} - 2a_2^{(1)} - 0.5 \implies y = \mathbb{I}[a_1^{(1)} - 2a_2^{(1)} \ge 0.5]$$

Let us trace the outputs:
*   $(0,0) \implies a_1^{(1)}=0, a_2^{(1)}=0 \implies z^{(2)} = -0.5 \implies y=0$
*   $(0,1) \implies a_1^{(1)}=1, a_2^{(1)}=0 \implies z^{(2)} = 0.5 \implies y=1$
*   $(1,0) \implies a_1^{(1)}=1, a_2^{(1)}=0 \implies z^{(2)} = 0.5 \implies y=1$
*   $(1,1) \implies a_1^{(1)}=1, a_2^{(1)}=1 \implies z^{(2)} = 1 - 2 - 0.5 = -1.5 \implies y=0$

By using a hidden layer, the MLP projects the input points into a new feature space where they are linearly separable, allowing the output layer to solve the problem.

---

## Q3: What happens mathematically if you stack multiple hidden layers in a neural network but only use linear activation functions? Derive the proof.

### Standard Answer
If all activation functions in a multi-layer neural network are linear, the network collapses into a single linear mapping. Stacking layers yields no additional representational capacity.

#### Mathematical Proof
Let the activation function at each layer $l$ be linear: $f^{(l)}(z) = k_l z$. For simplicity, assume $k_l = 1$, so $f^{(l)}(\mathbf{z}^{(l)}) = \mathbf{z}^{(l)}$.
The forward propagation step at layer 1 is:
$$\mathbf{a}^{(1)} = \mathbf{W}^{(1)} \mathbf{x} + \mathbf{b}^{(1)}$$
For layer 2:
$$\mathbf{a}^{(2)} = \mathbf{W}^{(2)} \mathbf{a}^{(1)} + \mathbf{b}^{(2)}$$
Substituting $\mathbf{a}^{(1)}$ into the equation for $\mathbf{a}^{(2)}$:
$$\mathbf{a}^{(2)} = \mathbf{W}^{(2)} \left( \mathbf{W}^{(1)} \mathbf{x} + \mathbf{b}^{(1)} \right) + \mathbf{b}^{(2)}$$
$$\mathbf{a}^{(2)} = \left( \mathbf{W}^{(2)} \mathbf{W}^{(1)} \right) \mathbf{x} + \left( \mathbf{W}^{(2)} \mathbf{b}^{(1)} + \mathbf{b}^{(2)} \right)$$

By induction, for an $L$-layer network:
$$\mathbf{a}^{(L)} = \mathbf{W}^{\text{eff}} \mathbf{x} + \mathbf{b}^{\text{eff}}$$
where:
$$\mathbf{W}^{\text{eff}} = \mathbf{W}^{(L)} \mathbf{W}^{(L-1)} \dots \mathbf{W}^{(1)}$$
$$\mathbf{b}^{\text{eff}} = \mathbf{b}^{(L)} + \sum_{l=1}^{L-1} \left( \prod_{j=l+1}^L \mathbf{W}^{(j)} \right) \mathbf{b}^{(l)}$$

Since the product of multiple matrices is simply another matrix ($\mathbf{W}^{\text{eff}} \in \mathbb{R}^{d_L \times d_0}$) and the bias term sums to a single vector ($\mathbf{b}^{\text{eff}} \in \mathbb{R}^{d_L}$), the mapping from inputs $\mathbf{x}$ to outputs $\mathbf{a}^{(L)}$ remains strictly affine. The network cannot represent any non-linear decision boundary regardless of how many layers are added.
