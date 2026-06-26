# Ascendrite Revision Card: Computer Vision Tasks

## Single-Stage Detection: YOLO

*   **Grid Cell Logic:** Divides input image into an $S \times S$ grid. If an object center falls in a cell, that cell is responsible for its detection.
*   **Bounding Box Vectors:** Predicts $B$ boxes per cell. Each box has 5 elements: $(x, y, w, h, c)$, where $x, y$ are cell-relative, $w, h$ are image-relative, and $c$ is the objectness confidence score.
*   **Tensor Shape:** Total output tensor is shaped $S \times S \times (5B + C)$, where $C$ is the number of class probabilities.

## Anchor Boxes, IoU & NMS

*   **Anchor Boxes:** Pre-defined aspect ratios and scales cluster-fitted to dataset targets. Model predicts deltas relative to these shapes.
*   **Intersection over Union (IoU):** Overlap ratio between predicted box $A$ and ground truth $B$:
    $$\text{IoU}(A, B) = \frac{\text{Area}(A \cap B)}{\text{Area}(A \cup B)}$$
*   **Non-Maximum Suppression (NMS) Protocol:**
    1.  Filter out boxes below confidence threshold (e.g. $0.5$).
    2.  Select box with highest confidence.
    3.  Compute IoU with all remaining boxes of the same class.
    4.  Discard boxes with $\text{IoU} \ge \text{NMS Threshold}$ (e.g. $0.45$).
    5.  Repeat until no boxes remain.

## U-Net: Semantic Segmentation

*   **Encoder-Decoder Layout:** Contractive encoder downsamples inputs (capturing context) and expanding decoder upsamples representations (recovering spatial coordinates).
*   **Skip Connections:** Concatenates high-resolution features from contracting encoder directly with upsampled decoder features at each corresponding level. This preserves fine spatial details (boundaries and edges) lost during pooling.
