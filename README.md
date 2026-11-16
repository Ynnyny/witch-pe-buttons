# PE Buttons — plugin cho Witch Launcher

Đổi nút điều khiển trong game (nút, ngăn kéo/drawer, joystick) sang kiểu **Minecraft PE**,
dùng chính texture nút của mod **TouchController** (LGPL-3.0-or-later):

- **Nút hành động** (D-pad, nhảy, ngồi, chạy, túi đồ, chat, tạm dừng, ...) → dùng sprite sẵn của TouchController, có bản "active" khi bấm.
- **Mọi nút còn lại** → **nền nút trống kiểu PE (9-patch) + tên nút** vẽ lên trên.
- **Joystick** → `pad` + `stick` của TouchController.
- Hai bộ texture: **classic** (PE cũ, đá xám) và **new** (Bedrock hiện tại, bo tròn).

Plugin native (`.dylib`, ABI 2) móc vào `ControlButton` / `ControlJoystick` của launcher.

> Bản tiếng Anh: [README.en.md](README.en.md)

## ⚠️ Plugin native: cần tắt sandbox

Launcher phân tích mọi plugin trước khi chạy. Một plugin có **mã native** luôn bị xếp mức
**Nguy hiểm** (huy hiệu đỏ) vì code của nó chạy ngay trong tiến trình launcher và không
cách ly được.

Khi cài, launcher sẽ hỏi bạn chọn:

| Lựa chọn | Kết quả |
| --- | --- |
| **Cài đặt trong sandbox** | Mã native bị chặn → **plugin không làm gì cả**. Dùng cho bản dùng thử. |
| **Cài đặt và cho chạy mã native** | Plugin chạy bình thường. Chọn lựa chọn này nếu bạn tin nguồn của mình. |

Sau khi cài, plugin vẫn có thể bật/tắt sandbox ở màn hình chi tiết plugin (**Sandbox**).
Bật lại sandbox sẽ chặn mã native và plugin sẽ ngừng hoạt động.

## Cài đặt

### Từ danh mục plugin (khuyến nghị)

Repository này cũng là **catalog** của launcher. Mở **Settings → Plugins → Available Plugins**
rồi bấm **Install** trên dòng PE Buttons. Launcher tải gói từ Release, kiểm tra mã băm
(SHA-256) đã ghim trong `witch-plugins.json`, xác minh chữ ký và checksum, rồi mới hỏi bạn
về sandbox.

### Từ file `.plgw`

