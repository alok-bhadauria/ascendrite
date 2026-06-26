import numpy as np


def compute_iou(box1: np.ndarray, box2: np.ndarray) -> float:
    """Computes the Intersection over Union (IoU) of two bounding boxes.

    Args:
        box1: Coordinates [x1, y1, x2, y2]
        box2: Coordinates [x1, y1, x2, y2]

    Returns:
        float: IoU value between 0.0 and 1.0
    """
    # Determine intersection coordinates
    x_left = max(box1[0], box2[0])
    y_top = max(box1[1], box2[1])
    x_right = min(box1[2], box2[2])
    y_bottom = min(box1[3], box2[3])

    # Compute intersection area
    intersection_width = max(0.0, x_right - x_left)
    intersection_height = max(0.0, y_bottom - y_top)
    intersection_area = intersection_width * intersection_height

    # Compute individual areas
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

    # Compute union area
    union_area = area1 + area2 - intersection_area

    if union_area == 0.0:
        return 0.0

    return intersection_area / union_area


def non_maximum_suppression(
    boxes: np.ndarray, scores: np.ndarray, iou_threshold: float
) -> list[int]:
    """Applies Non-Maximum Suppression (NMS) to eliminate overlapping boxes.

    Args:
        boxes: NumPy array of shape (N, 4) containing [x1, y1, x2, y2]
        scores: NumPy array of shape (N,) containing objectness confidence scores
        iou_threshold: Overlap limit threshold

    Returns:
        list[int]: Indices of the boxes to keep
    """
    if len(boxes) == 0:
        return []

    # Sort indices by score in descending order
    idxs = np.argsort(scores)[::-1]
    keep = []

    while len(idxs) > 0:
        # Keep the box with highest score
        best_idx = idxs[0]
        keep.append(best_idx)

        if len(idxs) == 1:
            break

        # Compute IoU between selected box and all remaining boxes
        remaining_idxs = idxs[1:]
        ious = np.array(
            [compute_iou(boxes[best_idx], boxes[i]) for i in remaining_idxs]
        )

        # Retain boxes that have an IoU lower than the threshold
        keep_idxs = np.where(ious < iou_threshold)[0]
        idxs = remaining_idxs[keep_idxs]

    return keep


if __name__ == "__main__":
    print("--- Running IoU and NMS Verification ---")

    # 1. Verify IoU Calculation
    boxA = np.array([0.0, 0.0, 2.0, 2.0])  # Area 4
    boxB = np.array([1.0, 1.0, 3.0, 3.0])  # Area 4
    # Intersection is [1, 1, 2, 2] -> Area 1
    # Union is 4 + 4 - 1 = 7
    # IoU = 1/7
    iou_val = compute_iou(boxA, boxB)
    print(f"Calculated IoU: {iou_val:.5f}")
    assert np.isclose(iou_val, 1.0 / 7.0)

    # Identical boxes IoU should be 1.0
    assert np.isclose(compute_iou(boxA, boxA), 1.0)

    # Disjoint boxes IoU should be 0.0
    boxC = np.array([5.0, 5.0, 6.0, 6.0])
    assert np.isclose(compute_iou(boxA, boxC), 0.0)
    print("IoU calculations verified.")

    # 2. Verify NMS pruning
    # Stack of candidate boxes around a single target object
    boxes = np.array(
        [[10.0, 10.0, 50.0, 50.0],  # Box 0 (Main box, high confidence)
         [12.0, 11.0, 48.0, 52.0],  # Box 1 (High overlap with Box 0, lower score)
         [100.0, 100.0, 140.0, 140.0]]  # Box 2 (Different object, high confidence)
    )
    scores = np.array([0.9, 0.75, 0.85])

    # With threshold 0.5, Box 1 should be pruned (its IoU with Box 0 is high)
    # Box 2 should be kept (it is distant, IoU = 0.0)
    keep_indices = non_maximum_suppression(boxes, scores, iou_threshold=0.5)
    print("Kept indices:", keep_indices)
    assert set(keep_indices) == {0, 2}
    print("NMS filtering logic verified.")

    print("\n  [PASS] Computer vision examples verified successfully.")
