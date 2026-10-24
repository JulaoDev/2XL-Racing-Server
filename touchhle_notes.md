# iOS Emulation Research - touchHLE Integration

We have successfully tested the iOS version (`.ipa`) of 2XL Racing inside the **touchhle (HyperHLE Reborn)** environment. The game assets and core graphics initializations boot flawlessly.

## Current Network Hanshake block
When clicking the "CONTINUE" action dialog button on the server expiration button on the server expiration screen layout, the internal binary processes standard telemetry hooks before terminating.

## Extracted Console Logs:
```text
touchHLE::objc::messages: Call to faked class "FlurryAds"
touchHLE::objc::messages: Call to faked class "NSHTTPCookie"
touchHLE::Libc::stdlib: Guest exit(0) on emulated thread 0; attempting validated frame recovery.
```

### Analysis:
1. The game client queries native iOS configuration singletons (`NSHTTPCookie`) looking for active valid session headers.
2. If no valid legacy persistent cache is found mapping a registered user, the internal application structure deliberately runs a clean **`exit(0)`** validation bypass abort rather than a critical system crash.
3. Setting static local dictionaries (`FirstLaunch = false`, `HasProfile = true`) inside the application bundle context sandbox preferences path (`com.twoxlgames.street.plist`) is currently not sufficient to cheat the validation logic without a full persistent data folder template structure.

## Legacy Client Assets
* **Decrypted iOS client package (.ipa):** https://drive.google.com/file/d/1d2slJeF0GEZk_DeyM4iFx_XSUCyEb9fm/view?usp=sharing
