import numpy as np


class DynamicLossScalerNumPy:
    """Simulates PyTorch's torch.cuda.amp.GradScaler dynamic loss scaling logic in NumPy."""

    def __init__(
        self,
        init_scale: float = 65536.0,
        growth_factor: float = 2.0,
        backoff_factor: float = 0.5,
        growth_interval: int = 2000,
    ):
        self.scale = init_scale
        self.growth_factor = growth_factor
        self.backoff_factor = backoff_factor
        self.growth_interval = growth_interval
        self.steps_since_last_overflow = 0

    def scale_loss(self, loss: float) -> float:
        """Scales the loss value."""
        return loss * self.scale

    def unscale_gradients(
        self, grads: dict[str, np.ndarray]
    ) -> dict[str, np.ndarray]:
        """Divides gradients by the scale factor to restore original values."""
        unscaled_grads = {}
        for name, g in grads.items():
            unscaled_grads[name] = g / self.scale
        return unscaled_grads

    def check_overflow_and_update(self, grads: dict[str, np.ndarray]) -> bool:
        """Checks for NaN/Inf in gradients and updates the scale factor.

        Args:
            grads: Dictionary of gradient tensors

        Returns:
            bool: True if overflow occurred (step should be discarded), False otherwise
        """
        overflow = False
        for name, g in grads.items():
            # Check for NaNs or Infs
            if np.any(np.isnan(g)) or np.any(np.isinf(g)):
                overflow = True
                break

        if overflow:
            # Scale down and reset counter
            old_scale = self.scale
            self.scale *= self.backoff_factor
            self.steps_since_last_overflow = 0
            print(f"  [OVERFLOW] NaN/Inf detected! Scaling down: {old_scale} -> {self.scale}")
            return True
        else:
            self.steps_since_last_overflow += 1
            if self.steps_since_last_overflow >= self.growth_interval:
                # Scale up if stable for growth_interval steps
                old_scale = self.scale
                self.scale *= self.growth_factor
                self.steps_since_last_overflow = 0
                print(f"  [STABLE] No overflow for {self.growth_interval} steps. Scaling up: {old_scale} -> {self.scale}")
            return False


if __name__ == "__main__":
    print("--- Running Dynamic Loss Scaling Verification ---")

    # Initialize scaler with low growth interval for testing
    scaler = DynamicLossScalerNumPy(init_scale=1024.0, growth_interval=3)

    # Mock parameters and loss
    loss = 0.5
    scaled_loss = scaler.scale_loss(loss)
    assert scaled_loss == 512.0
    print("Loss scaling verified.")

    # 1. Simulate stable steps (no NaNs/Infs)
    grads_stable = {"W": np.array([0.1, 0.2, 0.3])}
    
    # Step 1: stable
    overflow = scaler.check_overflow_and_update(grads_stable)
    assert not overflow
    assert scaler.scale == 1024.0

    # Step 2: stable
    overflow = scaler.check_overflow_and_update(grads_stable)
    assert not overflow
    assert scaler.scale == 1024.0

    # Step 3: stable -> should trigger growth because growth_interval = 3
    overflow = scaler.check_overflow_and_update(grads_stable)
    assert not overflow
    assert scaler.scale == 2048.0
    print("Dynamic scale expansion verified.")

    # Unscaling check
    unscaled = scaler.unscale_gradients({"W": np.array([20.48, 40.96])})
    assert np.allclose(unscaled["W"], np.array([0.01, 0.02]))
    print("Gradient unscaling values verified.")

    # 2. Simulate overflow step (contains Inf)
    grads_overflow = {"W": np.array([0.1, np.inf, 0.3])}
    overflow = scaler.check_overflow_and_update(grads_overflow)
    assert overflow
    assert scaler.scale == 1024.0  # Should backoff from 2048 to 1024
    print("Overflow detection and scale reduction verified.")

    print("\n  [PASS] Mixed precision scaling logic verified.")
