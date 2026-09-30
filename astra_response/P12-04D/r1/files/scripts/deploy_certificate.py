"""Install only the approved, trusted Certbot lineage and safely reload Caddy.

Executed as root by Certbot's deploy hook. No credentials appear in arguments,
output or persistent adapted Caddy JSON. Old certificate generations are retained.
"""

import hashlib
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

HOST = "appraisal.abrianbaker.com"
LINEAGE = Path("/etc/letsencrypt/live") / HOST
ARCHIVE = Path("/etc/letsencrypt/archive") / HOST
DESTINATION = Path("/etc/caddy/brickvault-tls")
CADDY_ENV = Path("/etc/caddy/brickvault.env")
GENERATION = re.compile(r"cert-[a-f0-9]{64}\Z")


class CertificateError(RuntimeError):
    """Safe error category, with no underlying command output."""


def run(arguments: list[str], *, environment: dict[str, str] | None = None) -> bytes:
    result = subprocess.run(
        arguments, env=environment, capture_output=True, check=False, timeout=60
    )
    if result.returncode:
        raise CertificateError("Certificate command failed; private details withheld.")
    return result.stdout


def safe_parents(path: Path) -> None:
    for parent in (path.parent, *path.parent.parents):
        info = parent.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
            raise CertificateError("Unsafe protected directory.")


def read_protected(path: Path, *, private: bool = False) -> bytes:
    safe_parents(path)
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        info = os.fstat(descriptor)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_uid != 0
            or info.st_nlink != 1
            or info.st_mode & (0o077 if private else 0o022)
            or info.st_size > 65536
        ):
            raise CertificateError("Unsafe certificate input.")
        with os.fdopen(descriptor, "rb", closefd=False) as source:
            return source.read(65537)
    finally:
        os.close(descriptor)


def certificate_inputs(lineage: Path) -> dict[str, bytes]:
    if lineage != LINEAGE:
        raise CertificateError("Unexpected Certbot lineage.")
    files = {}
    paths = {}
    for name in ("cert.pem", "chain.pem", "fullchain.pem", "privkey.pem"):
        path = (lineage / name).resolve(strict=True)
        if path.parent != ARCHIVE:
            raise CertificateError("Certificate input escaped its approved archive.")
        files[name] = read_protected(path, private=name == "privkey.pem")
        paths[name] = str(path)
    if files["fullchain.pem"] != files["cert.pem"] + files["chain.pem"]:
        raise CertificateError("Full chain does not match the verified leaf and chain.")
    run(
        [
            "/usr/bin/openssl",
            "verify",
            "-CAfile",
            "/etc/ssl/certs/ca-certificates.crt",
            "-untrusted",
            paths["chain.pem"],
            "-purpose",
            "sslserver",
            "-verify_hostname",
            HOST,
            paths["cert.pem"],
        ]
    )
    run(
        [
            "/usr/bin/openssl",
            "x509",
            "-in",
            paths["cert.pem"],
            "-checkend",
            "604800",
            "-noout",
        ]
    )
    sans = (
        run(
            [
                "/usr/bin/openssl",
                "x509",
                "-in",
                paths["cert.pem"],
                "-noout",
                "-ext",
                "subjectAltName",
            ]
        )
        .decode("ascii")
        .splitlines()
    )
    if "".join(line.strip() for line in sans[1:]) != "DNS:" + HOST:
        raise CertificateError(
            "Certificate SANs differ from the single approved hostname."
        )
    public = run(
        ["/usr/bin/openssl", "x509", "-in", paths["cert.pem"], "-pubkey", "-noout"]
    )
    key_public = run(
        ["/usr/bin/openssl", "pkey", "-in", paths["privkey.pem"], "-pubout"]
    )
    if public != key_public:
        raise CertificateError("Certificate and private key differ.")
    return {name: files[name] for name in ("fullchain.pem", "privkey.pem")}


