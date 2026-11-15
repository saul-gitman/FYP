"""JSON API + static files for the web UI, on the standard-library http.server.

GET  /api/models               every row and method (all UI words), plus the current results
POST /api/run/<row>/<method>   body = {input: value}; runs it, returns the result + totals
GET  /api/structure            geometry for the 3D view
Anything else is served from web/.
"""

import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import numpy as np

from aerosim.core import registry, ui_text
from aerosim.core.state import State

WEB = Path(__file__).resolve().parents[2] / "web"


def clean(obj):
    """Make results plain JSON: NumPy numbers/arrays → Python, NaN/inf → null."""
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, np.ndarray)):
        return [clean(v) for v in obj]
    if isinstance(obj, np.generic):
        obj = obj.item()
    if isinstance(obj, float) and not np.isfinite(obj):
        return None
    return obj


def make_handler(state):
    lock = threading.Lock()  # one run at a time: the rows share one state

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(WEB), **kwargs)

        def log_message(self, *args):  # keep the terminal quiet
            pass

        def send_json(self, obj, code=200):
            body = json.dumps(clean(obj), ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/api/models":
                with lock:
                    state.refresh()  # a method file added since the last call appears now
                    texts = {k: v for k, v in vars(ui_text).items() if k.isupper()}
                    rows = registry.describe([state.rows[k] for k in state.order])
                    self.send_json({"ui": texts, "rows": rows} | state.snapshot())
            elif self.path == "/api/structure":
                with lock:
                    s = state.results["structure"]
                    self.send_json(s.get("_geometry", {"kind": "none"}))
            else:
                super().do_GET()

        def do_POST(self):
            parts = self.path.strip("/").split("/")
            if len(parts) != 4 or parts[:2] != ["api", "run"]:
                return self.send_json({"error": "unknown address"}, 404)
            try:
                length = int(self.headers.get("Content-Length", 0))
                inputs = json.loads(self.rfile.read(length) or b"{}")
                if not isinstance(inputs, dict):
                    raise ValueError("the body must be a JSON object {input: value}")
                with lock:
                    result = state.run(parts[2], parts[3], inputs)
                    self.send_json({"result": result} | state.snapshot())
            except KeyError as e:
                self.send_json({"error": e.args[0]}, 404)
            except (ValueError, TypeError) as e:
                self.send_json({"error": str(e)}, 400)
            except Exception as e:  # e.g. a method file that breaks the contract
                self.send_json({"error": f"{type(e).__name__}: {e}"}, 500)

    return Handler


def serve(port=8000, host="127.0.0.1"):
    """Start the server (blocks). Returns only on Ctrl+C."""
    server = ThreadingHTTPServer((host, port), make_handler(State()))
    print(
        f"Aerogel k Simulator on http://localhost:{server.server_port}  (Ctrl+C to stop)",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
