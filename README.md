# 2XL-Racing-Server

A custom FastAPI server emulator built in Python to preserve and restore the online infrastructure, profile progression, and multiplayer services for the legacy mobile game **2XL Racing** (Android / `libndkwrapper.so`).

---

## Project Status

The login and startup handshake is **~90% complete**. The patched Android client successfully connects to the local FastAPI backend, clears SSL/certificate checks, completes device and account registration, and executes the initial authenticated RPC sequence.

### Working Endpoints (`200 OK`)
* `GET /api/Advertisements/{playerId}?placement=prelogin` — Pre-login banner handshake.
* `GET /api/token/initialize` — Initial request token generation (`RequestToken` + `RequestTokenSecret`).
* `POST /api/deviceinfo` — Device telemetry and hardware registration.
* `POST /api/Accounts` — Player account verification (`AccountFound`).
* `GET /api/token/authorize` — Session authorization token (`AuthorizationToken` + `Secret`) synced with dynamic `CurrentTime` (`int(time.time())`).
* `GET /api/Products?binary=true&nativeStore=GooglePlay` — Binary store catalog response (`application/octet-stream`).
* `GET /api/VideoReplay/GetUploadedReplays` — Replay list check.
* `GET /api/rpc/Profile/{playerId}/GetEventPrizes` — Event rewards check.
* `POST /api/rpc/Debug/{playerId}/DebuggingEnabled` — Debug state check.

### Current Blocker: Startup State Error `(8)`
* **Symptom:** After completing the initial authenticated RPC calls above, the client triggers Error `(8)` (*"Houston, we have a problem... (8)"*) before reaching the main menu/garage.
* **What We Know:** The final two startup state calls (`crew-settings` and `locations`) have been mapped in `libndkwrapper.so` and stubbed in `server_2xl.py`, but the state machine aborts right after `DebuggingEnabled`.

---

## Reverse Engineering Findings (`libndkwrapper.so` — x86)

All offsets below correspond to the x86 native library (`libndkwrapper.so`):

* **HMAC-SHA256 Request Signing (`FUN_0030bfa4` @ `0x0030c3d4`):**
  * Outgoing client requests concatenate `RequestToken`, `RequestTokenSecret`, `Retries`, `Timestamp`, `TwoXLGuid`, `TwoXLSecret`, `Version`, and the request body, then compute an HMAC-SHA256 digest (`FUN_00285a07`) sent in the `Signature` HTTP header.
  * The client **does not** validate an incoming `Signature` header on server responses.
* **Startup State Machine & Error `(8)` (`FUN_000b0102` / `FUN_000a27c8`):**
  * `FUN_000b0102` manages the 12 sequential startup steps (`0`–`11`). If any step passes `param_3 == 0` (JSON parse failure or false flag), it sets `*(param_1 + 0x26c8) = 8` (Error `8`) and transitions to error state `6`.
* **Shared RapidJSON Boolean Deserializer (`DAT_0051e684`):**
  * Multiple RPC callbacks (`FUN_00100d12` for `DebuggingEnabled`, `FUN_000c67d4` for `GetEventPrizes`, and `FUN_000c82b6` for `GetUploadedReplays`) deserialize responses using the shared boolean table at `DAT_0051e684`.
* **Remaining Startup Endpoints (`FUN_000a9a2e` & `FUN_000a9b8c`):**
  * State `10` (`FUN_000a9a2e` @ `0x000a9a67`) targets `"crew-settings"`.
  * State `11` (`FUN_000a9b8c` @ `0x000a9bfc`) targets `"locations"`.

---

## How to Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the FastAPI server:**
   ```bash
   python -m uvicorn server_2xl:app --host 0.0.0.0 --port 8080 --reload
   ```
3. **Configure the client:**
   * Patch `libndkwrapper.so` to point the server base URL to your local IP (e.g., `http://192.168.x.x:8080` or `http://10.0.2.2:8080` for Android emulators).

---

## Contributing

Pull requests and reverse engineering notes are welcome! If you have experience with RapidJSON deserialization tables in x86 binaries or 2XL Games' RDK backend, check the **Issues** tab to help resolve the final startup state transition into the main menu.
