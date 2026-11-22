from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
import threading
import webbrowser

ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8765
CLOSE_GRACE_SECONDS = 5

_state_lock = threading.Lock()
_pending_shutdown = None


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _send_no_content(self):
        self.send_response(204)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def do_GET(self):
        if self.path.split("?", 1)[0] == "/api/heartbeat":
            # A new page load (including a reload) cancels a pending shutdown.
            global _pending_shutdown
            with _state_lock:
                if _pending_shutdown is not None:
                    _pending_shutdown.cancel()
                    _pending_shutdown = None
            self._send_no_content()
            return
        super().do_GET()

    def do_POST(self):
        if self.path.split("?", 1)[0] == "/api/tab-closed":
            # Consume the small sendBeacon payload before responding.
            length = int(self.headers.get("Content-Length", "0"))
            if length:
                self.rfile.read(length)
            global _pending_shutdown
            with _state_lock:
                if _pending_shutdown is not None:
                    _pending_shutdown.cancel()
                _pending_shutdown = threading.Timer(
                    CLOSE_GRACE_SECONDS, self.server.stop_after_tab_close
                )
                _pending_shutdown.daemon = True
                _pending_shutdown.start()
            self._send_no_content()
            return
        self.send_error(404)

    def log_message(self, fmt, *args):
        print("[web] " + (fmt % args), flush=True)


class FlashcardServer(ThreadingHTTPServer):
    def stop_after_tab_close(self):
        print("Flashcard tab closed. Stopping the local server...", flush=True)
        threading.Thread(target=self.shutdown, daemon=True).start()


if __name__ == "__main__":
    os.chdir(ROOT)
    server = FlashcardServer((HOST, PORT), Handler)
    url = f"http://localhost:{PORT}/index.html"
    print("Flashcards are available at:", url, flush=True)
    print("This window closes when the flashcard tab is closed.", flush=True)
    print("A short delay allows page reloads without stopping the server.", flush=True)
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nStopping flashcard server...", flush=True)
    finally:
        server.server_close()
