import importlib.util
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.demo import run_demo as run_demo_module


class DummyColumn:
    def __enter__(self):
        return self

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


class DummyStreamlit:
    def __init__(self, *, mode_choice="Analyst"):
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

    def set_page_config(self, **_kwargs):
        return None

    def title(self, _text):
        return None

    def radio(self, _label, options, **_kwargs):
        if self.mode_choice in options:
            return self.mode_choice
        return options[0]

    def markdown(self, text, **_kwargs):
        self.markdowns.append((self.current_tab, text))

    def caption(self, text):
        self.captions.append((self.current_tab, text))

    def info(self, text):
        self.info_messages.append((self.current_tab, text))

    def write(self, _payload):
        return None

    def number_input(self, label, value=0.0, key=None, **_kwargs):
        self.number_inputs.append((self.current_tab, label, key))
        if key is not None:
            self.session_state[key] = value
        return value

    def tabs(self, names):
        self.tabs_requested.append(list(names))
        return [DummyTab(self, name) for name in names]

    def dataframe(self, df, **_kwargs):
        self.dataframes.append((self.current_tab, df.copy()))

    def selectbox(self, _label, options):
        self.selectbox_calls.append(list(options))
        return options[0]

    def columns(self, count):
        return [DummyColumn() for _ in range(count)]

    def subheader(self, _text):
        return None

    def code(self, _text, **_kwargs):
        return None


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
    monkeypatch.setattr(app_main, "generate_embedded_insights", lambda *_args, **_kwargs: {"headline": "ok"})
    monkeypatch.setattr(app_main, "render_embedded_insights", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(app_main, "render_portfolio_plan", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(app_main, "render_analyst_insights", lambda *_args, **_kwargs: None)

    app_main.main()

    assert dummy_st.tabs_requested[0] == ["Portfolio", "Review", "Ticker Analysis", "Analyst Insights", "Data"]
    assert dummy_st.number_inputs == [("Portfolio", "Total capital", "total_capital")]


def test_beginner_mode_hides_analyst_and_data_tabs(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Beginner")

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
    monkeypatch.setattr(app_main, "generate_embedded_insights", lambda *_args, **_kwargs: {"headline": "ok"})
    monkeypatch.setattr(app_main, "render_embedded_insights", lambda *_args, **_kwargs: None)

    app_main.main()

    assert dummy_st.tabs_requested[0] == ["Portfolio", "Review", "Ticker Analysis"]
    assert not any(tab == "Data" for tab, _ in dummy_st.dataframes)
    assert not any(tab == "Analyst Insights" for tab, _ in dummy_st.info_messages)


def test_analyst_mode_keeps_all_tabs_visible(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Analyst")

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
    monkeypatch.setattr(app_main, "generate_embedded_insights", lambda *_args, **_kwargs: {"headline": "ok"})
    monkeypatch.setattr(app_main, "render_embedded_insights", lambda *_args, **_kwargs: None)

    app_main.main()

    assert dummy_st.tabs_requested[0] == ["Portfolio", "Review", "Ticker Analysis", "Analyst Insights", "Data"]


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
    monkeypatch.setattr(app_main, "generate_embedded_insights", lambda *_args, **_kwargs: {"headline": "ok"})
    monkeypatch.setattr(app_main, "render_embedded_insights", lambda *_args, **_kwargs: None)

    app_main.main()

    review_markdowns = [text for tab, text in dummy_st.markdowns if tab == "Review"]
    assert "#### Data Status" not in review_markdowns
    assert "#### Main Dashboard" not in review_markdowns

    data_markdowns = [text for tab, text in dummy_st.markdowns if tab == "Data"]
    assert "#### Data Status" in data_markdowns
    assert "#### Main Dashboard" in data_markdowns
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
    monkeypatch.setattr(app_main, "generate_embedded_insights", lambda *_args, **_kwargs: {"headline": "ok"})
    monkeypatch.setattr(app_main, "render_embedded_insights", lambda *_args, **_kwargs: None)

    app_main.main()

    insight_messages = [text for tab, text in dummy_st.info_messages if tab == "Analyst Insights"]
    assert "Analyst insights are not available for this dataset yet." in insight_messages


def test_ticker_analysis_options_come_from_canonical_dataset_not_ranked_subset(monkeypatch):
    app_main = _load_app_module()
    dummy_st = DummyStreamlit(mode_choice="Analyst")

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
    monkeypatch.setattr(app_main, "generate_embedded_insights", lambda *_args, **_kwargs: {"headline": "ok"})
    monkeypatch.setattr(app_main, "render_embedded_insights", lambda *_args, **_kwargs: None)

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

    assert "**Errors:** 0" in markdowns
    assert "**Warnings:** 1" in markdowns
    assert "**Warning details**" in markdowns
    assert "- Missing volume for BBB" in markdowns
    assert "**Error details**" not in markdowns
    assert "No ingestion errors were reported for this dataset." in captions


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

    assert "**Errors:** 1" in markdowns
    assert "**Warnings:** 0" in markdowns
    assert "**Error details**" in markdowns
    assert "- Missing required column: close" in markdowns
    assert "**Warning details**" not in markdowns
    assert "No ingestion warnings were reported for this dataset." in captions


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

    assert "**Errors:** 1" in markdowns
    assert "**Warnings:** 1" in markdowns
    assert "**Warning details**" in markdowns
    assert "- Ticker normalized: BRG -> BRG.JM" in markdowns
    assert "**Error details**" in markdowns
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
    monkeypatch.setattr(app_main, "generate_embedded_insights", lambda *_args, **_kwargs: {"headline": "ok"})
    monkeypatch.setattr(app_main, "render_embedded_insights", lambda *_args, **_kwargs: None)
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
    dummy_st = DummyStreamlit(mode_choice="Beginner")
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
