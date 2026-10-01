# Gate 9 actual VM115 cold stop/start — PASS

Fresh Proxmox configuration verified firewall VM112 running with onboot=1,
startup order=1/up=15, and application VM115 onboot=1/startup order=2. The named
application identity, guest agent and expected reserved network matched privately.
Only those named targets were inspected; no LAN sweep or VM107 action.

After exact forward return, cleanup and new-session replay, graceful
`qm shutdown 115 --timeout 120` completed. Proxmox reported `status: stopped`.
The command's forceStop default is 0 and no force-stop was used. `qm start 115`
then completed; running status, guest agent, exact network identity and SSH listener
recovered. VM configs and network identity matched pre-stop digests. No host reboot,
firewall VM mutation or VM resource/configuration change.

Guest SSH post-readback verified the actual boot ID changed (kept private), expected
data mount, PostgreSQL, API, Caddy/trusted TLS, UFW/listener contract, required
enabled/active timers/units, all 13 normal health checks and zero failed units.
Exact repaired release, schema 0016, generation 1/28,278 sets and cleanup state
survived. [Guest recovery](cold-recovery.json) and [validation](validation.json).
