import numpy as np


def compute_iou_practice(
    box_a: tuple[float, float, float, float],
    box_b: tuple[float, float, float, float],
) -> float:
    """Calculates the Intersection over Union (IoU) of two bounding boxes.

    Args:
        box_a: (x1, y1, x2, y2) bounds
        box_b: (x1, y1, x2, y2) bounds

    Returns:
        float: Calculated IoU ratio
    """
    # 1. Unpack coordinates
    xa1, ya1, xa2, ya2 = box_a
    xb1, yb1, xb2, yb2 = box_b

    # 2. Determine intersection box boundaries
    inter_x1 = max(xa1, xb1)
    inter_y1 = max(ya1, yb1)
    inter_x2 = min(xa2, xb2)
    inter_y2 = min(ya2, yb2)

    # 3. Calculate width and height of the intersection box
    inter_w = max(0.0, inter_x2 - inter_x1)
    inter_h = max(0.0, inter_y2 - inter_y1)

    # 4. Compute areas
    inter_area = inter_w * inter_h
    area_a = (xa2 - xa1) * (ya2 - ya1)
    area_b = (xb2 - xb1) * (yb2 - yb1)
    union_area = area_a + area_b - inter_area

    if union_area == 0.0:
        return 0.0

    return inter_area / union_area


if __name__ == "__main__":
    print("--- Running IoU Bounds Practice ---")

    # Case 1: Simple overlapping boxes
    box_1 = (10, 10, 20, 20)  # Area = 100
    box_2 = (15, 10, 25, 20)  # Area = 100
    # Overlap is from x=15 to 20, y=10 to 20 -> area 50. Union = 100 + 100 - 50 = 150
    # IoU = 50 / 150 = 1/3
    val_1 = compute_iou_practice(box_1, box_2)
    print(f"Case 1 IoU: {val_1:.5f}")
    assert np.isclose(val_1, 1.0 / 3.0)

    # Case 2: Completely separate boxes
    box_3 = (0, 0, 5, 5)
    box_4 = (10, 10, 15, 15)
    val_2 = compute_iou_practice(box_3, box_4)
    print(f"Case 2 IoU: {val_2:.5f}")
    assert np.isclose(val_2, 0.0)

    # Case 3: Nested boxes (containment)
    box_5 = (0, 0, 10, 10)  # Area = 100
    box_6 = (2, 2, 8, 8)    # Area = 36 (inside box_5)
    # Overlap is box_6 (area 36). Union is box_5 (area 100)
    # IoU = 36 / 100 = 0.36
    val_3 = compute_iou_practice(box_5, box_6)
    print(f"Case 3 IoU: {val_3:.5f}")
    assert np.isclose(val_3, 0.36)

    print("\n  [PASS] IoU bounds practice verified successfully.")
