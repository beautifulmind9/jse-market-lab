import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.language.formatter import contains_advisory_language
from app.planner.portfolio_ui import (
    _compact_execution_summary,
    _extract_holding_days,
    _first_sentence,
    _format_holding_window_label,
    _group_mistakes_for_display,
    render_portfolio_plan,
)


class DummyStreamlit:
    def __init__(self):
        self.dataframes = []
        self.info_messages = []
        self.captions = []
        self.writes = []
        self.markdowns = []
        self.tabs_requested = []

    class _DummyTab:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def subheader(self, _text):
        return None

    def caption(self, text):
        self.captions.append(text)

    def markdown(self, _text, **_kwargs):
        self.markdowns.append(_text)
        return None

    def info(self, text):
        self.info_messages.append(text)

    def dataframe(self, df, use_container_width=False):
        self.dataframes.append((df.copy(), use_container_width))

    def write(self, payload):
        self.writes.append(payload)

    def tabs(self, names):
        self.tabs_requested.append(list(names))
        return [self._DummyTab(), self._DummyTab()]


def test_render_portfolio_plan_uses_cleaned_plan_labels_in_beginner_mode():
    st = DummyStreamlit()
    render_portfolio_plan(
        allocations=[
            {
                "instrument": "AAA",
                "allocation_amount": 1000,
                "allocation_pct": 0.1,
                "quality_tier": "A",
                "confidence_label": "strong",
                "selection_rank": 1,
            },
            {
                "instrument": "BBB",
                "allocation_amount": 0,
                "quality_tier": "A",
                "selection_rank": 4,
                "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
            },
        ],
        total_capital=10_000,
        st_module=st,
    )

    funded_df = st.dataframes[1][0]
    unfunded_df = st.dataframes[2][0]

    assert "Ticker" in funded_df.columns
    assert "Setup Strength" in funded_df.columns
    assert "Confidence / Reliability" in funded_df.columns
    assert "Holding Window" in funded_df.columns
    assert "Why this trade" in funded_df.columns
    assert "Execution Summary" in funded_df.columns
    assert "Why this trade" in unfunded_df.columns
    assert "Execution Summary" in unfunded_df.columns
    assert "Instrument" not in funded_df.columns
    assert "Confidence" not in funded_df.columns
    assert "Execution Framework" not in funded_df.columns
    assert "Setup Strength" in funded_df.columns
    assert "Strong setup" in funded_df.iloc[0]["Setup Strength"]
    assert "High confidence" in funded_df.iloc[0]["Confidence / Reliability"]
    assert funded_df.iloc[0]["Holding Window"] == "Not specified"
    assert "Primary Rule/Constraint" not in funded_df.columns
    assert "Primary Rule/Constraint" not in unfunded_df.columns
    assert "Selected because" in funded_df.iloc[0]["Why this trade"]
    assert "planned exit" in funded_df.iloc[0]["Execution Summary"]
    assert "trading days" not in funded_df.iloc[0]["Execution Summary"]
    assert funded_df.iloc[0]["Decision Status"] == "Selected"
    assert unfunded_df.iloc[0]["Decision Status"] == "Not funded (limit reached)"
    assert "funds the strongest eligible setups first" in st.captions[0]
    assert st.tabs_requested == [["Plan", "Review"]]
    assert any("followed system rules" in line for line in st.markdowns)


def test_render_portfolio_plan_beginner_vs_analyst_columns():
    beginner_st = DummyStreamlit()
    analyst_st = DummyStreamlit()
    allocations = [
        {
            "instrument": "AAA",
            "allocation_amount": 1000,
            "allocation_pct": 0.1,
            "quality_tier": "A",
            "confidence_label": "strong",
            "selection_rank": 1,
            "holding_window": 10,
        }
    ]

    render_portfolio_plan(
        allocations=allocations,
        total_capital=10_000,
        st_module=beginner_st,
        section="plan",
        mode="beginner",
    )
    render_portfolio_plan(
        allocations=allocations,
        total_capital=10_000,
        st_module=analyst_st,
        section="plan",
        mode="analyst",
    )

    beginner_df = beginner_st.dataframes[1][0]
    analyst_df = analyst_st.dataframes[1][0]

    assert "Selection Rank" not in beginner_df.columns
    assert "Allocation %" not in beginner_df.columns
    assert "Rule Note" not in beginner_df.columns

    assert "Selection Rank" in analyst_df.columns
    assert "Allocation %" in analyst_df.columns
    assert "Rule Note" in analyst_df.columns
    assert analyst_df.iloc[0]["Holding Window"] == "10 trading days"


