import pytest

from openjev.smoke import request_headers


@pytest.fixture(autouse=True)
def clear_smoke_auth(monkeypatch):
    monkeypatch.delenv("MODAL_PROXY_TOKEN", raising=False)
    monkeypatch.delenv("MODAL_PROXY_TOKEN_ID", raising=False)
    monkeypatch.delenv("MODAL_PROXY_TOKEN_SECRET", raising=False)
    monkeypatch.delenv("OPENJEV_API_KEY", raising=False)


def test_smoke_headers_default():
    assert request_headers() == {"Modal-Session-ID": "openjev-smoke"}


def test_smoke_headers_support_modal_proxy_pair(monkeypatch):
    monkeypatch.setenv("MODAL_PROXY_TOKEN_ID", "wk-test")
    monkeypatch.setenv("MODAL_PROXY_TOKEN_SECRET", "ws-test")
    monkeypatch.setenv("OPENJEV_API_KEY", "openjev-test")

    assert request_headers() == {
        "Modal-Session-ID": "openjev-smoke",
        "Modal-Key": "wk-test",
        "Modal-Secret": "ws-test",
        "Authorization": "Bearer openjev-test",
    }


def test_smoke_headers_support_combined_modal_token(monkeypatch):
    monkeypatch.setenv("MODAL_PROXY_TOKEN", "wk-test.ws-test")

    assert request_headers()["Authorization"] == "Bearer wk-test.ws-test"


def test_combined_modal_token_conflicts_with_openjev_key(monkeypatch):
    monkeypatch.setenv("MODAL_PROXY_TOKEN", "wk-test.ws-test")
    monkeypatch.setenv("OPENJEV_API_KEY", "openjev-test")

    with pytest.raises(ValueError, match="MODAL_PROXY_TOKEN_ID"):
        request_headers()