def caddy_environment() -> dict[str, str]:
    import grp

    data = read_protected(CADDY_ENV)
    info = CADDY_ENV.stat()
    if (
        info.st_gid != grp.getgrnam("caddy").gr_gid
        or stat.S_IMODE(info.st_mode) != 0o640
    ):
        raise CertificateError("Unsafe Caddy environment permissions.")
    match = re.fullmatch(rb"BVA_PROXY_SHARED_SECRET=([a-f0-9]{64})\n", data)
    if match is None:
        raise CertificateError("Unexpected Caddy environment format.")
    return {
        "PATH": "/usr/bin:/bin",
        "HOME": "/var/lib/caddy",
        "BVA_PROXY_SHARED_SECRET": match[1].decode("ascii"),
    }


def protected_directory(path: Path, group: int) -> None:
    safe_parents(path)
    try:
        path.mkdir(mode=0o700)
    except FileExistsError:
        info = path.lstat()
        if (
            not stat.S_ISDIR(info.st_mode)
            or info.st_uid != 0
            or info.st_gid != group
            or stat.S_IMODE(info.st_mode) != 0o750
        ):
            raise CertificateError("Unsafe certificate destination directory.")
    else:
        os.chown(path, 0, group)
        path.chmod(0o750)


def install(files: dict[str, bytes], group: int) -> bool:
    """Switch one verified certificate pair atomically; restore disk state on failure."""
    protected_directory(DESTINATION, group)
    generation = "cert-" + hashlib.sha256(files["fullchain.pem"]).hexdigest()
    target = DESTINATION / generation
    protected_directory(target, group)
    for name, content in files.items():
        path = target / name
        try:
            descriptor = os.open(
                path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600
            )
        except FileExistsError:
            info = path.lstat()
            if (
                read_protected(path) != content
                or info.st_gid != group
                or stat.S_IMODE(info.st_mode) != 0o640
            ):
                raise CertificateError("Existing certificate generation differs.")
        else:
            with os.fdopen(descriptor, "wb") as output:
                output.write(content)
                output.flush()
                os.fchown(output.fileno(), 0, group)
                os.fchmod(output.fileno(), 0o640)
                os.fsync(output.fileno())
    current = DESTINATION / "current"
    previous = None
    if current.is_symlink():
        previous = os.readlink(current)
        if GENERATION.fullmatch(previous) is None:
            raise CertificateError("Unexpected current certificate target.")
    elif current.exists():
        raise CertificateError("Current certificate pointer is not a symlink.")
    pending = DESTINATION / ".next"
    pending.symlink_to(generation)
    pending.replace(current)
    try:
        run(
            [
                "/usr/sbin/runuser",
                "-u",
                "caddy",
                "--",
                "/usr/bin/caddy",
                "validate",
                "--config",
                "/etc/caddy/Caddyfile",
                "--adapter",
                "caddyfile",
            ],
            environment=caddy_environment(),
        )
        active = (
            subprocess.run(
                ["/usr/bin/systemctl", "is-active", "--quiet", "caddy.service"],
                capture_output=True,
                check=False,
                timeout=10,
            ).returncode
            == 0
        )
        if active:
            run(["/usr/bin/systemctl", "reload", "caddy.service"])
        return active
    except BaseException:
        if previous is None:
            current.unlink()
        else:
            pending.symlink_to(previous)
            pending.replace(current)
        raise


def main() -> int:
    try:
        if os.name != "posix" or os.geteuid() != 0:
            raise CertificateError("Root is required.")
        if os.environ.get("RENEWED_DOMAINS", HOST).split() != [HOST]:
            raise CertificateError("Unexpected renewed domain set.")
        import fcntl
        import grp

        with Path("/run/brickvault-certificate.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            files = certificate_inputs(
                Path(os.environ.get("RENEWED_LINEAGE", str(LINEAGE)))
            )
            active = install(files, grp.getgrnam("caddy").gr_gid)
        print(
            "Trusted certificate installed; Caddy "
            + ("reloaded." if active else "remains stopped.")
        )
        return 0
    except (
        CertificateError,
        OSError,
        ValueError,
        KeyError,
        subprocess.SubprocessError,
    ):
        print(
            "Certificate deployment failed; private details withheld.", file=sys.stderr
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