def test_render_portfolio_plan_keeps_explanations_before_supporting_fields():
    st = DummyStreamlit()
    render_portfolio_plan(
        allocations=[
            {
                "instrument": "AAA",
                "allocation_amount": 2000,
                "allocation_pct": 0.2,
                "quality_tier": "A",
                "confidence_label": "strong",
                "selection_rank": 1,
                "holding_window": 5,
            }
        ],
        total_capital=10_000,
        st_module=st,
        section="plan",
        mode="analyst",
    )

    funded_df = st.dataframes[1][0]
    ordered_columns = list(funded_df.columns)

    assert ordered_columns.index("Why this trade") < ordered_columns.index("Allocation %")
    assert ordered_columns.index("Execution Summary") < ordered_columns.index("Selection Rank")


def test_group_mistakes_for_display_combines_repeated_types():
    grouped = _group_mistakes_for_display(
        [
            {"type": "low_quality_trade", "message": "a"},
            {"type": "low_quality_trade", "message": "b"},
            {"type": "low_quality_trade", "message": "c"},
            {"type": "liquidity_violation", "message": "d"},
        ]
    )

    assert "3 trade(s) missed the setup-quality rule." in grouped
    assert "1 trade(s) failed the liquidity check." in grouped


def test_render_portfolio_plan_places_snapshot_and_reserved_cash_before_tables():
    st = DummyStreamlit()
    render_portfolio_plan(
        allocations=[
            {
                "instrument": "AAA",
                "allocation_amount": 2000,
                "allocation_pct": 0.2,
                "quality_tier": "A",
                "confidence_label": "strong",
                "selection_rank": 1,
            },
            {
                "instrument": "BBB",
                "allocation_amount": 0,
                "allocation_pct": 0.0,
                "quality_tier": "B",
                "confidence_label": "medium",
                "selection_rank": 4,
                "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
            },
        ],
        total_capital=10_000,
        st_module=st,
        section="plan",
    )

    assert "#### Portfolio Snapshot" in st.markdowns
    assert "#### Why cash is reserved" in st.markdowns
    snapshot_idx = st.markdowns.index("#### Portfolio Snapshot")
    summary_idx = next(
        idx
        for idx, text in enumerate(st.markdowns)
        if "Portfolio Summary" in text
    )
    assert snapshot_idx < summary_idx


def test_render_portfolio_plan_reframes_rules_and_analyst_override_copy():
    st = DummyStreamlit()
    render_portfolio_plan(
        allocations=[
            {
                "instrument": "AAA",
                "allocation_amount": 2000,
                "allocation_pct": 0.2,
                "quality_tier": "A",
                "confidence_label": "strong",
                "selection_rank": 1,
            }
        ],
        total_capital=10_000,
        st_module=st,
        section="plan",
        mode="analyst",
        analyst_max_funded_trades_override=4,
    )

    combined = " ".join(st.markdowns)
    assert "Max funded trades: 3" not in combined
    assert "Funding approach: prioritize top-ranked, stronger setups" in combined
    assert "Analyst cap override: up to 4 funded trades" in combined
    assert "may include lower-ranked setups and reduce reserve discipline" in combined


def test_render_review_tab_uses_human_readable_decision_audit_table():
    st = DummyStreamlit()
    render_portfolio_plan(
        allocations=[
            {
                "instrument": "AAA",
                "allocation_amount": 1000,
                "quality_tier": "A",
                "liquidity_pass": True,
                "selection_rank": 1,
            },
            {
                "instrument": "BBB",
                "allocation_amount": 0,
                "quality_tier": "C",
                "liquidity_pass": True,
                "selection_rank": 3,
            },
            {
                "instrument": "CCC",
                "allocation_amount": 0,
                "quality_tier": "B",
                "liquidity_pass": False,
                "selection_rank": 4,
            },
        ],
        total_capital=10_000,
        st_module=st,
        section="review",
    )

    review_table = st.dataframes[0][0]
    assert set(review_table.columns) == {"Ticker", "Status", "What happened", "Why it matters"}
    assert "instrument" not in review_table.columns
    assert "followed_rules" not in review_table.columns
    assert "quality_flag" not in review_table.columns
    assert "Blocked by quality rule" in set(review_table["Status"])
    assert "Blocked by liquidity check" in set(review_table["Status"])


def test_first_sentence_keeps_decimal_number_intact():
    text = (
        "Entry reference: place a limit at 10.50 with staged risk controls. "
        "Exit after two sessions if momentum fades."
    )

    assert _first_sentence(text) == "Entry reference: place a limit at 10.50 with staged risk controls."


