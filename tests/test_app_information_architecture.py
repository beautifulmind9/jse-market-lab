import importlib.util
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.demo import run_demo as run_demo_module


class DummyColumn:
    def __init__(self, st_module):
        self._st = st_module

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def metric(self, label, value, *_args, **_kwargs):
        self._st.metrics.append((self._st.current_tab, label, value))

    def markdown(self, *_args, **_kwargs):
        return None

    def info(self, *_args, **_kwargs):
        return None


class DummyExpander:
    def __init__(self, st_module):
        self._st = st_module

    def __enter__(self):
        return self._st

    def __exit__(self, exc_type, exc, tb):
        return False


class DummyTab:
    def __init__(self, st_module, name):
        self._st = st_module
        self._name = name

    def __enter__(self):
        self._st.current_tab = self._name
        return self

    def __exit__(self, exc_type, exc, tb):
        self._st.current_tab = None
        return False


class DummyComponentsV1:
    def __init__(self, st_module):
        self._st = st_module

    def html(self, html, **kwargs):
        self._st.html_blocks.append((self._st.current_tab, html, kwargs))


class DummyComponents:
    def __init__(self, st_module):
        self.v1 = DummyComponentsV1(st_module)


class DummyStreamlit:
    def __init__(self, *, mode_choice="Advanced View"):
        self.session_state = {}
        self.current_tab = None
        self.mode_choice = mode_choice
        self.tabs_requested = []
        self.number_inputs = []
        self.markdowns = []
        self.info_messages = []
        self.dataframes = []
        self.captions = []
        self.selectbox_calls = []
        self.html_blocks = []
        self.components = DummyComponents(self)
        self.metrics = []
        self.expanders = []
        self.rerun_called = False
        self.selectbox_choice = None

    def set_page_config(self, **_kwargs):
        return None

    def title(self, _text):
        return None

    def radio(self, _label, options, **_kwargs):
        if self.mode_choice in options:
            return self.mode_choice
        return options[0]

    def cache_data(self, **_kwargs):
        def decorator(func):
            return func

        return decorator

    def markdown(self, text, **_kwargs):
        self.markdowns.append((self.current_tab, text))

    def caption(self, text):
        self.captions.append((self.current_tab, text))

    def info(self, text):
        self.info_messages.append((self.current_tab, text))

    def warning(self, text):
        self.info_messages.append((self.current_tab, text))

    def write(self, _payload):
        return None

    def metric(self, label, value, *_args, **_kwargs):
        self.metrics.append((self.current_tab, label, value))

    def number_input(self, label, value=0.0, key=None, **_kwargs):
        self.number_inputs.append((self.current_tab, label, key))
        if key is not None:
            self.session_state[key] = value
        return value

    def tabs(self, names, **_kwargs):
        self.tabs_requested.append(list(names))
        return [DummyTab(self, name) for name in names]

    def dataframe(self, df, **_kwargs):
        self.dataframes.append((self.current_tab, df.copy()))

    def selectbox(self, _label, options, index=0):
        self.selectbox_calls.append(list(options))
        if self.selectbox_choice in options:
            return self.selectbox_choice
        return options[index]

    def columns(self, count):
        return [DummyColumn(self) for _ in range(count)]

    def subheader(self, _text):
        return None

    def code(self, _text, **_kwargs):
        return None

    def expander(self, _label, **_kwargs):
        self.expanders.append((self.current_tab, _label))
        return DummyExpander(self)

    def button(self, *_args, **_kwargs):
        return False

    def rerun(self):
        self.rerun_called = True


