from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arduino_showcase.fsm_simulator import write_sample_logs
from arduino_showcase.log_parser import read_logs
from arduino_showcase.metrics import write_metrics


def main() -> None:
    log_paths = write_sample_logs(ROOT / "data" / "sample_logs")
    frame = read_logs(log_paths)
    metric_paths = write_metrics(frame, ROOT / "outputs" / "metrics")
    print("Arduino Mega synthetic demo pipeline completed.")
    print(f"logs: {len(log_paths)} files")
    for path in metric_paths:
        print(f"metric: {path}")


if __name__ == "__main__":
    main()
