#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-2.0-only
set -euo pipefail
KVER="${1:?Kernel version required}"
[[ $# -eq 1 ]] || { echo 'Expected exactly one kernel version' >&2; exit 2; }
[[ "$KVER" == '7.0.0-42-generic' && "$KVER" == "$(uname -r)" ]] || {
    echo 'Unsupported/offline kernel: only active 7.0.0-42-generic is supported' >&2
    exit 2
}
SRC="$(cd -- "$(dirname -- "$0")" && pwd -P)"
make -C "/lib/modules/$KVER/build" M="$SRC" modules
python3 "$SRC/verify-abi.py" --kver "$KVER" --module "$SRC/snd-hda-codec-cs8409.ko"
