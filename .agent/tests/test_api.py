"""API smoke test: start the server on a free port, read the models, run every fast method."""

import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from aerosim.core.server import make_handler
from aerosim.core.state import State


@pytest.fixture(scope="module")
def base():
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(State()))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    server.server_close()


def call(url, body=None):
    data = None if body is None else json.dumps(body).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=60) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def test_models_and_structure(base):
    code, body = call(base + "/api/models")
    data = json.loads(body)
    assert code == 200 and data["ui"]["REMINDER"].startswith("Scope: Honeycomb")
    assert [r["ROW"] for r in data["rows"]][-1] == "Material"
    assert "61.3" in data["totals"]["k_trans_text"]
    code, body = call(base + "/api/structure")
    assert code == 200 and json.loads(body)["kind"] == "cells"


def test_every_fast_method_runs(base):
    rows = json.loads(call(base + "/api/models")[1])["rows"]
    for row in rows:
        for m in row["methods"]:
            if m["LEVEL"] != "fast":
                continue
            inputs = {k: v["value"] for k, v in m["INPUTS"].items()}
            code, body = call(f"{base}/api/run/{row['key']}/{m['key']}", inputs)
            data = json.loads(body)
            assert code == 200, (row["key"], m["key"], data)
            assert "summary" in data["result"] and "k_trans_text" in data["totals"]
            assert not any(k.startswith("_") for k in data["result"])  # internals stay in Python


def test_bad_requests(base):
    assert call(base + "/api/run/structure/honeycomb", {"d": "abc"})[0] == 400
    assert call(base + "/api/run/structure/honeycomb", {"d": -1})[0] == 400
    assert call(base + "/api/run/solid/nope", {})[0] == 404
    assert call(base + "/api/run/solid", {})[0] == 404


def test_page_is_served(base):
    code, body = call(base + "/")
    assert code == 200 and b'src="app.js"' in body
