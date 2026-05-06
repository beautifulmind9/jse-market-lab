from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)

PROHIBITED_LANGUAGE = (
    "buy this stock",
    "sell this stock",
    "guaranteed",
    "will go up",
    "risk-free",
)


def _assert_safe_language(payload: object) -> None:
    text = str(payload).lower()
    for phrase in PROHIBITED_LANGUAGE:
        assert phrase not in text


def test_health_endpoint_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "jse-market-lab-api"


def test_data_status_endpoint_returns_required_fields() -> None:
    response = client.get("/api/data/status")

    assert response.status_code == 200
    payload = response.json()
    assert "dataset_source" in payload
    assert "row_count" in payload
    assert "latest_market_date" in payload
    assert "warnings" in payload
    assert "errors" in payload
    assert "message" in payload


def test_portfolio_plan_endpoint_returns_decision_support_payload() -> None:
    response = client.post("/api/portfolio/plan", json={"capital": 100000, "mode": "guided"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["capital"] == 100000
    assert payload["mode"] == "guided"
    assert "funded_trades" in payload
    assert "unfunded_trades" in payload
    assert "reserve_cash" in payload
    assert "summary" in payload
    assert payload["disclaimer"] == "This is decision support, not financial advice."
    _assert_safe_language(payload)


def test_ticker_analysis_endpoint_returns_decision_support_payload() -> None:
    response = client.get("/api/ticker/JMMBGL/analysis?mode=guided")

    assert response.status_code == 200
    payload = response.json()
    assert payload["ticker"] == "JMMBGL"
    assert payload["mode"] == "guided"
    assert "quick_take" in payload
    assert "best_holding_window" in payload
    assert "holding_windows" in payload
    assert "risk_profile" in payload
    assert "what_to_watch" in payload
    assert "execution_behavior" in payload
    assert payload["disclaimer"] == "This is decision support, not financial advice."
    _assert_safe_language(payload)


def test_review_decision_audit_endpoint_returns_decision_support_payload() -> None:
    response = client.get("/api/review/decision-audit?capital=100000&mode=guided")

    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "guided"
    assert "summary" in payload
    assert "funded_rationale" in payload
    assert "unfunded_rationale" in payload
    assert "rules_applied" in payload
    assert "cash_reserve_explanation" in payload
    assert payload["disclaimer"] == "This is decision support, not financial advice."
    _assert_safe_language(payload)
