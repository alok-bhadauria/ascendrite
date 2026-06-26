import numpy as np


class MultiLayerPerceptron:
    """Implements a Multi-Layer Perceptron (MLP) forward propagation from scratch.

    Supports custom layer dimensions and standard activation functions.
    """

    def __init__(self, layer_sizes: list[int], activation: str = "relu"):
        """Initializes the MLP parameters (weights and biases).

        Args:
            layer_sizes: List of integers containing dimensions of each layer.
              e.g., [input_dim, hidden_dim_1, hidden_dim_2, output_dim].
            activation: Activation function for hidden layers ('relu', 'sigmoid',
              'tanh').
        """
        self.layer_sizes = layer_sizes
        self.activation_name = activation.lower()

        # Initialize parameter containers
        self.weights = []
        self.biases = []

        # Initialize weights and biases using a simple uniform distribution
        # In practice, Xavier or He initialization should be used (derived in Module 2)
        np.random.seed(42)
        for i in range(len(layer_sizes) - 1):
            w_shape = (layer_sizes[i + 1], layer_sizes[i])
            b_shape = (layer_sizes[i + 1], 1)

            # Standard scale for initialization
            scale = np.sqrt(2.0 / layer_sizes[i])
            w = np.random.normal(loc=0.0, scale=scale, size=w_shape)
            b = np.zeros(b_shape)

            self.weights.append(w)
            self.biases.append(b)

    def _activate(self, z: np.ndarray) -> np.ndarray:
        """Applies the configured activation function element-wise."""
        if self.activation_name == "relu":
            return np.maximum(0.0, z)
        elif self.activation_name == "sigmoid":
            return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))
        elif self.activation_name == "tanh":
            return np.tanh(z)
        else:
            raise ValueError(f"Unknown activation function: {self.activation_name}")

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Executes forward propagation.

        Args:
            x: Input feature matrix of shape (n_samples, input_dim).

        Returns:
            np.ndarray: Network predictions of shape (n_samples, output_dim).
        """
        # Transpose input matrix to shape (input_dim, n_samples) for column-vector operations
        a = x.T

        # Iterate through hidden layers
        num_layers = len(self.layer_sizes) - 1
        for l in range(num_layers - 1):
            w = self.weights[l]
            b = self.biases[l]

            # Linear combination: z^(l) = W^(l) * a^(l-1) + b^(l)
            # z shape: (dim_l, n_samples)
            z = w @ a + b

            # Activation: a^(l) = f(z^(l))
            a = self._activate(z)

        # Output layer forward pass (typically uses raw linear outputs or Softmax)
        w_out = self.weights[-1]
        b_out = self.biases[-1]
        z_out = w_out @ a + b_out

        # For this example, we return the raw linear pre-activation outputs transposed back to (n_samples, output_dim)
        return z_out.T


if __name__ == "__main__":
    # Define a network: 3 input units, two hidden layers (size 4 and 3), and 2 output units
    layer_config = [3, 4, 3, 2]
    print(f"Initializing MLP with Layer Architecture: {layer_config}")

    mlp = MultiLayerPerceptron(layer_sizes=layer_config, activation="relu")

    # Generate synthetic input batch: 5 samples with 3 features each
    X_input = np.array(
        [
            [1.0, -0.5, 2.0],
            [-1.5, 0.0, 0.5],
            [0.0, 1.5, -1.0],
            [2.0, 2.0, 2.0],
            [-0.5, -0.5, -0.5],
        ]
    )

    print("\nInput Batch (shape: 5 samples, 3 features):\n", X_input)

    # Compute forward pass
    output = mlp.forward(X_input)

    print("\nForward Propagation Complete.")
    print("Output Layer Predictions (shape: 5 samples, 2 outputs):\n", output)

    # Output dimensions check
    assert output.shape == (
        5,
        2,
    ), "Output dimensions do not match layer configuration!"
    print("\n  [PASS] Forward propagation dimensions verified successfully.")