def _load_app_module():
    spec = importlib.util.spec_from_file_location("app_main", ROOT / "app.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_sprint12_tab_layout_and_capital_location(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit()

    canonical_df = pd.DataFrame(
        {
            "instrument": ["AAA"],
            "date": pd.to_datetime(["2024-01-01"]),
            "close": [10.0],
        }
    )
    ranked_df = pd.DataFrame({"instrument": ["AAA"], "selection_rank": [1], "tier": ["A"]})

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (canonical_df, {"source": "demo", "dataset_id": "demo-v1"}, {"errors": [], "warnings": []}),
    )
    monkeypatch.setattr(app_main, "run_demo", lambda: {"ranked": ranked_df})
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: pd.DataFrame())
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [{"instrument": "AAA"}])
    monkeypatch.setattr(app_main, "generate_portfolio_allocation", lambda _rows, _capital: {"allocations": [{"allocation_amount": 5000, "allocation_pct": 0.05}]})
    monkeypatch.setattr(app_main, "render_portfolio_plan", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(app_main, "render_analyst_insights", lambda *_args, **_kwargs: None)

    app_main.main()

    assert dummy_st.tabs_requested[0] == ["Portfolio", "Review", "Ticker Analysis", "Analyst Insights", "Data"]
    assert dummy_st.number_inputs == [("Portfolio", "Enter your investment amount (JMD)", "total_capital")]
    assert ("Portfolio", "Start here: enter your investment amount above to build your plan.") in dummy_st.info_messages
    assert ("Portfolio", "This is the amount you want to allocate across trades.") in dummy_st.captions
    assert (
        "Portfolio",
        "This plan is built from the market data currently loaded in the dashboard.",
    ) in dummy_st.captions
    assert (
        "Portfolio",
        "Click a stock to see how it typically behaves and when it’s usually reviewed.",
    ) in dummy_st.captions
    assert any(
        tab == "Portfolio" and "Viewed as at" in text and ("Jamaica time" in text or "UTC" in text)
        for tab, text in dummy_st.captions
    )
    assert any(tab == "Portfolio" and "Latest market data in dashboard" in text for tab, text in dummy_st.captions)
    assert any(
        tab == "Portfolio" and "5D, 10D, 20D, and 30D are review windows." in text
        for tab, text in dummy_st.info_messages
    )
    assert any(
        tab == "Portfolio" and "If you enter today" in text
        for tab, text in dummy_st.info_messages
    )
    assert any(
        tab == "Portfolio" and "start counting from your entry date" in text
        for tab, text in dummy_st.info_messages
    )
    assert any(
        tab == "Portfolio" and "review after that many trading days" in text
        for tab, text in dummy_st.info_messages
    )
    assert any(
        tab == "Portfolio" and "not month-end hold rules" in text
        for tab, text in dummy_st.info_messages
    )


def test_guided_view_hides_analyst_insights_tab(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Guided View")

    canonical_df = pd.DataFrame({"instrument": ["AAA"], "date": pd.to_datetime(["2024-01-01"]), "close": [10.0]})

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (canonical_df, {"source": "demo", "dataset_id": "demo-v1"}, {"errors": [], "warnings": []}),
    )
    monkeypatch.setattr(app_main, "run_demo", lambda: {"ranked": pd.DataFrame()})
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: pd.DataFrame())
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [])

    app_main.main()

    assert dummy_st.tabs_requested[0] == ["Portfolio", "Review", "Ticker Analysis", "Data"]
    assert not any(tab == "Analyst Insights" for tab, _ in dummy_st.info_messages)


def test_analyst_mode_keeps_all_tabs_visible(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Advanced View")

    canonical_df = pd.DataFrame({"instrument": ["AAA"], "date": pd.to_datetime(["2024-01-01"]), "close": [10.0]})

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (canonical_df, {"source": "demo", "dataset_id": "demo-v1"}, {"errors": [], "warnings": []}),
    )
    monkeypatch.setattr(app_main, "run_demo", lambda: {"ranked": pd.DataFrame()})
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: pd.DataFrame())
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [])

    app_main.main()

    assert dummy_st.tabs_requested[0] == ["Portfolio", "Review", "Ticker Analysis", "Analyst Insights", "Data"]


