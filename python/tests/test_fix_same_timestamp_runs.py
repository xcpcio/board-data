import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fix_same_timestamp_runs import fix_collapsed_timestamps, is_collapsed_timestamp_contest


def test_detects_nanchang_style_collapsed_timestamps():
    runs = [
        {"team_id": "a", "problem_id": "0", "timestamp": 10920, "status": "REJECTED"},
        {"team_id": "a", "problem_id": "0", "timestamp": 10920, "status": "REJECTED"},
        {"team_id": "a", "problem_id": "0", "timestamp": 10920, "status": "ACCEPTED"},
        {"team_id": "a", "problem_id": "1", "timestamp": 420, "status": "ACCEPTED"},
        {"team_id": "b", "problem_id": "0", "timestamp": 18000, "status": "REJECTED"},
        {"team_id": "b", "problem_id": "0", "timestamp": 18000, "status": "REJECTED"},
    ]

    assert is_collapsed_timestamp_contest(runs) is True

    changed = fix_collapsed_timestamps(runs)
    assert changed == 4
    assert [run["timestamp"] for run in runs] == [0, 0, 10920, 420, 0, 0]


def test_ignores_normal_contests_with_distinct_timestamps():
    runs = [
        {"team_id": "a", "problem_id": "0", "timestamp": 60, "status": "REJECTED"},
        {"team_id": "a", "problem_id": "0", "timestamp": 120, "status": "ACCEPTED"},
        {"team_id": "b", "problem_id": "0", "timestamp": 180, "status": "REJECTED"},
        {"team_id": "b", "problem_id": "0", "timestamp": 180, "status": "ACCEPTED"},
    ]

    assert is_collapsed_timestamp_contest(runs) is False


def test_keeps_pending_timestamps():
    runs = [
        {"team_id": "a", "problem_id": "0", "timestamp": 100, "status": "REJECTED"},
        {"team_id": "a", "problem_id": "0", "timestamp": 100, "status": "ACCEPTED"},
        {"team_id": "b", "problem_id": "0", "timestamp": 18000, "status": "PENDING"},
    ]

    assert is_collapsed_timestamp_contest(runs) is True
    changed = fix_collapsed_timestamps(runs)
    assert changed == 1
    assert runs[2]["timestamp"] == 18000
