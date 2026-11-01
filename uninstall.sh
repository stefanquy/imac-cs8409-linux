#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-2.0-only
set -euo pipefail
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
export LC_ALL=C
[[ $# -eq 0 ]] || { echo 'Usage: sudo bash uninstall.sh' >&2; exit 2; }
[[ $EUID -eq 0 ]] || { echo 'Run sudo bash uninstall.sh' >&2; exit 1; }
command -v dkms >/dev/null
# Scope is deliberately fixed. Let DKMS restore its recorded original module.
dkms remove -m snd-hda-codec-cs8409-imac-patched -v 1.33.1 --all
depmod -a "$(uname -r)"
echo 'DKMS package removed. No loaded module was unloaded.'
echo 'The source directory under /usr/src is retained for inspection.'
echo 'Review dkms status and modinfo -n snd_hda_codec_cs8409 before rebooting.'