def test_ticker_analysis_preloads_selected_ticker_from_portfolio_context(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Guided View")
    dummy_st.session_state["selected_ticker"] = "BBB"
    dummy_st.session_state["ticker_analysis_source"] = "portfolio"
    dummy_st.session_state["ticker_analysis_source_ticker"] = "BBB"
    dummy_st.session_state["active_tab_name"] = "Ticker Analysis"

    canonical_df = pd.DataFrame(
        {
            "instrument": ["AAA", "BBB"],
            "date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "close": [10.0, 12.0],
        }
    )

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (canonical_df, {"source": "demo", "dataset_id": "demo-v1"}, {"errors": [], "warnings": []}),
    )
    monkeypatch.setattr(app_main, "run_demo", lambda: {"ranked": pd.DataFrame()})
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: canonical_df)
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [])
    monkeypatch.setattr(
        app_main,
        "build_ticker_drilldown",
        lambda _analyst_df, _ticker: {
            "holding_window_stats": {"10D": {"win_rate": 0.6, "median_return": 0.03, "avg_return": 0.02, "count": 5}},
            "pattern_summary": "Pattern summary",
            "tier_performance": {},
            "volatility_performance": {},
            "return_distribution": {},
            "signals": [],
        },
    )
    monkeypatch.setattr(
        app_main,
        "compute_ticker_metrics",
        lambda _analyst_df, _ticker, mode="beginner": {
            "stats": {"win_rate": 0.6, "avg_return": 0.02, "median_return": 0.03, "best_window": "10D"},
            "behavior": {
                "holding_window": "Holding window context",
                "reliability": "Reliability",
                "consistency": "Consistency",
                "tier_profile": "Tier profile",
            },
            "execution": {
                "entry_reference": "Entry reference",
                "planned_exit": "Planned exit",
                "typical_outcome": "Typical outcome",
                "execution_risk": "Execution risk",
            },
        },
    )

    app_main.main()

    assert ("Ticker Analysis", "Viewing analysis for BBB from your portfolio plan.") in dummy_st.captions


def test_ticker_analysis_clears_portfolio_context_after_manual_ticker_change(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Guided View")
    dummy_st.session_state["selected_ticker"] = "BBB"
    dummy_st.session_state["ticker_analysis_source"] = "portfolio"
    dummy_st.session_state["ticker_analysis_source_ticker"] = "BBB"
    dummy_st.selectbox_choice = "AAA"

    canonical_df = pd.DataFrame(
        {
            "instrument": ["AAA", "BBB"],
            "date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "close": [10.0, 12.0],
        }
    )

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (canonical_df, {"source": "demo", "dataset_id": "demo-v1"}, {"errors": [], "warnings": []}),
    )
    monkeypatch.setattr(app_main, "run_demo", lambda: {"ranked": pd.DataFrame()})
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: canonical_df)
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [])
    monkeypatch.setattr(
        app_main,
        "build_ticker_drilldown",
        lambda _analyst_df, _ticker: {
            "holding_window_stats": {"10D": {"win_rate": 0.6, "median_return": 0.03, "avg_return": 0.02, "count": 5}},
            "pattern_summary": "Pattern summary",
            "tier_performance": {},
            "volatility_performance": {},
            "return_distribution": {},
            "signals": [],
        },
    )
    monkeypatch.setattr(
        app_main,
        "compute_ticker_metrics",
        lambda _analyst_df, _ticker, mode="beginner": {
            "stats": {"win_rate": 0.6, "avg_return": 0.02, "median_return": 0.03, "best_window": "10D"},
            "behavior": {
                "holding_window": "Holding window context",
                "reliability": "Reliability",
                "consistency": "Consistency",
                "tier_profile": "Tier profile",
            },
            "execution": {
                "entry_reference": "Entry reference",
                "planned_exit": "Planned exit",
                "typical_outcome": "Typical outcome",
                "execution_risk": "Execution risk",
            },
        },
    )

    app_main.main()

    assert ("Ticker Analysis", "Viewing analysis for AAA from your portfolio plan.") not in dummy_st.captions
    assert dummy_st.session_state.get("ticker_analysis_source") is None


