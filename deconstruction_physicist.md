# Phase 1: Deconstruction (The Physicist)
## Atomic Particles of i11 Extraction

The **Extraction Swarm** for i11 node operations is deconstructed into the following atomic components, filtered through the laws of hardware constraints and binary truth:

### 1. The Entry Vector (usbmuxd MITM)
- **Constraint**: The physical link via USB must be established and hijacked.
- **Action**: Use `usbmuxd` to proxy the connection. Target `com.apple.mobile.diagnostics` for service hijacking.
- **Logic**: Redirect port 62078 (standard diagnostics) to a local socket for injection.

### 2. The Payload Delivery (AFC Session Hijack)
- **Constraint**: Filesystem access is restricted to user-space (rootless).
- **Action**: Hijack the `com.apple.afc2` service if available, or fallback to standard AFC.
- **Logic**: Inject the first-stage dropper into `/var/mobile/Media/.system`. This dotfolder is typically overlooked by standard system sweeps.

### 3. The Persistence Layer (launchd Abuse)
- **Constraint**: Persistence must survive reboots without a kernel exploit.
- **Action**: Use a `launchd` abuse plist to trigger a stealth daemon upon specific system events (e.g., sysdiagnose trigger).
- **Logic**: Drop a small IPA + embedded binary + plist. Utilize known remnant APIs for installation without full TrollStore requirements.

### 4. The Exfiltration Pipe (C2 Beacon)
- **Constraint**: Data must be exfiltrated without triggering network anomalies.
- **Action**: Use a small plist-based C2 transport over the established diagnostic pipe.
- **Logic**: Stealth-max flavor: low frequency, encrypted payloads, disguised as standard system logs.

---
*Verified by The Physicist — 2026-05-07*
