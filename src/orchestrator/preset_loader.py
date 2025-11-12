"""Preset configuration loader."""

from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any, Dict, Optional

from src.orchestrator.yaml_loader import Policy


def load_preset(preset_name: str) -> Optional[Policy]:
    """
    Load preset configuration.

    Args:
        preset_name: Name of preset (e.g., 'mvp-fast', 'production')

    Returns:
        Policy object or None if preset not found
    """
    presets_path = Path("config/presets.yaml")
    
    if not presets_path.exists():
        return None
    
    with open(presets_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    presets = data.get("presets", {})
    preset_data = presets.get(preset_name)
    
    if not preset_data:
        return None
    
    # Extract policy from preset
    policy_data = preset_data.get("policy", {})
    
    # Convert to Policy object
    # Note: Policy uses 'advisors' not 'council', and 'weights' is nested in advisors
    return Policy(
        version=int(policy_data.get("version", "1")) if isinstance(policy_data.get("version"), str) else policy_data.get("version", 1),
        score_thresholds=policy_data.get("score_thresholds"),
        retries=policy_data.get("retries"),
        timeouts=policy_data.get("timeouts"),
        budget=policy_data.get("budget"),
        advisors=policy_data.get("advisors"),  # Map to advisors field
    )


def list_presets() -> Dict[str, str]:
    """
    List all available presets.

    Returns:
        Dictionary mapping preset names to descriptions
    """
    presets_path = Path("config/presets.yaml")
    
    if not presets_path.exists():
        return {}
    
    with open(presets_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    presets = data.get("presets", {})
    return {
        name: preset.get("description", "") 
        for name, preset in presets.items()
    }