def test_ticker_analysis_navigation_injects_tab_focus_script_when_tab_preselected(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Guided View")
    dummy_st.session_state["active_tab_name"] = "Ticker Analysis"

    canonical_df = pd.DataFrame({"instrument": ["AAA"], "date": pd.to_datetime(["2024-01-01"]), "close": [10.0]})

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (canonical_df, {"source": "demo", "dataset_id": "demo-v1"}, {"errors": [], "warnings": []}),
    )
    monkeypatch.setattr(app_main, "run_demo", lambda: {"ranked": pd.DataFrame()})
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: pd.DataFrame())
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [])

    app_main.main()

    focus_scripts = [html for _, html, _ in dummy_st.html_blocks if 'targetLabel = "Ticker Analysis"' in html]
    assert len(focus_scripts) == 1
    assert dummy_st.session_state.get("active_tab_name") is None


def test_help_video_labels_and_links_render_in_expected_sections(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Advanced View")

    canonical_df = pd.DataFrame({"instrument": ["AAA"], "date": pd.to_datetime(["2024-01-01"]), "close": [10.0]})

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (canonical_df, {"source": "demo", "dataset_id": "demo-v1"}, {"errors": [], "warnings": []}),
    )
    monkeypatch.setattr(app_main, "run_demo", lambda: {"ranked": pd.DataFrame()})
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: pd.DataFrame())
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [])

    app_main.main()

    all_markdowns = [text for _, text in dummy_st.markdowns]
    assert "### New here? Start with this video" in all_markdowns
    assert any("▶ Watch: Understanding the Portfolio" in text for tab, text in dummy_st.markdowns if tab == "Portfolio")
    assert any("▶ Watch: How to Read a Trade" in text for tab, text in dummy_st.markdowns if tab == "Portfolio")
    assert any("▶ Watch: Understanding Ticker Analysis" in text for tab, text in dummy_st.markdowns if tab == "Ticker Analysis")
    assert any("▶ Watch: Understanding Review" in text for tab, text in dummy_st.markdowns if tab == "Review")
    assert any("▶ Watch: How to Use Analyst Mode" in text for tab, text in dummy_st.markdowns if tab == "Analyst Insights")
    assert any("loom.com/embed/7429a995143a4bf498b640b5371309bc" in html for _, html, _ in dummy_st.html_blocks)
    assert (None, "Learn how this works") in dummy_st.expanders


def test_analyst_help_video_hidden_from_beginner_mode(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Guided View")

    canonical_df = pd.DataFrame({"instrument": ["AAA"], "date": pd.to_datetime(["2024-01-01"]), "close": [10.0]})

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (canonical_df, {"source": "demo", "dataset_id": "demo-v1"}, {"errors": [], "warnings": []}),
    )
    monkeypatch.setattr(app_main, "run_demo", lambda: {"ranked": pd.DataFrame()})
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: pd.DataFrame())
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [])

    app_main.main()

    assert not any("▶ Watch: How to Use Analyst Mode" in text for _, text in dummy_st.markdowns)

def test_review_excludes_data_status_and_data_tab_contains_raw_preview(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit()

    canonical_df = pd.DataFrame(
        {
            "instrument": ["AAA", "BBB"],
            "date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "close": [10.0, 11.0],
        }
    )

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (
            canonical_df,
            {"source": "demo", "dataset_id": "dataset-42"},
            {"errors": [], "warnings": ["Missing volume for BBB"]},
        ),
    )
    monkeypatch.setattr(app_main, "run_demo", lambda: {"ranked": pd.DataFrame()})
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: pd.DataFrame())
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [])

    app_main.main()

    review_markdowns = [text for tab, text in dummy_st.markdowns if tab == "Review"]
    assert "#### Data Status" not in review_markdowns
    assert "#### Main Dashboard" not in review_markdowns

    data_markdowns = [text for tab, text in dummy_st.markdowns if tab == "Data"]
    assert "#### Data Status" in data_markdowns
    assert any(tab == "Data" and len(df) == 2 for tab, df in dummy_st.dataframes)


