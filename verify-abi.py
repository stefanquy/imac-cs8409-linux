#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
# Local ChatGPT/Codex-assisted project contribution; origin confirmed 2026-11-01.
"""Fail-closed ABI layout check for the iMac18,3 CS8409 driver.

Packaging changes, 2026-11-01: compare bitfield widths and use loaded
component BTF instead of an on-disk compressed module. See ATTRIBUTION.md.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

TYPES = {
    "hda_multi_out": "generic",
    "hda_gen_spec": "generic",
    "hda_component": "component",
    "hda_component_parent": "component",
}

def run(command):
    return subprocess.run(
        command, capture_output=True, text=True, check=True
    ).stdout

def layout(path, name, base=None):
    command = ["pahole"]
    if base:
        command.append(f"--btf_base={base}")
    command.extend(["-C", name, str(path)])
    output = run(command)

    size = re.search(r"/\* size: (\d+),", output)
    count = re.search(r"members: (\d+)", output)
    if not size or not count:
        raise RuntimeError(f"Incomplete structure: {name}")

    fields = []
    for line in output.splitlines():
        match = re.search(r";\s*/\*\s*(\d+)\s+(\d+)\s*\*/", line)
        if match:
            fields.append((int(match.group(1)), int(match.group(2))))
            continue
        bitfield = re.search(r":\s*(\d+);\s*/\*\s*(\d+):\s*(\d+)\s+(\d+)\s*\*/", line)
        if bitfield:
            fields.append(tuple(int(bitfield.group(i)) for i in (2, 3, 4, 1)))

    if len(fields) != int(count.group(1)):
        raise RuntimeError(
            f"Unparsed members: {name} ({len(fields)}/{count.group(1)})"
        )
    return (int(size.group(1)), tuple(fields))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kver", required=True)
    parser.add_argument("--module", required=True)
    args = parser.parse_args()

    if args.kver != os.uname().release:
        raise RuntimeError(
            "UNKNOWN: offline kernel BTF verification not implemented"
        )

    candidate = Path(args.module).resolve()
    if not candidate.is_file():
        raise RuntimeError("Candidate module missing")

    if not run(["modinfo", "-F", "vermagic", str(candidate)]).startswith(
        args.kver + " "
    ):
        raise RuntimeError("Kernel version mismatch")

    base = Path("/sys/kernel/btf/vmlinux")
    generic = Path("/sys/kernel/btf/snd_hda_codec_generic")

    # Compare against the loaded component, not a disk file that could differ
    # from the module actually running. Missing loaded BTF is an unknown result.
    component = Path("/sys/kernel/btf/snd_hda_scodec_component")
    if not all(p.is_file() for p in (base, generic, component)):
        raise RuntimeError("Required loaded kernel/module BTF source missing")

    for name, source in TYPES.items():
        reference = generic if source == "generic" else component
        actual = layout(candidate, name)
        expected = layout(reference, name, base)
        if actual != expected:
            print(f"FAIL: {name} layout mismatch")
            return 1
        print(f"PASS: {name} ({actual[0]} bytes)")

    print("PASS: all required targeted layout checks")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"UNKNOWN / FAIL CLOSED: {exc}", file=sys.stderr)
        sys.exit(2)
