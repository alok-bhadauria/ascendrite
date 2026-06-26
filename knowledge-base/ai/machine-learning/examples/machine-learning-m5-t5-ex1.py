import numpy as np


class UniformAffineQuantizer:
    """Implements 8-bit uniform affine quantization.

    Maps continuous float values to int8 or uint8 representations.
    """

    def __init__(self, bits: int = 8, signed: bool = False):
        self.bits = bits
        self.signed = signed

        # Define integer bounds
        if signed:
            self.q_min = -(2 ** (bits - 1))
            self.q_max = 2 ** (bits - 1) - 1
        else:
            self.q_min = 0
            self.q_max = 2**bits - 1

        self.scale = 1.0
        self.zero_point = 0

    def fit(self, x: np.ndarray) -> None:
        """Computes the scale and zero-point based on the range of input array x."""
        r_min = float(np.min(x))
        r_max = float(np.max(x))

        # Handle edge case where all values are identical
        if r_min == r_max:
            self.scale = 1.0
            self.zero_point = self.q_min
            return

        # 1. Compute scale factor
        self.scale = (r_max - r_min) / (self.q_max - self.q_min)

        # 2. Compute zero-point
        # Z = round(-r_min / S) + q_min
        z_approx = (0.0 - r_min) / self.scale + self.q_min
        self.zero_point = int(np.clip(np.round(z_approx), self.q_min, self.q_max))

    def quantize(self, x: np.ndarray) -> np.ndarray:
        """Quantizes float input array to discrete integer values."""
        # q = clamp(round(x / S) + Z, q_min, q_max)
        scaled_x = x / self.scale
        q = np.round(scaled_x) + self.zero_point
        q_clamped = np.clip(q, self.q_min, self.q_max)
        return q_clamped.astype(np.int32 if self.signed else np.uint32)

    def dequantize(self, q: np.ndarray) -> np.ndarray:
        """Dequantizes integer array back to estimated float representation."""
        # r_hat = S * (q - Z)
        return self.scale * (q.astype(float) - self.zero_point)


def simulated_qat_forward(
    w: np.ndarray, quantizer: UniformAffineQuantizer
) -> np.ndarray:
    """Simulates quantization noise on weights (quantize followed by dequantize)."""
    quantizer.fit(w)
    q = quantizer.quantize(w)
    w_hat = quantizer.dequantize(q)
    return w_hat


def simulated_qat_backward(grad_output: np.ndarray) -> np.ndarray:
    """Implements backpropagation using the Straight-Through Estimator (STE).

    The derivative of the rounding operation is assumed to be 1.0.
    """
    # STE passes the gradient straight through without modifications:
    # dL/dw = dL/dw_hat * dw_hat/dw = dL/dw_hat * 1.0
    return grad_output


if __name__ == "__main__":
    # 1. Initialize data representing activations/weights
    np.random.seed(42)
    original_weights = np.random.normal(loc=0.0, scale=2.5, size=(4, 4))
    print("Original Weights (FP32):\n", original_weights)

    # 2. Asymmetric Unsigned 8-bit Quantization (uint8)
    quantizer_uint8 = UniformAffineQuantizer(bits=8, signed=False)
    quantizer_uint8.fit(original_weights)

    print("\n--- Unsigned 8-bit Quantization (uint8) ---")
    print(f"Computed Scale:      {quantizer_uint8.scale:.6f}")
    print(f"Computed Zero-Point: {quantizer_uint8.zero_point}")

    quantized_uint8 = quantizer_uint8.quantize(original_weights)
    print("Quantized representation (uint8):\n", quantized_uint8)

    reconstructed_uint8 = quantizer_uint8.dequantize(quantized_uint8)
    print("Dequantized reconstruction:\n", reconstructed_uint8)

    l2_error_uint8 = np.sqrt(np.mean((original_weights - reconstructed_uint8) ** 2))
    print(f"Reconstruction RMSE: {l2_error_uint8:.6f}")

    # 3. Symmetric/Asymmetric Signed 8-bit Quantization (int8)
    quantizer_int8 = UniformAffineQuantizer(bits=8, signed=True)
    quantizer_int8.fit(original_weights)

    print("\n--- Signed 8-bit Quantization (int8) ---")
    print(f"Computed Scale:      {quantizer_int8.scale:.6f}")
    print(f"Computed Zero-Point: {quantizer_int8.zero_point}")

    quantized_int8 = quantizer_int8.quantize(original_weights)
    print("Quantized representation (int8):\n", quantized_int8)

    reconstructed_int8 = quantizer_int8.dequantize(quantized_int8)
    print("Dequantized reconstruction:\n", reconstructed_int8)

    l2_error_int8 = np.sqrt(np.mean((original_weights - reconstructed_int8) ** 2))
    print(f"Reconstruction RMSE: {l2_error_int8:.6f}")

    # 4. QAT Simulation with STE
    print("\n--- QAT Forward/Backward Simulation ---")
    # Simulate forward pass (quantization noise injection)
    sim_weights = simulated_qat_forward(original_weights, quantizer_int8)
    print("Simulated Quantized Weights (w_hat):\n", sim_weights)

    # Let's say downstream loss computation yields a dummy output gradient dL/dw_hat
    grad_w_hat = np.ones((4, 4)) * 0.1
    # Backward pass using STE
    grad_w = simulated_qat_backward(grad_w_hat)
    print("Gradient dL/dw using STE:\n", grad_w)
