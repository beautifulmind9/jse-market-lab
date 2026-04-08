import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.decision_review import (
    build_behavior_summary,
    compute_discipline_score,
    compute_trade_review,
    detect_decision_mistakes,
)


def _signals_df():
    return pd.DataFrame(
        [
            {"instrument": "AAA", "rank": 1, "score_total": 0.95},
            {"instrument": "BBB", "rank": 2, "score_total": 0.90},
            {"instrument": "CCC", "rank": 3, "score_total": 0.85},
        ]
    )


def test_compute_trade_review_returns_expected_columns_and_flags():
    trades_df = pd.DataFrame(
        [
            {
                "instrument": "AAA",
                "selection_rank": 2,
                "quality_tier": "A",
                "liquidity_pass": True,
            },
            {
                "instrument": "CCC",
                "selection_rank": 3,
                "quality_tier": "C",
                "liquidity_pass": False,
            },
        ]
    )

    review_df = compute_trade_review(trades_df, _signals_df())

    assert set(review_df.columns) == {
        "instrument",
        "followed_rules",
        "deviation_type",
        "selected_rank",
        "best_available_rank",
        "quality_flag",
        "liquidity_flag",
    }
    assert review_df.iloc[0]["deviation_type"] == "rank_deviation"
    assert review_df.iloc[1]["quality_flag"] == "fail"
    assert review_df.iloc[1]["liquidity_flag"] == "fail"


def test_detect_decision_mistakes_catches_each_mistake_type():
    trades_df = pd.DataFrame(
        [
            {
                "instrument": "AAA",
                "selection_rank": 2,
                "quality_tier": "A",
                "liquidity_pass": True,
                "cooldown_active": False,
            },
            {
                "instrument": "BBB",
                "selection_rank": 2,
                "quality_tier": "C",
                "liquidity_pass": False,
                "cooldown_active": False,
            },
            {
                "instrument": "CCC",
                "selection_rank": 3,
                "quality_tier": "A",
                "liquidity_pass": True,
                "cooldown_active": True,
            },
        ]
    )
    allocation_df = pd.DataFrame(
        [
            {"instrument": "AAA", "allocation_pct": 0.10},
            {"instrument": "BBB", "allocation_pct": 0.80},
            {"instrument": "CCC", "allocation_pct": 0.20},
        ]
    )

    mistakes = detect_decision_mistakes(trades_df, _signals_df(), allocation_df)
    mistake_types = {item["type"] for item in mistakes}

    assert "ignored_higher_rank" in mistake_types
    assert "low_quality_trade" in mistake_types
    assert "liquidity_violation" in mistake_types
    assert "over_allocation" in mistake_types
    assert "cooldown_violation" in mistake_types


def test_build_behavior_summary_generates_observational_bullets():
    trades_df = pd.DataFrame(
        [
            {"instrument": "AAA"},
            {"instrument": "BBB"},
            {"instrument": "CCC"},
        ]
    )
    review_df = pd.DataFrame(
        [
            {
                "instrument": "AAA",
                "followed_rules": True,
                "deviation_type": None,
                "quality_flag": "pass",
                "liquidity_flag": "pass",
            },
            {
                "instrument": "BBB",
                "followed_rules": False,
                "deviation_type": "rank_deviation",
                "quality_flag": "pass",
                "liquidity_flag": "pass",
            },
            {
                "instrument": "CCC",
                "followed_rules": False,
                "deviation_type": "quality_deviation",
                "quality_flag": "fail",
                "liquidity_flag": "fail",
            },
        ]
    )

    summary = build_behavior_summary(trades_df, review_df)

    assert 2 <= len(summary) <= 4
    assert all(isinstance(item, str) for item in summary)
    assert "followed the selection rules" in summary[0]


def test_compute_discipline_score_uses_adherence_components():
    review_df = pd.DataFrame(
        [
            {
                "followed_rules": True,
                "selected_rank": 1,
                "best_available_rank": 1,
                "quality_flag": "pass",
            },
            {
                "followed_rules": False,
                "selected_rank": 3,
                "best_available_rank": 2,
                "quality_flag": "pass",
            },
            {
                "followed_rules": False,
                "selected_rank": 4,
                "best_available_rank": 2,
                "quality_flag": "fail",
            },
            {
                "followed_rules": True,
                "selected_rank": 2,
                "best_available_rank": 2,
                "quality_flag": "pass",
            },
        ]
    )

    score = compute_discipline_score(review_df)

    assert score == 56.2


def test_empty_inputs_are_safe():
    empty_df = pd.DataFrame()

    review_df = compute_trade_review(empty_df, empty_df)
    mistakes = detect_decision_mistakes(empty_df, empty_df, empty_df)
    summary = build_behavior_summary(empty_df, empty_df)
    score = compute_discipline_score(empty_df)

    assert review_df.empty
    assert mistakes == []
    assert len(summary) >= 2
    assert score == 0.0


def test_detect_decision_mistakes_handles_missing_allocation_pct_column():
    trades_df = pd.DataFrame(
        [
            {
                "instrument": "AAA",
                "selection_rank": 1,
                "quality_tier": "A",
                "liquidity_pass": True,
                "cooldown_active": False,
            }
        ]
    )
    allocation_df = pd.DataFrame([{"instrument": "AAA"}])

    mistakes = detect_decision_mistakes(trades_df, _signals_df(), allocation_df)

    assert isinstance(mistakes, list)
    assert all(item["type"] != "over_allocation" for item in mistakes)


def test_detect_decision_mistakes_keeps_cooldown_check_when_trades_are_allocation_context():
    trades_df = pd.DataFrame(
        [
            {
                "instrument": "AAA",
                "selection_rank": 1,
                "quality_tier": "A",
                "liquidity_pass": True,
                "cooldown_active": True,
                "allocation_pct": 0.25,
            }
        ]
    )

    mistakes = detect_decision_mistakes(trades_df, _signals_df(), trades_df)
    mistake_types = {item["type"] for item in mistakes}

    assert "cooldown_violation" in mistake_types