def test_first_sentence_keeps_percentage_intact():
    text = (
        "Protective stop sits at 1.00% below entry to cap downside. "
        "Trim size if spread widens."
    )

    assert _first_sentence(text) == "Protective stop sits at 1.00% below entry to cap downside."


def test_compact_execution_summary_includes_entry_and_exit_timing_for_beginner():
    compact = _compact_execution_summary(
        {
            "entry_reference": "Use the signal-day close area as a reference, not an exact guaranteed fill.",
            "planned_exit": "Default exit is after about 10 trading days, unless conditions are reviewed earlier.",
        },
        mode="beginner",
    )

    assert "signal-day close" in compact
    assert "planned exit after 10 trading days" in compact


def test_compact_execution_summary_includes_entry_and_exit_timing_for_analyst():
    compact = _compact_execution_summary(
        {
            "entry_reference": "Use the signal-day close area (around 12.34) as a reference, not an exact guaranteed fill.",
            "planned_exit": "Default exit is after about 20 trading days, unless conditions are reviewed earlier.",
        },
        mode="analyst",
    )

    assert "signal-day close" in compact
    assert "after 20 trading days" in compact




def test_compact_execution_summary_has_no_advisory_language_in_both_modes():
    beginner = _compact_execution_summary(
        {
            "entry_reference": "Use the signal-day close area as a reference, not an exact guaranteed fill.",
            "planned_exit": "Default exit is after about 5 trading days, unless conditions are reviewed earlier.",
        },
        mode="beginner",
    )
    analyst = _compact_execution_summary(
        {
            "entry_reference": "Use the signal-day close area as a reference, not an exact guaranteed fill.",
            "planned_exit": "Default exit is after about 30 trading days, unless conditions are reviewed earlier.",
        },
        mode="analyst",
    )

    assert contains_advisory_language(beginner) is False
    assert contains_advisory_language(analyst) is False


def test_compact_execution_summary_uses_not_specified_exit_fallback():
    compact = _compact_execution_summary(
        {
            "entry_reference": "Use the signal-day close area as a reference, not an exact guaranteed fill.",
            "planned_exit": "Use the default time-based exit window and review conditions before closing.",
        }
    )

    assert "planned exit timing is not specified" in compact


def test_first_sentence_splits_when_next_sentence_starts_lowercase():
    text = (
        "Entry reference is around 10.50. if momentum fades, fills may vary."
    )

    assert _first_sentence(text) == "Entry reference is around 10.50."


def test_first_sentence_splits_when_next_sentence_starts_with_digit():
    text = (
        "Risk capped at 1%. 2nd entry waits for confirmation."
    )

    assert _first_sentence(text) == "Risk capped at 1%."


def test_first_sentence_splits_when_next_sentence_starts_with_quote():
    text = (
        'Execution uses signal-day close. "Second leg" entries are not guaranteed.'
    )

    assert _first_sentence(text) == "Execution uses signal-day close."


def test_first_sentence_keeps_e_g_abbreviation_in_first_sentence():
    text = (
        "Use limit orders, e.g. near VWAP for cleaner fills. "
        "Avoid chasing late prints."
    )

    assert _first_sentence(text) == "Use limit orders, e.g. near VWAP for cleaner fills."


def test_first_sentence_keeps_i_e_abbreviation_in_first_sentence():
    text = (
        "Scale risk, i.e. reduce size when spreads widen. "
        "Wait for liquidity to improve."
    )

    assert _first_sentence(text) == "Scale risk, i.e. reduce size when spreads widen."


def test_first_sentence_keeps_title_abbreviation_in_first_sentence():
    text = (
        "Follow Dr. Lane's execution note before entry. "
        "Then stage the order across two clips."
    )

    assert _first_sentence(text) == "Follow Dr. Lane's execution note before entry."


def test_first_sentence_keeps_initialism_abbreviation_in_first_sentence():
    text = (
        "Focus on U.S. large-cap names when liquidity thins. "
        "Delay small-cap entries until spread normalizes."
    )

    assert _first_sentence(text) == "Focus on U.S. large-cap names when liquidity thins."


def test_extract_holding_days_accepts_positive_values_only():
    assert _extract_holding_days(10) == 10
    assert _extract_holding_days("10 trading days") == 10
    assert _extract_holding_days("0 trading days") is None
    assert _extract_holding_days("-5 trading days") is None
    assert _extract_holding_days("window: 5? maybe") is None


def test_format_holding_window_label_falls_back_for_invalid_or_non_positive_values():
    assert _format_holding_window_label(10) == "~10 trading days"
    assert _format_holding_window_label("0 trading days") == "Not specified"
    assert _format_holding_window_label("-5 trading days") == "Not specified"
    assert _format_holding_window_label("invalid window") == "Not specified"
