# P12-04A runtime sources

| Runtime | Source and integrity | Installed result |
| --- | --- | --- |
| CPython | [Python.org 3.13.15 release](https://www.python.org/downloads/release/python-31315/) source `Python-3.13.15.tar.xz`, SHA-256 `1e66a7945a48390ee4c2a4268a0e4185884059a13c4aab6d148aa208deea4a76`; detached signature verified with release-manager fingerprint `7169605F62C751356D054A26A821E680E5FA6305` using [Python's signing-key guidance](https://www.python.org/downloads/metadata/pgp/). | Built with optimizations and LTO into `/opt/python/3.13.15`; `python3.13` reports 3.13.15 and required SSL, decimal, SQLite, compression, ctypes, and venv modules import. Ubuntu `/usr/bin/python3` remains 3.12. |
| uv | [Astral 0.12.10 release](https://github.com/astral-sh/uv/releases/tag/0.12.10) Linux GNU archive, SHA-256 `173d95a0c32d18c896c46ba6fafbf3cf9c14ab74b033f81b76c883ef492a976b`. | Root-owned `/usr/local/bin/uv`, version 0.12.10. Release installation uses the versioned system interpreter and disables uv-managed Python and Python downloads. |
| PostgreSQL | [Official PGDG Ubuntu Noble repository](https://www.postgresql.org/download/linux/ubuntu/), signed by fingerprint `B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8` ([project key announcement](https://www.postgresql.org/about/news/pgdg-apt-repository-for-debianubuntu-1432/)). | `postgresql-18=18.6-1.pgdg24.04+2`; only major 18 was installed. |

Ubuntu 24.04 does not provide the accepted Python 3.13 runtime as its system default. The Python.org signed-source build satisfies the repository's `>=3.13,<3.14` constraint without replacing Ubuntu's own interpreter. Its security updates require monitoring Python 3.13 releases and rebuilding a verified new source into a new versioned prefix; apt updates alone do not patch this interpreter.

The VM's release venv uses CPython 3.13.15, 26 hash-locked production dependencies exported from the repository's unchanged `uv.lock`, and the reviewed wheel. Dependency installation required hashes, used binary distributions, disabled dependency expansion, and passed `uv pip check`. Caddy, restic, and rclone were not installed in this checkpoint.
