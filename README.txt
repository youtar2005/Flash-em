INDEX CARDS — LOCALHOST VERSION

1. Keep index.html, localhost_server.py, and Start Flashcards.bat together.
2. Double-click "Start Flashcards.bat".
3. Your browser should open http://localhost:8765/index.html.
4. When prompted, allow microphone access for localhost.

The command window closes automatically when the flashcard tab is closed.
The page sends a close notification as it unloads. The server waits 5 seconds
before stopping, allowing a reload or navigation back to the app to cancel the
shutdown. Merely switching to another tab does not trigger shutdown.
You can still stop it manually with Ctrl+C.

To change microphone permission in Edge:
  - Open edge://settings/content/microphone
  - Make sure microphone access is enabled.
  - Check that localhost is not in the blocked list.

This launcher uses Python's built-in HTTP server; no extra packages are needed.
The server listens only on your own computer (127.0.0.1).
