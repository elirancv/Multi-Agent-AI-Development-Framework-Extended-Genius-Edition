"""Tests for deterministic seeding."""

import random

from src.orchestrator.seed import seed_for


def test_seed_deterministic():
    """Test that seeding produces deterministic results."""
    seed_for("run1", "stage1")
    val1 = random.random()
    
    seed_for("run1", "stage1")
    val2 = random.random()
    
    # Same run_id and stage should produce same seed
    assert val1 == val2


def test_seed_different_runs():
    """Test that different run_ids produce different seeds."""
    seed_for("run1", "stage1")
    val1 = random.random()
    
    seed_for("run2", "stage1")
    val2 = random.random()
    
    # Different run_ids should produce different seeds
    assert val1 != val2


def test_seed_different_stages():
    """Test that different stages produce different seeds."""
    seed_for("run1", "stage1")
    val1 = random.random()
    
    seed_for("run1", "stage2")
    val2 = random.random()
    
    # Different stages should produce different seeds
    assert val1 != val2

