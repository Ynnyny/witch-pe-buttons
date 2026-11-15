# PE Buttons — plugin cho Witch Launcher

Đổi nút điều khiển trong game (nút, ngăn kéo/drawer, joystick) sang kiểu **Minecraft PE**,
dùng chính texture nút của mod **TouchController** (LGPL-3.0-or-later):

- **Nút hành động** (D-pad, nhảy, ngồi, chạy, túi đồ, chat, tạm dừng, ...) → dùng sprite sẵn của TouchController, có bản "active" khi bấm.
- **Mọi nút còn lại** → **nền nút trống kiểu PE (9-patch) + tên nút** vẽ lên trên.
- **Joystick** → `pad` + `stick` của TouchController.
- Hai bộ texture: **classic** (PE cũ, đá xám) và **new** (Bedrock hiện tại, bo tròn).

Plugin native (`.dylib`, ABI 2) móc vào `ControlButton` / `ControlJoystick` của launcher nhánh `beta`.

## Nút nào ra sprite, nút nào ra chữ

Sprite chỉ dùng khi nút **gần vuông** và gửi **đúng 1 phím** (nút gửi nhiều phím giữ tên chữ).
Nút dài (như Keyboard, Chat, Debug trong layout mặc định) hiện nền trống + tên.

| Phím / hành động | Sprite |
| --- | --- |
| W / A / S / D, D-pad, cuộn lên/xuống | `up` `left` `down` `right` |
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
python3 Witch_launcher/scripts/plugins/pack_plugin.py --generate-key ./keys/private.pem --key-id my-key
WITCH_LAUNCHER_DIR=$PWD/Witch_launcher PLUGIN_KEY_ID=my-key ./tools/build_and_pack.sh
```

Không có Mac: đẩy thư mục này lên GitHub, chạy workflow `Build PE Buttons`
(`.github/workflows/build.yml`), tải `.plgw` ở Artifacts.

Trước khi build, **sửa `source` trong `plugin/witch-plugin.json`** thành URL repo thật của bạn.
Cài: chép `.plgw` vào máy → Settings → Plugins → `+`. Theo docs, build phải được registry xác minh mới
cài được, hoặc để trống `Witch base URL` để bỏ qua bước này (mình chưa kiểm chứng). Plugin native còn
cần bản cài cho phép nạp dylib tự ký.

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

- Chưa build/chạy thử trên thiết bị thật (không có Xcode/iOS SDK ở môi trường mình). Mã đã qua kiểm
  tra cú pháp bằng libclang với header giả, và gói đã qua packer của launcher.
- Sprite là hình vuông cố định nên chỉ dùng cho nút gần vuông; nút dài dùng nền trống + tên.
- Chữ trên nút dùng font hệ thống đậm + bóng đổ cứng (không phải font pixel của Minecraft) để giữ tên tiếng Việt có dấu.
- Chỉ đổi nút điều khiển trong game, chưa đụng nút ở màn hình chính của launcher.
