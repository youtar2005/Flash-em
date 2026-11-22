# Flash 'em

A locally hosted flashcard application that runs in your web browser. The application uses a lightweight Python HTTP server to provide a localhost address, allowing browser features such as microphone access and speech recognition to work reliably.

## 1. Requirements

The following files must be kept together in the same directory:

| File | Purpose |
|---|---|
| `index.html` | Main flashcard application |
| `localhost_server.py` | Python HTTP server |
| `Flash 'em.vbs` | Hidden launcher that starts the server without displaying a command window |

Additional requirements:

- Windows operating system.
- Python 3 installed and accessible through the `py` command.
- Microsoft Edge, Google Chrome, or another compatible browser.
- A working microphone if you intend to use voice-based answers.

No additional Python packages are required. The server uses Python's standard library.

## 2. Starting the application

1. Make sure all three files are in the same folder.
2. Double-click **`Flash 'em.vbs`**.
3. The Python server starts in the background.
4. Your default browser should automatically open:

   `http://localhost:8765/index.html`

5. If prompted, grant microphone access to localhost.

The application should now be ready to use.

**Important:** Do not manually close the browser tab while expecting the server to remain available. Closing the application tab initiates the server shutdown process.

## 3. Server lifecycle and automatic shutdown

The server is designed to run only while the flashcard application is being used.

### Closing the application

When the flashcard webpage is closed or navigated away from, it sends a shutdown notification to the local server.

The server then:

1. Receives the close notification.
2. Starts a five-second shutdown delay.
3. Checks whether the application has been reopened or reloaded.
4. Shuts down if no new application connection is detected.

This delay allows the application to reload without unnecessarily terminating the server.

### Browser tab behaviour

| Action | Expected behaviour |
|---|---|
| Switch to another browser tab | Server remains running |
| Minimise the browser | Server remains running |
| Reload the flashcard page | Shutdown is cancelled |
| Navigate away from the flashcard page | Shutdown is initiated |
| Close the flashcard tab | Shutdown is initiated |
| Close the entire browser | Shutdown is initiated when the browser sends the page-unload notification |

**Note:** Browser shutdown notifications are not guaranteed in every situation. For example, a browser crash or forced termination may prevent the notification from reaching the server.

### Manual shutdown

If the server is running in a visible debugging session, you can stop it manually by pressing:

`Ctrl + C`

When launched through the hidden VBScript launcher, there is no visible command window in which to enter this command.

## 4. Microphone permissions

The application uses browser microphone functionality for spoken answers. Microphone access must be explicitly granted.

### Microsoft Edge

1. Open Microsoft Edge.
2. Navigate to:

   `edge://settings/content/microphone`

3. Make sure **Ask before accessing** or the equivalent microphone permission setting is enabled.
4. Check that microphone access is not blocked for localhost.
5. Select the desired microphone if multiple devices are available.

### Google Chrome

1. Open Google Chrome.
2. Navigate to:

   `chrome://settings/content/microphone`

3. Make sure microphone access is enabled.
4. Check that localhost is not listed under blocked websites.

### Windows microphone permissions

If the browser cannot access the microphone despite having permission:

1. Open Windows Settings.
2. Navigate to **Privacy & security → Microphone**.
3. Enable microphone access.
4. Enable microphone access for desktop applications.

The first time the application requests microphone access, the browser may display a permission prompt. Select **Allow**.

## 5. Network and security

The server listens on:

- **Host:** `127.0.0.1`
- **Port:** `8765`
- **Application URL:** `http://localhost:8765/index.html`

The server binds exclusively to `127.0.0.1`, meaning it accepts connections from the local computer rather than exposing the application to other devices on the network.

The application does not require an internet-facing server or external hosting.

Some application functionality, such as loading external JavaScript libraries or models, may still require an internet connection.

## 6. Troubleshooting

### The browser does not open

Open the following address manually:

`http://localhost:8765/index.html`

If the page still does not load, check whether Python is installed:

```cmd
py --version
```

If Python is not recognised, install Python and ensure its launcher is available.

### The page cannot connect to localhost

Possible causes include:

- The Python server failed to start.
- Another application is already using port `8765`.
- The server script is missing or located in a different directory.
- Python is not accessible through the `py` command.

For debugging, run the server manually from the application directory:

```cmd
py -3 localhost_server.py
```

This displays server messages and errors in the command window.

### The microphone does not work

Check the following:

- Browser microphone permission is enabled.
- Windows microphone privacy settings allow access.
- The correct microphone is selected.
- The microphone is not being used exclusively by another application.

### The server closes unexpectedly

The server uses the webpage's unload notification to determine when the application is closed. If the browser sends an unload notification during navigation, the server may begin its shutdown procedure.

If this happens unexpectedly, reload the application by starting `Flash 'em.vbs` again.

## 7. Technical overview

The application consists of three components:

**`index.html`**

The frontend containing the flashcard interface, deck selection, answer evaluation, speech synthesis, and voice input functionality.

**`localhost_server.py`**

A Python HTTP server based on:

- `http.server`
- `ThreadingHTTPServer`
- `SimpleHTTPRequestHandler`

It serves the application locally and handles the shutdown notification.

**`Flash 'em.vbs`**

A Windows Script Host launcher that starts the Python server without displaying a command prompt.

The server requires no third-party Python dependencies.

## 8. Quick reference

| Item | Value |
|---|---|
| Start application | Double-click `Flash 'em.vbs` |
| Local application URL | `http://localhost:8765/index.html` |
| Server host | `127.0.0.1` |
| Server port | `8765` |
| Shutdown delay | 5 seconds |
| Python command | `py -3 localhost_server.py` |
| Dependencies | Python standard library only |
| Network exposure | Local computer only |
