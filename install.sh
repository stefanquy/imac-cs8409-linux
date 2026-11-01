#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-2.0-only
set -euo pipefail
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
export LC_ALL=C
umask 022
fail() { echo "ERROR: $*" >&2; exit 1; }
[[ $# -eq 0 || ( $# -eq 1 && $1 == --check ) ]] || fail 'Usage: bash install.sh [--check]'
CHECK="${1:-}"
PKG=snd-hda-codec-cs8409-imac-patched
VERSION=1.33.1
KVER=$(uname -r)
SRC=$(cd -- "$(dirname -- "$0")" && pwd -P)
DEST="/usr/src/$PKG-$VERSION"
[[ "$KVER" == 7.0.0-42-generic ]] || fail 'Only active kernel 7.0.0-42-generic is supported; no offline validation'
[[ $(uname -m) == x86_64 ]] || fail 'Only x86_64 is supported'
[[ $(cat /sys/class/dmi/id/product_name) == iMac18,3 ]] || fail 'Only Apple iMac18,3 is supported'
for tool in dkms make gcc python3 pahole modinfo depmod install mokutil; do
    command -v "$tool" >/dev/null || fail "Missing dependency: $tool"
done
[[ -d /lib/modules/$KVER/build ]] || fail 'Matching kernel headers missing'
for btf in vmlinux snd_hda_codec_generic snd_hda_scodec_component; do
    [[ -r /sys/kernel/btf/$btf ]] || fail "Loaded BTF missing: $btf; load the stock audio stack first"
done
if [[ -d /sys/firmware/efi ]]; then
    [[ -f "$SRC/check-secure-boot.sh" && ! -L "$SRC/check-secure-boot.sh" ]] || fail 'Missing/unsafe Secure Boot policy script'
    bash "$SRC/check-secure-boot.sh" || fail 'Secure Boot check rejected this system'
fi
FILES=(Kbuild dkms.conf dkms-build.sh verify-abi.py check-secure-boot.sh
       codecs/generic.h codecs/side-codecs/hda_component.h
       codecs/cirrus/cs8409.c codecs/cirrus/cs8409.h codecs/cirrus/cs8409-tables.c
       common/hda_local.h common/hda_jack.h common/hda_auto_parser.h)
for directory in codecs codecs/side-codecs codecs/cirrus common; do
    [[ -d "$SRC/$directory" && ! -L "$SRC/$directory" ]] || fail "Symlink/invalid directory: $directory"
done
for file in "${FILES[@]}"; do
    [[ -f "$SRC/$file" && ! -L "$SRC/$file" ]] || fail "Missing/unsafe source: $file"
done
if [[ "$CHECK" == --check ]]; then
    echo 'Prerequisites OK. No build, ABI test or system changes performed.'
    exit 0
fi
[[ $EUID -eq 0 ]] || fail 'Run sudo bash install.sh, or bash install.sh --check'
[[ ! -e "$DEST" && ! -L "$DEST" ]] || fail "Source destination already exists: $DEST; refusing overwrite"
STATUS=$(dkms status) || fail 'Cannot read DKMS status'
if [[ "$STATUS" == *snd-hda-codec-cs8409* ]]; then
    fail 'A CS8409 DKMS package is already registered. Review dkms status and resolve the existing installation first.'
fi
# Only these reviewed files enter the root-owned DKMS source directory.
# Never run this script from a checkout writable by an untrusted concurrent user.
install -d -m 0755 "$DEST"
for file in "${FILES[@]}"; do
    install -D -m 0644 -- "$SRC/$file" "$DEST/$file"
done
# A failure stops here. Preserve diagnostic state; do not replace a failed
# verification with a force-install or an unrelated binary backup.
dkms add -m "$PKG" -v "$VERSION"
dkms build -m "$PKG" -v "$VERSION" -k "$KVER"
dkms install -m "$PKG" -v "$VERSION" -k "$KVER"
depmod -a "$KVER"
SELECTED=$(modinfo -k "$KVER" -n snd_hda_codec_cs8409)
[[ "$SELECTED" == /lib/modules/"$KVER"/updates/dkms/snd-hda-codec-cs8409.ko* ]] || fail "Unexpected selected module: $SELECTED"
echo "Installed on disk: $SELECTED"
echo 'No module was reloaded. Review dkms status, then reboot manually when ready.'
