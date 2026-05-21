from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


STATES = [
    "LEAVE_BAY",
    "LINE_FOLLOW_TO_PICK",
    "TARGET_CONFIRM",
    "PICK_OBJECT",
    "COLOR_CLASSIFY",
    "SORT_DROP",
    "RETURN_HOME",
    "COMPLETE",
]


@dataclass(frozen=True)
class DemoRunConfig:
    run_id: str = "demo_run_001"
    steps: int = 360
    seed: int = 42
    object_color: str = "red"


def _state_for_step(step: int, steps: int) -> str:
    boundaries = [
        (35, "LEAVE_BAY"),
        (120, "LINE_FOLLOW_TO_PICK"),
        (150, "TARGET_CONFIRM"),
        (190, "PICK_OBJECT"),
        (225, "COLOR_CLASSIFY"),
        (280, "SORT_DROP"),
        (steps - 12, "RETURN_HOME"),
        (steps + 1, "COMPLETE"),
    ]
    for limit, state in boundaries:
        if step < limit:
            return state
    return "COMPLETE"


def simulate_run(config: DemoRunConfig) -> pd.DataFrame:
    """Generate deterministic synthetic sensor/control logs for one demo run."""
    rng = np.random.default_rng(config.seed)
    rows: list[dict[str, object]] = []
    for step in range(config.steps):
        state = _state_for_step(step, config.steps)
        line_error = float(rng.normal(0.0, 0.18))
        correction = float(np.clip(38.0 * line_error, -45.0, 45.0))
        left_pwm = int(np.clip(145 - correction, 75, 210))
        right_pwm = int(np.clip(145 + correction, 75, 210))
        ultrasonic_cm = float(48 - 0.22 * step + rng.normal(0, 1.2))
        if state not in {"TARGET_CONFIRM", "PICK_OBJECT"}:
            ultrasonic_cm = max(18.0, ultrasonic_cm + 18.0)
        color_confidence = 0.0
        color_label = "unknown"
        if state in {"COLOR_CLASSIFY", "SORT_DROP", "RETURN_HOME", "COMPLETE"}:
            color_label = config.object_color
            color_confidence = float(np.clip(0.78 + 0.12 * rng.random(), 0, 1))
        servo_angle = {
            "PICK_OBJECT": 68,
            "SORT_DROP": 128,
            "COMPLETE": 90,
        }.get(state, 35)
        event = ""
        if step in {35, 120, 150, 190, 225, 280, config.steps - 12}:
            event = f"enter_{state.lower()}"
        rows.append(
            {
                "run_id": config.run_id,
                "step": step,
                "timestamp_s": round(step * 0.05, 3),
                "state": state,
                "line_error": round(line_error, 4),
                "pid_correction": round(correction, 3),
                "left_pwm": left_pwm,
                "right_pwm": right_pwm,
                "ultrasonic_cm": round(max(4.0, ultrasonic_cm), 3),
                "color_label": color_label,
                "color_confidence": round(color_confidence, 3),
                "servo_angle_deg": servo_angle,
                "object_slot": 1 if step >= 150 else 0,
                "telemetry_ok": True,
                "event": event,
                "data_note": "synthetic_demo",
            }
        )
    return pd.DataFrame(rows)


def write_sample_logs(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    configs = [
        DemoRunConfig("demo_red_object", seed=7, object_color="red"),
        DemoRunConfig("demo_blue_object", seed=13, object_color="blue"),
    ]
    paths: list[Path] = []
    for config in configs:
        path = output_dir / f"{config.run_id}.csv"
        simulate_run(config).to_csv(path, index=False)
        paths.append(path)
    return paths

