#!/usr/bin/env python3
import argparse
import random
import sys
import os
from datetime import datetime, timedelta, timezone
from urllib import request
import json

ARCHITECTURES = ["amd64", "arm64", "loongarch64"]

PACKAGE_NAMES = [
    "bash",
    "binutils",
    "clang",
    "cmake",
    "coreutils",
    "curl",
    "dbus",
    "diffutils",
    "elfutils",
    "ffmpeg",
    "findutils",
    "gawk",
    "gcc",
    "gdb",
    "glibc",
    "gmp",
    "gnupg",
    "gnutls",
    "grep",
    "grub",
    "gzip",
    "icu",
    "iproute2",
    "iptables",
    "kernel",
    "less",
    "libcap",
    "libffi",
    "libjpeg-turbo",
    "libpng",
    "libseccomp",
    "libssl",
    "libwebp",
    "libxml2",
    "llvm",
    "lz4",
    "make",
    "mesa",
    "mpfr",
    "ncurses",
    "nss",
    "openssl",
    "pam",
    "patch",
    "pcre2",
    "perl",
    "python",
    "readline",
    "sed",
    "shadow",
    "sqlite",
    "systemd",
    "tar",
    "util-linux",
    "xz",
    "zlib",
    "zstd",
]

FAILURE_REASONS = [
    "configure: error: C compiler cannot create executables",
    "make[2]: *** [Makefile:423: libfoo.so] Error 1",
    "ld: cannot find -lz: No such file or directory",
    "fatal error: sys/capability.h: No such file or directory",
    "CMake Error: The source directory does not appear to contain CMakeLists.txt",
    "ninja: build stopped: subcommand failed",
    "error: use of undeclared identifier '__NR_clone3'",
    "Segmentation fault (core dumped) during test suite",
    "FAILED: tests/unit_test -- exit code 139",
    "timeout: build exceeded 3600 s",
    "checksum mismatch: expected sha256 differs from download",
    "ImportError: No module named '_ssl'",
]


def random_timestamp(rng: random.Random, days_back: int = 90) -> str:
    """Return an ISO-8601 UTC timestamp somewhere in the last `days_back` days."""
    now = datetime.now(timezone.utc)
    delta = timedelta(seconds=rng.randint(0, days_back * 86400))
    return (now - delta).isoformat()


def make_build(rng: random.Random, buildbot: str) -> dict:
    arch = rng.choice(ARCHITECTURES)
    success = rng.random() > 0.20

    return {
        "package_name": rng.choice(PACKAGE_NAMES),
        "success": success,
        "timestamp": random_timestamp(rng),
        "architecture": arch,
        "buildbot": buildbot,
        "failure_reason": None if success else rng.choice(FAILURE_REASONS),
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Seed QAshboard with test build data.")
    p.add_argument(
        "--url",
        default="http://localhost:8000/api/v1",
        help="Base URL of the backend API (default: http://localhost:8000/api/v1)",
    )
    p.add_argument(
        "--count",
        type=int,
        default=514,
        help="Number of build records to generate (default: 514)",
    )
    p.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)",
    )
    p.add_argument(
        "--buildbot",
        "-b",
        type=str,
        required=True,
        help="Buildbot name. You have to create one using CLI first."
        "For more information: `docker compose exec backend qbcli buildbot --help`",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    endpoint = f"{args.url.rstrip('/')}/builds"
    buildbot = args.buildbot

    print(f"Target  : {endpoint}")
    print(f"Records : {args.count}")
    print(f"Seed    : {args.seed}")
    print(f"Buildbot: {buildbot}")
    print()

    buildbot_token = os.getenv("BUILDBOT_TOKEN")
    if not buildbot_token:
        raise RuntimeError("BUILDBOT_TOKEN is not set")

    for i in range(1, args.count + 1):
        payload = make_build(rng, buildbot)
        try:
            req = request.Request(
                endpoint,
                data=json.dumps(payload).encode("UTF-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {buildbot_token}",
                },
                method="POST",
            )
            resp = request.urlopen(req)
            print(resp.status, json.load(resp)["package_name"])

        except Exception as e:
            print(
                payload["package_name"],
                e,
                file=sys.stderr,
            )


if __name__ == "__main__":
    main()