Tải `pe-buttons-1.1.0.plgw` từ [Releases](https://github.com/Ynnyny/witch-pe-buttons/releases)
→ chép vào máy → **Settings → Plugins → `+`** → chọn gói.

> Gói phải được **Witch registry xác minh** thì launcher mới cho cài. Nếu bản dựng của bạn
> chưa được registry duyệt, launcher sẽ báo "chưa xác minh" và từ chối cài.

### Yêu cầu

- Launcher bản có hỗ trợ plugin native (cần bản cài cho phép nạp dylib tự ký).
- Khởi động lại launcher sau khi cài.

## Nút nào ra sprite, nút nào ra chữ

Sprite chỉ dùng khi nút **gần vuông** và gửi **đúng 1 phím** (nút gửi nhiều phím giữ tên chữ).
Nút dài (như Keyboard, Chat, Debug trong layout mặc định) hiện nền trống + tên.

| Phím / hành động | Sprite |
| --- | --- |
| W / A / S / D, D-pad, cuộn lên/xuốn | `up` `left` `down` `right` |
| Space / Left Shift / Left Ctrl | `jump` / `sneak` / `sprint` |
| E / T / Esc, Menu | `inventory` / `chat` / `pause` |
| F1 / F2 / F3 / F5 | `hide_hud` / `screenshot` / `debug_screen` / `perspective` |
| F (đổi tay phụ) / Tab | `shield` / `player_list` |
| Chuột trái / phải | `attack` (hoặc `pickaxe`) / `use` |
| **Còn lại** (Opti-Zoom, GUI, Keyboard, Mouse, tên tự đặt...) | **tên nút trên nền PE** |

## Cài đặt (Settings → Plugins → PE Buttons)

Bộ texture (classic/new) · dùng sprite hay chỉ chữ · mẫu nền nút chữ (1–5 của TouchController) ·
cỡ pixel (tự động hoặc 1–4 pt) · dùng texture riêng. Đổi xong cần khởi động lại launcher.

## Dùng texture riêng

Đặt PNG cùng đường dẫn vào `POJAV_HOME/PEButtons/` (cạnh `plugins.json`), file nào có ở đó
được ưu tiên: `classic/jump.png`, `classic/jump_active.png`, `new/up.png`,
`empty/empty_1.png`, `classic/joystick_pad.png`...
Nền 9-patch co giãn theo `nine.json` (`l/t/r/b` = số texel viền); mặc định là 1/3 cạnh ngắn.

## Build và đóng gói (cần macOS + Xcode)

```sh
git clone -b beta https://github.com/Witch-Launcher/Witch_launcher.git
python3 Witch_launcher/scripts/plugins/pack_plugin.py --generate-key ./keys/private.pem --key-id pe-buttons
WITCH_LAUNCHER_DIR=$PWD/Witch_launcher ./tools/build_and_pack.sh
```

Script sẽ tự lấy version trong `plugin/witch-plugin.json` để đặt tên gói
(`pe-buttons-<version>.plgw`), đóng gói, verify lại và in ra **SHA-256** của gói để bạn
điền vào `witch-plugins.json`.

> **Mã băm đổi mỗi lần build.** Chữ ký ECDSA có khoá ngẫu nhiên nên gói `.plgw` mỗi lần
> đóng gói đều khác byte. Hãy publish đúng tệp bạn đính kèm vào Release và dùng SHA-256
> của chính tệp đó trong `witch-plugins.json`.

> **Khóa ký phải giữ nguyên.** Launcher ghim khóa của nhà phát hành khi cài; một bản build
> ký bằng khóa khác sẽ bị launcher từ chối. Vì vậy CI **không được** tự sinh khóa mới mỗi lần
> build — hãy đặt khóa vào secret `PLUGIN_PRIVATE_KEY_PEM`.

Không có Mac: đẩy thư mục này lên GitHub, chạy workflow `Build PE Buttons`
(`.github/workflows/build.yml`), tải `.plgw` ở Artifacts.

Trước khi build, **sửa `source` trong `plugin/witch-plugin.json`** thành URL repo thật của bạn.

## Phát hành bản mới

1. Build (xem trên) → nhận `artifact_sha256` và `checksums_sha256` trong log.
2. **Nộp lên Witch registry** — launcher chỉ cài build đã được registry xác minh:

```sh
curl -X POST https://witch-worker.vvvuduyanh2012.workers.dev/v1/plugins/submit \
  -H 'Content-Type: application/json' \
  -d '{
    "pluginId": "com.witch.community.pe-buttons",
    "version": "1.1.0",
    "name": "PE Buttons",
    "summary": "Nút điều khiển kiểu Minecraft PE.",
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

3. **Admin duyệt** (`X-Admin-Key` là khoá admin của registry):

```sh
curl -H 'X-Admin-Key: ...' -X POST \
  'https://witch-worker.vvvuduyanh2012.workers.dev/admin/plugins/com.witch.community.pe-buttons/verify' \
  -d '{"version":"1.1.0","notes":"Source and license reviewed"}'
```

4. **Đăng Release** với file `.plgw` đã build, rồi cập nhật `sha256` trong
   `witch-plugins.json` bằng SHA-256 của **đúng file đó** và commit.

> Registry chỉ duyệt build đúng hash đó. Nếu bạn build lại, hash đổi (chữ ký ECDSA có
> khoá ngẫu nhiên) nên phải nộp và duyệt lại bản mới.

## Cập nhật texture từ TouchController

```sh
git clone --depth 1 https://github.com/fifth-light/TouchController.git
pip install pillow
python3 tools/import_touchcontroller.py ./TouchController
python3 tools/preview.py classic preview.png      # ảnh xem trước bằng chính các PNG đó
```

## License

Mã `PEButtons.m`: MIT. Texture: LGPL-3.0-or-later của TouchController (xem `plugin/NOTICE.md`,
`plugin/LICENSE`). Cả gói khai báo `LGPL-3.0-or-later`. Không chứa tài nguyên của Mojang.

## Giới hạn hiện tại

- Sprite là hình vuông cố định nên chỉ dùng cho nút gần vuông; nút dài dùng nền trống + tên.
- Chữ trên nút dùng font hệ thống đậm + bóng đổ cứng (không phải font pixel của Minecraft) để giữ tên tiếng Việt có dấu.
- Chỉ đổi nút điều khiển trong game, chưa đụng nút ở màn hình chính của launcher.
- Hook được cài bằng `class_replaceMethod` và **không** gỡ khi plugin bị gỡ; cần khởi động
  lại launcher sau khi gỡ.