def test_analyst_insights_empty_state_when_no_content(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit()

    canonical_df = pd.DataFrame(
        {
            "instrument": ["AAA"],
            "date": pd.to_datetime(["2024-01-01"]),
            "close": [10.0],
        }
    )

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (canonical_df, {"source": "demo", "dataset_id": "demo"}, {"errors": [], "warnings": []}),
    )
    monkeypatch.setattr(app_main, "run_demo", lambda: {"ranked": pd.DataFrame()})
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: pd.DataFrame())
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [])

    app_main.main()

    insight_messages = [text for tab, text in dummy_st.info_messages if tab == "Analyst Insights"]
    assert "Analyst insights are not available for this dataset yet." in insight_messages


def test_ticker_analysis_options_come_from_canonical_dataset_not_ranked_subset(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Advanced View")

    large_ticker_universe = [f"T{i:03d}" for i in range(1, 21)]
    canonical_df = pd.DataFrame(
        {
            "instrument": large_ticker_universe,
            "date": pd.to_datetime(["2024-01-01"] * len(large_ticker_universe)),
            "close": [10.0] * len(large_ticker_universe),
        }
    )
    ranked_subset = pd.DataFrame({"instrument": ["T001", "T002"], "selection_rank": [1, 2], "tier": ["A", "B"]})

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (
            canonical_df,
            {"source": "demo", "dataset_id": "dataset-42"},
            {"errors": [], "warnings": []},
        ),
    )
    monkeypatch.setattr(
        app_main,
        "run_demo",
        lambda **_kwargs: {"ranked": ranked_subset},
    )
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: pd.DataFrame())
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [])

    app_main.main()

    ticker_options = dummy_st.selectbox_calls[0]
    assert len(ticker_options) > 9
    assert set(large_ticker_universe).issubset(set(ticker_options))


def test_data_status_uses_warning_bucket_for_counts_and_details():
    app_main = _load_app_module()
    dummy_st = DummyStreamlit()

    app_main._render_data_status_summary(
        dummy_st,
        source="demo",
        row_count=12,
        issues={"errors": [], "warnings": ["Missing volume for BBB"]},
        dataset_id="dataset-42",
        analyst_mode=False,
    )

    markdowns = [text for _, text in dummy_st.markdowns]
    captions = [text for _, text in dummy_st.captions]

    assert ("Rows loaded", 12) in [(label, value) for _, label, value in dummy_st.metrics]
    assert ("Warnings", 1) in [(label, value) for _, label, value in dummy_st.metrics]
    assert ("Errors", 0) in [(label, value) for _, label, value in dummy_st.metrics]
    assert "- Missing volume for BBB" in markdowns
    assert "Source: demo" in captions


def test_data_status_uses_error_bucket_for_counts_and_details():
    app_main = _load_app_module()
    dummy_st = DummyStreamlit()

    app_main._render_data_status_summary(
        dummy_st,
        source="upload",
        row_count=8,
        issues={"errors": ["Missing required column: close"], "warnings": []},
        dataset_id="dataset-100",
        analyst_mode=False,
    )

    markdowns = [text for _, text in dummy_st.markdowns]
    captions = [text for _, text in dummy_st.captions]

    assert ("Warnings", 0) in [(label, value) for _, label, value in dummy_st.metrics]
    assert ("Errors", 1) in [(label, value) for _, label, value in dummy_st.metrics]
    assert "- Missing required column: close" in markdowns
    assert "Source: upload" in captions


def test_data_status_uses_both_buckets_without_top_level_keys():
    app_main = _load_app_module()
    dummy_st = DummyStreamlit()

    app_main._render_data_status_summary(
        dummy_st,
        source="upload",
        row_count=5,
        issues={
            "errors": ["Price parse failed on row 3"],
            "warnings": ["Ticker normalized: BRG -> BRG.JM"],
        },
        dataset_id="dataset-200",
        analyst_mode=True,
    )

    markdowns = [text for _, text in dummy_st.markdowns]

    assert ("Warnings", 1) in [(label, value) for _, label, value in dummy_st.metrics]
    assert ("Errors", 1) in [(label, value) for _, label, value in dummy_st.metrics]
    assert "- Ticker normalized: BRG -> BRG.JM" in markdowns
    assert "- Price parse failed on row 3" in markdowns
    assert "- errors" not in markdowns
    assert "- warnings" not in markdowns


