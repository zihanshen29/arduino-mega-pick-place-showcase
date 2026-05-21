from __future__ import annotations

from pathlib import Path

import pandas as pd


def summarize_runs(frame: pd.DataFrame) -> pd.DataFrame:
    summaries: list[dict[str, object]] = []
    for run_id, run in frame.groupby("run_id", sort=True):
        complete_rows = run[run["state"] == "COMPLETE"]
        completion_step = int(complete_rows["step"].iloc[0]) if not complete_rows.empty else None
        summaries.append(
            {
                "run_id": run_id,
                "data_note": "synthetic_demo_metrics",
                "steps": int(run["step"].max() + 1),
                "completion_step": completion_step,
                "mean_abs_line_error": round(float(run["line_error"].abs().mean()), 4),
                "max_abs_pid_correction": round(float(run["pid_correction"].abs().max()), 3),
                "mean_ultrasonic_cm": round(float(run["ultrasonic_cm"].mean()), 3),
                "color_confidence_mean": round(float(run["color_confidence"].mean()), 3),
                "telemetry_ok_rate": round(float(run["telemetry_ok"].mean()), 3),
                "state_count": int(run["state"].nunique()),
            }
        )
    return pd.DataFrame(summaries)


def state_distribution(frame: pd.DataFrame) -> pd.DataFrame:
    counts = frame.groupby(["run_id", "state"]).size().rename("step_count").reset_index()
    totals = counts.groupby("run_id")["step_count"].transform("sum")
    counts["share"] = (counts["step_count"] / totals).round(4)
    counts["data_note"] = "synthetic_demo_metrics"
    return counts


def write_metrics(frame: pd.DataFrame, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "run_summary.csv"
    state_path = output_dir / "state_distribution.csv"
    summarize_runs(frame).to_csv(summary_path, index=False)
    state_distribution(frame).to_csv(state_path, index=False)
    return [summary_path, state_path]

