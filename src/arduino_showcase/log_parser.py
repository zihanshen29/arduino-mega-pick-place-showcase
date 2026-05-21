from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "run_id",
    "step",
    "timestamp_s",
    "state",
    "line_error",
    "pid_correction",
    "left_pwm",
    "right_pwm",
    "ultrasonic_cm",
    "color_label",
    "color_confidence",
    "servo_angle_deg",
    "telemetry_ok",
    "data_note",
}


def read_log(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = sorted(REQUIRED_COLUMNS.difference(frame.columns))
    if missing:
        raise ValueError(f"{path} is missing required columns: {missing}")
    if set(frame["data_note"]) != {"synthetic_demo"}:
        raise ValueError(f"{path} must be labeled as synthetic_demo data")
    return frame


def read_logs(paths: list[Path]) -> pd.DataFrame:
    if not paths:
        raise ValueError("No log files provided")
    return pd.concat([read_log(path) for path in paths], ignore_index=True)

