#!/bin/zsh
set -e
unsetopt bg_nice 2>/dev/null || true

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

URL="http://127.0.0.1:8765"

echo "YomiEpub Studio"
echo "================"
echo "This window starts the local converter web page."
echo "First launch may take a few minutes while dependencies are installed."
echo

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

echo "Installing or updating YomiEpub Studio locally..."
".venv/bin/python" -m pip install --upgrade pip
".venv/bin/python" -m pip install --upgrade "$ROOT_DIR"

echo
echo "Starting local web page:"
echo "$URL"
echo
echo "Keep this window open while using YomiEpub Studio."
echo "Press Ctrl+C here to stop the server."
echo

".venv/bin/python" -c 'import subprocess, sys; subprocess.Popen([sys.executable, "-c", "import subprocess, time; time.sleep(2); subprocess.run([\"open\", \"http://127.0.0.1:8765\"])"])'
".venv/bin/jp-ebook-web"
