#!/bin/zsh
set -e
unsetopt bg_nice 2>/dev/null || true

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

URL="http://127.0.0.1:8765"
LOG_DIR="$HOME/Library/Logs"
LOG_FILE="$LOG_DIR/start_yomiepub.log"

open_yomiepub() {
  echo "Opening $URL"
  local chrome_bin="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  if [ -x "$chrome_bin" ]; then
    "$chrome_bin" --new-window "$URL" >> "$LOG_FILE" 2>&1 &
    sleep 0.4
    /usr/bin/open -a "Google Chrome" >/dev/null 2>&1 || true
  else
    /usr/bin/open "$URL"
  fi
  echo
  echo "If the browser did not appear, open this URL manually:"
  echo "$URL"
}

mkdir -p "$LOG_DIR"

echo "YomiEpub Studio"
echo "================"
echo "This window starts the local converter web page."
echo "First launch may take a few minutes while dependencies are installed."
echo

if /usr/sbin/lsof -nP -iTCP:8765 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "YomiEpub Studio is already running."
  open_yomiepub
  echo
  read "?Press Enter to close this window..."
  exit 0
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required."
  echo "Install it from https://www.python.org/downloads/ and run this file again."
  echo
  read "?Press Enter to close..."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creating local Python environment..."
  python3 -m venv .venv
fi

if [ ! -x ".venv/bin/jp-ebook-web" ]; then
  echo "Installing YomiEpub Studio locally..."
  ".venv/bin/python" -m pip install --upgrade pip
  ".venv/bin/python" -m pip install "$ROOT_DIR"
else
  echo "Local environment is ready."
fi

echo
echo "Starting local web page:"
echo "$URL"
echo "Log: $LOG_FILE"
echo
echo "Keep this window open while using YomiEpub Studio."
echo "Press Ctrl+C here to stop the server."
echo

(
  sleep 2
  open_yomiepub
) >/dev/null 2>&1 &
".venv/bin/jp-ebook-web" 2>&1 | tee -a "$LOG_FILE"