def test_app_does_not_depend_on_global_cache_data_clear():
    app_source = (ROOT / "app.py").read_text()
    assert "cache_data.clear" not in app_source


def test_run_demo_uses_active_dataset_context_when_supported(monkeypatch):
    app_main = _load_app_module()

    canonical_df = pd.DataFrame({"instrument": ["AAA"], "date": pd.to_datetime(["2024-01-01"]), "close": [10.0]})
    meta = {"dataset_id": "demo-1", "dataset_source_label": "internal_jse_dataset"}
    issues = {"errors": [], "warnings": []}
    calls = {}

    def run_demo_with_context(*, canonical_df, meta, issues):
        calls["canonical_df"] = canonical_df
        calls["meta"] = meta
        calls["issues"] = issues
        return {"ranked": pd.DataFrame()}

    monkeypatch.setattr(app_main, "run_demo", run_demo_with_context)

    result = app_main._run_demo_with_active_dataset(
        canonical_df=canonical_df,
        meta=meta,
        issues=issues,
    )

    assert "ranked" in result
    assert isinstance(result["ranked"], pd.DataFrame)
    assert calls["canonical_df"] is canonical_df
    assert calls["meta"] is meta
    assert calls["issues"] is issues


def test_run_demo_falls_back_to_legacy_signature_when_context_not_supported(monkeypatch):
    app_main = _load_app_module()

    canonical_df = pd.DataFrame({"instrument": ["AAA"], "date": pd.to_datetime(["2024-01-01"]), "close": [10.0]})
    meta = {"dataset_id": "demo-1"}
    issues = {"errors": [], "warnings": []}
    calls = {"count": 0}

    def legacy_run_demo():
        calls["count"] += 1
        return {"ranked": pd.DataFrame()}

    monkeypatch.setattr(app_main, "run_demo", legacy_run_demo)

    result = app_main._run_demo_with_active_dataset(
        canonical_df=canonical_df,
        meta=meta,
        issues=issues,
    )

    assert "ranked" in result
    assert isinstance(result["ranked"], pd.DataFrame)
    assert calls["count"] == 1


def test_ticker_analysis_selector_uses_canonical_dataset_universe(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit()

    canonical_df = pd.DataFrame(
        {
            "instrument": [f"T{i:02d}" for i in range(12)],
            "date": pd.to_datetime(["2024-01-01"] * 12),
            "close": [10.0 + i for i in range(12)],
        }
    )
    analyst_subset = pd.DataFrame(
        {
            "instrument": ["T00", "T01"],
            "entry_date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
            "return_pct": [0.01, -0.01],
            "holding_window": [5, 5],
            "quality_tier": ["A", "B"],
            "volatility_bucket": ["low", "medium"],
        }
    )

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (
            canonical_df,
            {"source": "demo", "dataset_id": "demo-v1", "dataset_source_label": "internal_jse_dataset"},
            {"errors": [], "warnings": []},
        ),
    )
    monkeypatch.setattr(app_main, "run_demo", lambda *_args, **_kwargs: {"ranked": pd.DataFrame()})
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: analyst_subset)
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [])
    monkeypatch.setattr(app_main, "compute_ticker_metrics", lambda *_args, **_kwargs: {"summary": "", "behavior": {}})
    monkeypatch.setattr(
        app_main,
        "build_ticker_drilldown",
        lambda *_args, **_kwargs: {
            "pattern_summary": "",
            "signals": [],
            "holding_window_stats": {},
            "tier_performance": {},
            "volatility_performance": {},
            "return_distribution": {},
        },
    )

    app_main.main()

    assert dummy_st.selectbox_calls
    assert len(dummy_st.selectbox_calls[0]) == 12


