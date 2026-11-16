#!/bin/sh
# Build PEButtons.dylib and pack a .plgw. Needs macOS + Xcode command line tools.
#
#   WITCH_LAUNCHER_DIR=~/Witch_launcher ./tools/build_and_pack.sh
#
# The signing key MUST stay the same for every release: the launcher pins the
# publisher key of an installed plugin and refuses a build that was signed with
# a different key. Generate the key once and keep it in CI secrets:
#
#   python3 "$WITCH_LAUNCHER_DIR/scripts/plugins/pack_plugin.py" \
#       --generate-key ./keys/private.pem --key-id pe-buttons
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LAUNCHER="${WITCH_LAUNCHER_DIR:?set WITCH_LAUNCHER_DIR to your Witch_launcher checkout}"
KEY="${PLUGIN_PRIVATE_KEY:-$ROOT/keys/private.pem}"
KEY_ID="${PLUGIN_KEY_ID:-pe-buttons}"
SDK="$(xcrun --sdk iphoneos --show-sdk-path)"

# The artifact is named after the version in the manifest, so the file name and
# the manifest never drift apart.
VERSION="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["version"])' "$ROOT/plugin/witch-plugin.json")"
OUT="$ROOT/pe-buttons-$VERSION.plgw"

if [ ! -f "$KEY" ]; then
  echo "error: signing key not found at $KEY" >&2
  echo "       generate one with pack_plugin.py --generate-key, then keep it stable" >&2
  exit 1
fi

rm -f "$OUT"

xcrun --sdk iphoneos clang -dynamiclib -fobjc-arc -arch arm64 -miphoneos-version-min=14.0 \
  -isysroot "$SDK" -I "$LAUNCHER/Natives/PluginKit" -I "$LAUNCHER/Natives" \
  -framework UIKit -framework Foundation -framework CoreGraphics -framework QuartzCore \
  -Wl,-undefined,dynamic_lookup \
  -o "$ROOT/plugin/PEButtons.dylib" "$ROOT/plugin/PEButtons.m"
codesign --force --sign - "$ROOT/plugin/PEButtons.dylib"

python3 "$LAUNCHER/scripts/plugins/pack_plugin.py" \
  --source "$ROOT/plugin" --private-key "$KEY" --key-id "$KEY_ID" \
  --out "$OUT"
python3 "$LAUNCHER/scripts/plugins/pack_plugin.py" --verify "$OUT"

echo
echo "artifact: $OUT"
echo "sha256:   $(shasum -a 256 "$OUT" | awk '{print $1}')"
echo "put that sha256 into witch-plugins.json so the launcher can pin the download"
