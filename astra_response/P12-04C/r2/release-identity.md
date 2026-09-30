# Installed immutable release

| Item | Value |
|---|---|
| Release | p12-04c-r4 |
| Base main HEAD | 5b0fc9919d6755d1414527c27592b7df1068c96d |
| Reviewed source ID | 6c0ca52d142b2018c2a4b7a72342705196e1cb72e883cb352e91a3f167cb6536 |
| Manifest SHA-256 | 980b7d9894eeee745bd8c7e8222714790f8ac6a56e7812d1d0c6d9fd29ae96a8 |
| Wheel SHA-256 | 02dc2675632ffc72ffd11a797aab11b52fee5820b5966bc582864baf9ce8fc97 |
| Locked requirements SHA-256 | 26b6b014320a29683278a4248bee4918df94b3dd3b53251b48172d29bfeaee03 |
| Transport archive SHA-256 | e4614003566fef2a8d200e7776310547bbdc56429251590c13fca2cba96419ba |
| Backup service SHA-256 | 69f868c85113ea3ea340c4fcd204374863148d3060c5d2a6dec4e9ff5bbb33e4 |

The source identity includes the corrected backup module, focused tests and service definition. Local packaging verified wheel/source equality, the frontend, dependency lock, independent installed-wheel import and migration graph. The VM verified transferred artifacts, installed hash-locked dependencies, admin/backup entrypoints and the exact packaged head. The installed backup module bytes matched the wheel.

`/opt/brickvault/current` was atomically moved to `/opt/brickvault/releases/p12-04c-r4`. The r3 release remains intact. The API stayed disabled/inactive. The service definition passed systemd verification; its effective NoNewPrivileges and RestrictSUIDSGID properties are both true.
