from pathlib import Path

from arduino_showcase.fsm_simulator import DemoRunConfig, simulate_run, write_sample_logs
from arduino_showcase.log_parser import read_logs
from arduino_showcase.metrics import summarize_runs


def test_simulated_run_has_expected_states() -> None:
    frame = simulate_run(DemoRunConfig(steps=120))
    assert frame["state"].iloc[0] == "LEAVE_BAY"
    assert "LINE_FOLLOW_TO_PICK" in set(frame["state"])
    assert set(frame["data_note"]) == {"synthetic_demo"}


def test_parser_and_metrics(tmp_path: Path) -> None:
    paths = write_sample_logs(tmp_path)
    frame = read_logs(paths)
    summary = summarize_runs(frame)
    assert len(summary) == 2
    assert (summary["telemetry_ok_rate"] == 1.0).all()
    assert summary["mean_abs_line_error"].max() < 0.3

