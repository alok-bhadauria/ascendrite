# Ascendrite Interview Prep: Computer Vision Tasks

## Q1: Walk through the mathematical steps to calculate the Intersection over Union (IoU) of two 2D bounding boxes. What are the edge cases?

### Standard Answer
Given two bounding boxes $A$ and $B$, represented by their coordinate bounds:
$$A = [x_{a1}, y_{a1}, x_{a2}, y_{a2}] \quad \text{and} \quad B = [x_{b1}, y_{b1}, x_{b2}, y_{b2}]$$
Where $(x_1, y_1)$ is the top-left coordinate and $(x_2, y_2)$ is the bottom-right coordinate.

**Step 1: Calculate the Area of both boxes:**
$$\text{Area}(A) = (x_{a2} - x_{a1}) \times (y_{a2} - y_{a1})$$
$$\text{Area}(B) = (x_{b2} - x_{b1}) \times (y_{b2} - y_{b1})$$

**Step 2: Calculate Coordinates of the Intersection Box:**
$$\text{inter\_x1} = \max(x_{a1}, x_{b1})$$
$$\text{inter\_y1} = \max(y_{a1}, y_{b1})$$
$$\text{inter\_x2} = \min(x_{a2}, x_{b2})$$
$$\text{inter\_y2} = \min(y_{a2}, y_{b2})$$

**Step 3: Compute Intersection Area:**
$$\text{inter\_w} = \max(0, \text{inter\_x2} - \text{inter\_x1})$$
$$\text{inter\_h} = \max(0, \text{inter\_y2} - \text{inter\_y1})$$
$$\text{Area}(A \cap B) = \text{inter\_w} \times \text{inter\_h}$$

**Step 4: Compute Union Area:**
$$\text{Area}(A \cup B) = \text{Area}(A) + \text{Area}(B) - \text{Area}(A \cap B)$$

**Step 5: Compute IoU:**
$$\text{IoU} = \frac{\text{Area}(A \cap B)}{\text{Area}(A \cup B)}$$

**Edge Cases:**
1.  **Zero Overlap:** If the boxes do not overlap, $\text{inter\_x2} \le \text{inter\_x1}$ or $\text{inter\_y2} \le \text{inter\_y1}$. The width or height calculation returns 0 via the $\max(0, \dots)$ clamping, yielding an IoU of exactly 0.
2.  **Identical Boxes:** If $A = B$, then $\text{Area}(A \cap B) = \text{Area}(A) = \text{Area}(B)$, and $\text{Area}(A \cup B) = \text{Area}(A) + \text{Area}(A) - \text{Area}(A) = \text{Area}(A)$. The IoU is exactly 1.0.
3.  **Containment:** If $A$ is completely inside $B$, the intersection area is $\text{Area}(A)$. The union area is $\text{Area}(B)$. IoU becomes $\frac{\text{Area}(A)}{\text{Area}(B)}$.

---

## Q2: How does Non-Maximum Suppression (NMS) resolve redundant detections during object detection inference? Write down the sorting and pruning algorithm.

### Standard Answer
**Non-Maximum Suppression (NMS)** is a post-processing step used to eliminate overlapping bounding boxes that detect the same object, retaining only the box with the highest confidence.

**Algorithm Steps:**
Let $P = \{b_1, b_2, \dots\}$ be the set of predicted bounding boxes with their corresponding confidence scores $S = \{s_1, s_2, \dots\}$, and $N_{\text{thresh}}$ be the NMS threshold (e.g. 0.45).

1.  **Confidence Filtering:** Discard all boxes $b_i$ where score $s_i < s_{\text{filter\_thresh}}$ (e.g. 0.5).
2.  **Initialization:** Create an empty list $D$ for keeping final detections.
3.  **Sorting:** Sort the remaining boxes in $P$ in descending order of their confidence scores $S$.
4.  **Selection Loop:** While $P$ is not empty:
    *   Select the box with the highest confidence score from $P$, say $M$.
    *   Move $M$ from $P$ to the final list $D$.
    *   For each remaining box $b_j$ in $P$:
        *   Calculate $\text{IoU}(M, b_j)$.
        *   If $\text{IoU}(M, b_j) \ge N_{\text{thresh}}$, remove $b_j$ from $P$ (as it is considered a duplicate detection of the same object).
5.  **Output:** Return list $D$ containing the final filtered bounding boxes.

---

## Q3: What is the mechanical role of skip connections in U-Net compared to ResNet?

### Standard Answer
While both architectures use skip connections, their layout and mathematical operations differ:

1.  **Mathematical Operation:**
    *   **ResNet:** Uses **element-wise addition** ($y = F(x) + x$). This requires the channel dimensions of the residual path and identity path to be identical.
    *   **U-Net:** Uses **channel-wise concatenation** ($y = \operatorname{concat}(F(x), x)$). If $F(x)$ has shape $(C, H, W)$ and $x$ has shape $(C, H, W)$, the output has shape $(2C, H, W)$.
2.  **Structural Path:**
    *   **ResNet:** Connects adjacent blocks within the same resolution level to allow gradients to flow backward through deep layers.
    *   **U-Net:** Connects symmetrical levels of the contracting path (encoder) across to the expanding path (decoder).
3.  **Role in Feature Spaces:**
    *   **ResNet:** Resolves the vanishing gradient problem in deep networks.
    *   **U-Net:** Resolves the spatial resolution loss problem. The encoder compresses spatial detail to extract abstract semantics. The decoder uses skip connections to copy high-resolution spatial features (like object edges and boundaries) directly from the encoder, combining them with upsampled semantic features to output high-fidelity pixel-wise segmentation maps.
