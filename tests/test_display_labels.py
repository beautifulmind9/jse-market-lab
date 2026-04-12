import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.ui.display_labels import clean_dataframe_labels, display_label, display_value


def test_display_label_cleans_common_snake_case_tokens():
    assert display_label("quality_tier") == "Quality Tier"
    assert display_label("holding_window") == "Holding Window"
    assert display_label("win_rate") == "Win Rate"


def test_display_value_cleans_snake_case_status_values():
    assert display_value("target_hit") == "Target Hit"
    assert display_value("time_exit") == "Time Exit"


def test_clean_dataframe_labels_renames_headers_and_selected_value_columns():
    raw = pd.DataFrame(
        {
            "quality_tier": ["A"],
            "exit_reason": ["target_hit"],
            "win_rate": [0.6],
        }
    )

    cleaned = clean_dataframe_labels(raw, value_columns=["exit_reason"])

    assert list(cleaned.columns) == ["Quality Tier", "Exit Reason", "Win Rate"]
    assert cleaned.loc[0, "Exit Reason"] == "Target Hit"