def test_main_startup_path_is_not_blocked_by_missing_legacy_events_file(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Guided View")
    events_path = (ROOT / "data" / "demo" / "earnings_events.csv").resolve()
    original_exists = Path.exists
    original_read_csv = pd.read_csv

    def patched_exists(path_obj):
        if path_obj.resolve() == events_path:
            return False
        return original_exists(path_obj)

    def fail_if_events_read(path, *args, **kwargs):
        if Path(path).resolve() == events_path:
            raise AssertionError("app startup attempted to read missing legacy events file")
        return original_read_csv(path, *args, **kwargs)

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(Path, "exists", patched_exists)
    monkeypatch.setattr(run_demo_module.pd, "read_csv", fail_if_events_read)
    monkeypatch.setattr(app_main, "run_demo", lambda **kwargs: run_demo_module.run_demo(**kwargs))

    app_main.main()

    assert dummy_st.tabs_requested


def test_ticker_analysis_beginner_mode_hides_raw_deep_dive_tables(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Guided View")

    canonical_df = pd.DataFrame({"instrument": ["CAR"], "date": pd.to_datetime(["2024-01-01"]), "close": [10.0]})
    analyst_df = pd.DataFrame({"instrument": ["CAR"], "holding_window": [5], "net_return_pct": [0.01]})

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (
            canonical_df,
            {"source": "demo", "dataset_id": "demo-v1", "dataset_source_label": "internal_jse_dataset"},
            {"errors": [], "warnings": []},
        ),
    )
    monkeypatch.setattr(app_main, "run_demo", lambda *_args, **_kwargs: {"ranked": pd.DataFrame()})
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: analyst_df)
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [])
    monkeypatch.setattr(
        app_main,
        "compute_ticker_metrics",
        lambda *_args, **_kwargs: {
            "summary": "",
            "stats": {"win_rate": 0.5, "avg_return": 0.01, "median_return": 0.01, "best_window": "5D"},
            "behavior": {
                "holding_window": "5D looks stronger than 20D in this dataset.",
                "consistency": "Average and median returns are close.",
                "reliability": "Win rate is mixed.",
                "tier_profile": "Setup mix leans to A.",
            },
            "execution": {
                "entry_reference": "Use the signal-day close as the entry reference area.",
                "planned_exit": "Default exit is around 5 trading days.",
                "typical_outcome": "Typical result is centered on median return near 1.00%.",
                "execution_risk": "Spread conditions can affect realized fills.",
                "summary": "Entry reference and exit framing are rule-based.",
            },
        },
    )
    monkeypatch.setattr(
        app_main,
        "build_ticker_drilldown",
        lambda *_args, **_kwargs: {
            "pattern_summary": "This stock has mixed results so far.",
            "signals": [{"holding_window": "5D", "return_pct": 1.0}],
            "holding_window_stats": {"5D": {"count": 12, "win_rate": 0.5, "avg_return": 1.0}},
            "tier_performance": {"A": {"count": 10, "win_rate": 0.6, "avg_return": 1.2}},
            "volatility_performance": {"low": {"count": 10, "win_rate": 0.6, "avg_return": 1.2}},
            "return_distribution": {"negative": 5, "small_positive": 4, "strong_positive": 3},
        },
    )

    app_main.main()

    ticker_markdowns = [text for tab, text in dummy_st.markdowns if tab == "Ticker Analysis"]
    assert "#### Execution Behavior" in ticker_markdowns
    assert "#### G) Analyst Deep Dive" not in ticker_markdowns
    assert any(
        tab == "Ticker Analysis" and "Viewed as at" in text and ("Jamaica time" in text or "UTC" in text)
        for tab, text in dummy_st.captions
    )
    assert any(tab == "Ticker Analysis" and "Latest market data in dashboard" in text for tab, text in dummy_st.captions)
    assert any(
        tab == "Ticker Analysis" and "5D, 10D, 20D, and 30D are review windows." in text
        for tab, text in dummy_st.info_messages
    )
    assert any(
        tab == "Ticker Analysis" and "If you enter today" in text
        for tab, text in dummy_st.info_messages
    )
    assert any(
        tab == "Ticker Analysis" and "start counting from your entry date" in text
        for tab, text in dummy_st.info_messages
    )
    assert any(
        tab == "Ticker Analysis" and "review after that many trading days" in text
        for tab, text in dummy_st.info_messages
    )
    assert any(
        tab == "Ticker Analysis" and "not month-end hold rules" in text
        for tab, text in dummy_st.info_messages
    )
    assert any("Switch to Advanced View to open the full table breakdown." in text for _, text in dummy_st.captions)
    assert not any("Outcome context:" in text for text in ticker_markdowns)


