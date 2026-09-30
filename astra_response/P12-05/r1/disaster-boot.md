# VM cold start — UNRUN; startup configuration inspected

Read-only Proxmox configuration confirms firewall VM 112 onboot=1,
startup order=1,up=15 and application VM 115 onboot=1,order=2. VM 115 was running,
its guest agent responded and the expected reserved address matched. This orders
the firewall before the app with a 15-second startup delay; configuration alone
does not prove firewall readiness, actual host reboot, or P12-05 guest cold recovery.
Neither VM nor Proxmox was rebooted or stopped during this blocked run.
