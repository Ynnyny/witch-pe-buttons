#!/bin/sh
# Build PEButtons.dylib and pack a .plgw. Needs macOS + Xcode command line tools.
#
#   WITCH_LAUNCHER_DIR=~/Witch_launcher ./tools/build_and_pack.sh
#
# First time only, make a signing key:
#   python3 "$WITCH_LAUNCHER_DIR/scripts/plugins/pack_plugin.py" --generate-key ./keys/private.pem --key-id my-key
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LAUNCHER="${WITCH_LAUNCHER_DIR:?set WITCH_LAUNCHER_DIR to your Witch_launcher checkout (beta branch)}"
KEY="${PLUGIN_PRIVATE_KEY:-$ROOT/keys/private.pem}"
KEY_ID="${PLUGIN_KEY_ID:-my-key}"
SDK="$(xcrun --sdk iphoneos --show-sdk-path)"

xcrun --sdk iphoneos clang -dynamiclib -fobjc-arc -arch arm64 -miphoneos-version-min=14.0 \
  -isysroot "$SDK" -I "$LAUNCHER/Natives/PluginKit" -I "$LAUNCHER/Natives" \
  -framework UIKit -framework Foundation -framework CoreGraphics -framework QuartzCore \
  -Wl,-undefined,dynamic_lookup \
  -o "$ROOT/plugin/PEButtons.dylib" "$ROOT/plugin/PEButtons.m"
codesign --force --sign - "$ROOT/plugin/PEButtons.dylib"

python3 "$LAUNCHER/scripts/plugins/pack_plugin.py" \
  --source "$ROOT/plugin" --private-key "$KEY" --key-id "$KEY_ID" \
  --out "$ROOT/pe-buttons-1.0.0.plgw"
python3 "$LAUNCHER/scripts/plugins/pack_plugin.py" --verify "$ROOT/pe-buttons-1.0.0.plgw"
