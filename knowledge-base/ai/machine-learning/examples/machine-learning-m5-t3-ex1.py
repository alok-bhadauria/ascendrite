import numpy as np


class IsolationTreeNode:
    """A node in an Isolation Tree."""

    def __init__(self, left=None, right=None, split_feature=None, split_val=None, size=0):
        self.left = left
        self.right = right
        self.split_feature = split_feature
        self.split_val = split_val
        self.size = size  # Number of samples in the node
        self.is_leaf = left is None and right is None


def fit_isolation_tree(X: np.ndarray, current_depth: int, max_depth: int) -> IsolationTreeNode:
    """Recursively builds an Isolation Tree by selecting random features and split points."""
    n_samples, n_features = X.shape

    # Base cases for recursion: maximum depth reached or node contains only 1 sample
    if current_depth >= max_depth or n_samples <= 1:
        return IsolationTreeNode(size=n_samples)

    # 1. Randomly select a feature index
    feature_idx = np.random.randint(0, n_features)
    feature_vals = X[:, feature_idx]

    min_val = np.min(feature_vals)
    max_val = np.max(feature_vals)

    # If all feature values are identical, we cannot split
    if min_val == max_val:
        return IsolationTreeNode(size=n_samples)

    # 2. Randomly select a split value uniformly between min and max
    split_val = np.random.uniform(min_val, max_val)

    # 3. Partition data
    left_mask = feature_vals < split_val
    X_left = X[left_mask]
    X_right = X[~left_mask]

    # Recursively build left and right subtrees
    left_child = fit_isolation_tree(X_left, current_depth + 1, max_depth)
    right_child = fit_isolation_tree(X_right, current_depth + 1, max_depth)

    return IsolationTreeNode(
        left=left_child,
        right=right_child,
        split_feature=feature_idx,
        split_val=split_val,
        size=n_samples,
    )


def c_factor(n: int) -> float:
    """Computes the average path length of an unsuccessful search in a Binary Search Tree (BST)."""
    if n <= 1:
        return 0.0
    if n == 2:
        return 1.0
    euler_constant = 0.5772156649
    return float(2.0 * (np.log(n - 1) + euler_constant) - (2.0 * (n - 1) / n))


def get_path_length(x: np.ndarray, node: IsolationTreeNode, current_depth: int) -> float:
    """Traverses the tree to find the path length of sample x."""
    if node.is_leaf:
        # If leaf, path length is current depth plus the adjustment factor c(node.size)
        return current_depth + c_factor(node.size)

    feature_val = x[node.split_feature]
    if feature_val < node.split_val:
        return get_path_length(x, node.left, current_depth + 1)
    else:
        return get_path_length(x, node.right, current_depth + 1)


class IsolationForest:
    """An ensemble of Isolation Trees for anomaly detection."""

    def __init__(self, n_estimators: int = 100, max_samples: int = 256):
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.trees = []

    def fit(self, X: np.ndarray) -> "IsolationForest":
        n_samples = X.shape[0]
        subsample_size = min(self.max_samples, n_samples)
        max_depth = int(np.ceil(np.log2(max(subsample_size, 2))))

        self.trees = []
        for _ in range(self.n_estimators):
            # Draw random subsample without replacement
            indices = np.random.choice(n_samples, size=subsample_size, replace=False)
            X_sub = X[indices]
            tree = fit_isolation_tree(X_sub, current_depth=0, max_depth=max_depth)
            self.trees.append(tree)

        return self

    def compute_anomaly_score(self, X: np.ndarray) -> np.ndarray:
        """Computes the anomaly score s(x, N) for each sample in X."""
        n_samples = X.shape[0]
        expected_paths = np.zeros(n_samples)

        # Average path length across the forest
        for i in range(n_samples):
            x = X[i]
            paths = [get_path_length(x, tree, current_depth=0) for tree in self.trees]
            expected_paths[i] = np.mean(paths)

        # Compute BST normalization factor using subsample size
        subsample_size = min(self.max_samples, n_samples)
        c_n = c_factor(subsample_size)

        if c_n == 0.0:
            return np.zeros(n_samples)

        # Score s(x, N) = 2^(-E[h(x)] / c(N))
        return 2.0 ** (-expected_paths / c_n)


if __name__ == "__main__":
    # Generate normal cluster in 2D
    np.random.seed(42)
    X_normal = np.random.normal(loc=0.0, scale=0.5, size=(100, 2))

    # Inject deliberate outliers (anomalies) far from the normal cluster
    X_anomalies = np.array([
        [4.5, 4.5],
        [-4.5, -4.5],
        [5.0, -5.0]
    ])

    X_all = np.vstack([X_normal, X_anomalies])

    # Fit Isolation Forest
    forest = IsolationForest(n_estimators=100, max_samples=64)
    forest.fit(X_all)

    # Compute scores
    scores = forest.compute_anomaly_score(X_all)

    print("Isolation Forest Anomaly Detection (Pure NumPy):")
    print(f"Average score for normal points: {np.mean(scores[:100]):.5f}")
    print(f"Score for outlier [4.5, 4.5]:   {scores[100]:.5f}")
    print(f"Score for outlier [-4.5, -4.5]: {scores[101]:.5f}")
    print(f"Score for outlier [5.0, -5.0]:   {scores[102]:.5f}")
