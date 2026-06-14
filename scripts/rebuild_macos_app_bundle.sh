#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
APP_DIR="$ROOT_DIR/YomiEpub Studio.app"
RESOURCES_DIR="$APP_DIR/Contents/Resources"
ICON_PNG="$ROOT_DIR/docs/assets/yomiepub-studio-icon.png"
ICONSET_DIR="/tmp/yomiepub-icon.iconset"
WHEEL_DIR="/tmp/yomiepub-wheel"

cd "$ROOT_DIR"

mkdir -p "$RESOURCES_DIR"
rm -rf "$WHEEL_DIR"
mkdir -p "$WHEEL_DIR"

python3 -m pip wheel --no-deps "$ROOT_DIR" -w "$WHEEL_DIR"
rm -f "$RESOURCES_DIR"/jp_ebook_furigana_bilingual_pipeline-*.whl
cp "$WHEEL_DIR"/*.whl "$RESOURCES_DIR/"

if command -v sips >/dev/null 2>&1 && command -v iconutil >/dev/null 2>&1 && [ -f "$ICON_PNG" ]; then
  rm -rf "$ICONSET_DIR"
  mkdir -p "$ICONSET_DIR"
  for size in 16 32 128 256 512; do
    sips -z "$size" "$size" "$ICON_PNG" --out "$ICONSET_DIR/icon_${size}x${size}.png" >/dev/null
    sips -z "$((size * 2))" "$((size * 2))" "$ICON_PNG" --out "$ICONSET_DIR/icon_${size}x${size}@2x.png" >/dev/null
  done
  iconutil -c icns "$ICONSET_DIR" -o "$RESOURCES_DIR/YomiEpub.icns"
fi

chmod +x "$APP_DIR/Contents/MacOS/YomiEpub Studio"

echo "Updated $APP_DIR"
