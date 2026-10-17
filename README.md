# 2XL-Racing-Server
A custom Python emulation server built to preserve and revive the profile and local features of 2XL Racing

# 2XL Racing Preservation server

A custom emulation backend built with **FastAPI** to revive the local and profile features of the classic mobile game **2XL Racing** (1.3.6), whose official servers are currently offline.

## 🚀 Current status
- **APK Modding:** network security configurations patched (*usesCleartextTraffic="true"`) to allow raw HTTP traffic.
- **Binary Patching:** Hardcoded URLs in `libndkwrapper.so` succesfully redirected using **Ghidra** to localhost (`http://127.0.0.1:8080`).
- **Backend Infrastructure:** Python server listens properly and handles with endpoints with `200 OK` statuses using `adb reverse`.

## 🚧 The Current Challenge (Help Needed!)
The game client succesfully hits the server at `/api/Advertisements/0` and `api/token/initialize`. However, the client-side parser rejects the JSON response payloads and triggers an internal **Server error (6)**.

We need developers experienced in *Smali compilation, JNI runtime environments, or Ghidra/IDA Pro reverse engineering** to help analyze how the binary handles the authentication handshake and identify the exact JSON keys/structures required to unlock the main menu.

## 🛠️ Requirements
- Python 3.10+
- FastAPI & Uvicron
- LDPlayer 9 (with ADB Debugging enabled)
