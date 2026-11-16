# PE Buttons — a plugin for Witch Launcher

Re-skins the in-game touch controls (buttons, the drawer, the joystick) in the style of
**Minecraft: Pocket/Bedrock Edition**, using the button textures of the **TouchController**
mod (LGPL-3.0-or-later):

- **Action buttons** (D-pad, jump, sneak, sprint, inventory, chat, pause, ...) use the ready-made TouchController sprite, including its pressed ("_active") variant.
- **Every other button** keeps its name, drawn over an empty PE-style nine-patch button.
- **Joystick** uses the TouchController `pad` and `stick`.
- Two texture sets: **classic** (old PE, stone) and **new** (current Bedrock, rounded).

The plugin is native (`.dylib`, ABI 2). It hooks `ControlButton` / `ControlJoystick` of the
launcher.

> Vietnamese version: [README.md](README.md)

## ⚠️ Native plugin: the sandbox has to be off

The launcher analyses every plugin before it runs. A plugin that ships **native code** is
always graded **Dangerous** (red badge): its code runs inside the launcher process and
cannot be isolated.

At install time the launcher asks you to choose:

| Choice | Result |
| --- | --- |
| **Install inside the sandbox** | Native code stays blocked → **the plugin does nothing**. Useful to try the package out. |
| **Install and allow native code** | The plugin runs normally. Pick this one if you trust the source. |

The sandbox can be toggled later on the plugin screen (**Sandbox**). Turning it back on
blocks the native code and the plugin stops working.

## Installing

### From the plugin catalog (recommended)

This repository is also the launcher's **catalog**. Open **Settings → Plugins → Available
Plugins** and tap **Install** on the PE Buttons row. The launcher downloads the package from
the Release, checks it against the SHA-256 pinned in `witch-plugins.json`, verifies the
signature and every checksum, and only then asks about the sandbox.

### From a `.plgw` file

