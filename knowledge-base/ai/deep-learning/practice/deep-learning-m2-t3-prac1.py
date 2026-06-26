class EarlyStopping:
    """Implements an Early Stopping checker to terminate training when

    validation loss fails to improve after a set number of epochs.
    """

    def __init__(self, patience: int = 5, min_delta: float = 0.0):
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss = None
        self.patience_counter = 0

    def step(self, val_loss: float) -> bool:
        """Executes a check step for the validation loss of the current epoch.

        Args:
            val_loss: Scalar loss value evaluated on validation data.

        Returns:
            bool: True if training must stop, False otherwise.
        """
        # If first epoch, initialize best_loss and continue
        if self.best_loss is None:
            self.best_loss = val_loss
            return False

        # Check if validation loss improved by at least min_delta
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.patience_counter = 0  # Reset counter
        else:
            self.patience_counter += 1  # Increment counter

        # Check if patience limit has been reached
        if self.patience_counter >= self.patience:
            return True  # Stop training

        return False


if __name__ == "__main__":
    print("--- Running Early Stopping Callback Practice ---")

    # Initialize callback: wait for 3 epochs of no improvement, delta = 0.01
    early_stop = EarlyStopping(patience=3, min_delta=0.01)

    # Simulated validation losses:
    # Epoch 1: 0.50 (initial best)
    # Epoch 2: 0.45 (improvement, delta = 0.05 > 0.01) -> counter = 0
    # Epoch 3: 0.445 (no meaningful improvement, delta = 0.005 < 0.01) -> counter = 1
    # Epoch 4: 0.46 (loss rose) -> counter = 2
    # Epoch 5: 0.455 (loss dropped slightly, but no improvement over best 0.45) -> counter = 3 -> STOP

    losses = [0.50, 0.45, 0.445, 0.46, 0.455]
    expected_stops = [False, False, False, False, True]

    for epoch, (loss, expected) in enumerate(zip(losses, expected_stops), 1):
        should_stop = early_stop.step(loss)
        print(
            f"Epoch {epoch}: Loss = {loss:.3f} | Trigger Stop: {should_stop} | Counter = {early_stop.patience_counter}"
        )
        assert (
            should_stop == expected
        ), f"Early stopping check failed at epoch {epoch}!"

    print("\n  [PASS] Early stopping logic and patience checks verified.")