def test_ticker_analysis_analyst_mode_shows_deep_dive_tables(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Advanced View")

    canonical_df = pd.DataFrame({"instrument": ["CAR"], "date": pd.to_datetime(["2024-01-01"]), "close": [10.0]})
    analyst_df = pd.DataFrame({"instrument": ["CAR"], "holding_window": [5], "net_return_pct": [0.01]})

    monkeypatch.setitem(sys.modules, "streamlit", dummy_st)
    monkeypatch.setattr(
        app_main,
        "ingest_dataset",
        lambda _dataset: (
            canonical_df,
            {"source": "demo", "dataset_id": "demo-v1", "dataset_source_label": "internal_jse_dataset"},
            {"errors": [], "warnings": []},
        ),
    )
    monkeypatch.setattr(app_main, "run_demo", lambda *_args, **_kwargs: {"ranked": pd.DataFrame()})
    monkeypatch.setattr(app_main, "build_analyst_dataset", lambda _canonical, _ranked: analyst_df)
    monkeypatch.setattr(app_main, "coerce_trade_rows_from_ranked", lambda _ranked: [])
    monkeypatch.setattr(
        app_main,
        "compute_ticker_metrics",
        lambda *_args, **_kwargs: {
            "summary": "",
            "stats": {"win_rate": 0.5, "avg_return": 0.01, "median_return": 0.01, "best_window": "5D"},
            "behavior": {
                "holding_window": "5D looks stronger than 20D in this dataset.",
                "consistency": "Average and median returns are close.",
                "reliability": "Win rate is mixed.",
                "tier_profile": "Setup mix leans to A.",
            },
            "execution": {
                "entry_reference": "Use the signal-day close as the entry reference area.",
                "planned_exit": "Default exit is around 5 trading days.",
                "typical_outcome": "Typical result is centered on median return near 1.00%.",
                "execution_risk": "Spread conditions can affect realized fills.",
                "summary": "Entry reference and exit framing are rule-based.",
            },
        },
    )
    monkeypatch.setattr(
        app_main,
        "build_ticker_drilldown",
        lambda *_args, **_kwargs: {
            "pattern_summary": "This stock has mixed results so far.",
            "signals": [{"holding_window": "5D", "return_pct": 1.0}],
            "holding_window_stats": {"5D": {"count": 12, "win_rate": 0.5, "avg_return": 1.0}},
            "tier_performance": {"A": {"count": 10, "win_rate": 0.6, "avg_return": 1.2}},
            "volatility_performance": {"low": {"count": 10, "win_rate": 0.6, "avg_return": 1.2}},
            "return_distribution": {"negative": 5, "small_positive": 4, "strong_positive": 3},
        },
    )

    app_main.main()

    ticker_markdowns = [text for tab, text in dummy_st.markdowns if tab == "Ticker Analysis"]
    ticker_dataframes = [df for tab, df in dummy_st.dataframes if tab == "Ticker Analysis"]
    assert "#### Execution Behavior" in ticker_markdowns
    assert "#### G) Analyst Deep Dive" not in ticker_markdowns
    assert any("Outcome context:" in text for text in ticker_markdowns)
    assert len(ticker_dataframes) >= 4