Download `pe-buttons-1.1.0.plgw` from [Releases](https://github.com/Ynnyny/witch-pe-buttons/releases)
→ copy it to the device → **Settings → Plugins → `+`** → pick the package.

> The package must be **verified by the Witch registry** before the launcher installs it. A
> build the registry has not approved is rejected.

### Requirements

- A launcher build that supports native plugins (the installation has to allow loading a
  self-signed dylib).
- Restart the launcher after installing.

## Which button gets a sprite

A sprite is only used when the button is **roughly square** and sends **exactly one key**
(buttons that send several keys keep their written name). Wide buttons — Keyboard, Chat,
Debug in the default layout — show the empty background plus the name.

| Key / action | Sprite |
| --- | --- |
| W / A / S / D, D-pad, scroll up/down | `up` `left` `down` `right` |
| Space / Left Shift / Left Ctrl | `jump` / `sneak` / `sprint` |
| E / T / Esc, Menu | `inventory` / `chat` / `pause` |
| F1 / F2 / F3 / F5 | `hide_hud` / `screenshot` / `debug_screen` / `perspective` |
| F (offhand) / Tab | `shield` / `player_list` |
| Left / right mouse button | `attack` (or `pickaxe`) / `use` |
| **Everything else** (Opti-Zoom, GUI, Keyboard, Mouse, custom names…) | **the button name on a PE background** |

## Settings (Settings → Plugins → PE Buttons)

Texture set (classic / new) · sprites or text only · the text-button background from
TouchController (1–5) · pixel size (automatic or 1–4 pt) · use your own textures. Restart the
launcher after changing them.

## Using your own textures

Drop PNGs with the same relative path into `POJAV_HOME/PEButtons/` (next to `plugins.json`).
Whatever is there wins over the bundled file: `classic/jump.png`, `classic/jump_active.png`,
`new/up.png`, `empty/empty_1.png`, `classic/joystick_pad.png`…
The nine-patch background stretches according to `nine.json` (`l/t/r/b` = border size in
texels); the default is a third of the short side.

## Building and packaging (needs macOS + Xcode)

```sh
git clone -b beta https://github.com/Witch-Launcher/Witch_launcher.git
python3 Witch_launcher/scripts/plugins/pack_plugin.py --generate-key ./keys/private.pem --key-id pe-buttons
WITCH_LAUNCHER_DIR=$PWD/Witch_launcher ./tools/build_and_pack.sh
```

The script reads the version from `plugin/witch-plugin.json` to name the package
(`pe-buttons-<version>.plgw`), packs it, verifies it again and prints the **SHA-256** of the
package so you can put it into `witch-plugins.json`.

> **The hash changes with every build.** The ECDSA signature is randomized, so each packed
> `.plgw` differs byte for byte. Publish the exact file you attach to the release and use
> the SHA-256 of that very file in `witch-plugins.json`.

> **The signing key must stay the same.** The launcher pins the publisher key of an installed
> plugin and refuses a build that was signed with a different key. CI must therefore **not**
> generate a fresh key on every run — put the key into the `PLUGIN_PRIVATE_KEY_PEM` secret.

No Mac? Push this folder to GitHub, run the `Build PE Buttons` workflow
(`.github/workflows/build.yml`) and download the `.plgw` from the artifacts.

Before building, **set `source` in `plugin/witch-plugin.json`** to your real repository URL.

## Publishing a new version

1. Build (see above) and take the `artifact_sha256` and `checksums_sha256` from the log.
2. **Submit it to the Witch registry** — the launcher only installs a build the registry verified:

```sh
curl -X POST https://witch-worker.vvvuduyanh2012.workers.dev/v1/plugins/submit \
  -H 'Content-Type: application/json' \
  -d '{
    "pluginId": "com.witch.community.pe-buttons",
    "version": "1.1.0",
    "name": "PE Buttons",
    "summary": "Minecraft PE style touch controller buttons.",
    "author": "Community",
    "license": "LGPL-3.0-or-later",
    "sourceUrl": "https://github.com/Ynnyny/witch-pe-buttons",
    "artifactSha256": "<artifact_sha256>",
    "checksumsSha256": "<checksums_sha256>",
    "publicKey": "<public_key>",
    "publisherKeyId": "pe-buttons",
    "permissions": []
  }'
```

3. **Let an admin approve it** (`X-Admin-Key` is the registry admin key):

```sh
curl -H 'X-Admin-Key: ...' -X POST \
  'https://witch-worker.vvvuduyanh2012.workers.dev/admin/plugins/com.witch.community.pe-buttons/verify' \
  -d '{"version":"1.1.0","notes":"Source and license reviewed"}'
```

4. **Publish a Release** with the package you built, then put the SHA-256 of **that exact
   file** into `witch-plugins.json` and commit it.

> The registry approves one hash. A rebuild changes the hash (the ECDSA signature is
> randomized), so a new build has to be submitted and approved again.

## Updating the textures from TouchController

```sh
git clone --depth 1 https://github.com/fifth-light/TouchController.git
pip install pillow
python3 tools/import_touchcontroller.py ./TouchController
python3 tools/preview.py classic preview.png      # preview using those very PNGs
```

## License

`PEButtons.m`: MIT. Textures: LGPL-3.0-or-later from TouchController (see
`plugin/NOTICE.md` and `plugin/LICENSE`). The package itself declares
`LGPL-3.0-or-later`. It contains no Mojang assets.

## Current limitations

- Sprites are fixed squares, so they are only used for roughly square buttons; wide buttons
  use the empty background plus the name.
- The button text uses the bold system font with a hard drop shadow (not the Minecraft pixel
  font) so that accented names stay readable.
- Only the in-game controls are reskinned; the launcher home screen buttons are untouched.
- The hooks are installed with `class_replaceMethod` and are **not** removed when the plugin
  is uninstalled — restart the launcher after uninstalling.
