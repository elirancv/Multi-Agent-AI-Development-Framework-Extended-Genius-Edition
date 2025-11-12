"""Deterministic seeding for reproducibility."""

from __future__ import annotations

import hashlib
import random

try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


def seed_for(run_id: str, stage: str) -> None:
    """
    Set deterministic seed based on run_id and stage.

    Ensures reproducible results for the same run_id/stage combination.

    Args:
        run_id: Run identifier
        stage: Stage name
    """
    h = hashlib.sha256(f"{run_id}:{stage}".encode()).digest()
    seed = int.from_bytes(h[:8], "little") & 0x7FFFFFFF
    random.seed(seed)
    if NUMPY_AVAILABLE:
        try:
            np.random.seed(seed)
        except Exception:
            pass
