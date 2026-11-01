#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-2.0-only
# Installer policy, 2026-11-01. Caller first checks iMac18,3 and supplies a
# trusted system PATH. No generic nonzero-exit or substring-based exception.
set -euo pipefail
export LC_ALL=C
SB_STATUS=0
SB=$(mokutil --sb-state 2>&1) || SB_STATUS=$?
case "$SB_STATUS:$SB" in
    '0:SecureBoot disabled')
        echo 'Secure Boot: disabled'
        ;;
    "255:This system doesn't support Secure Boot")
        echo 'Secure Boot: unsupported by firmware (recognized mokutil result)'
        ;;
    *)
        echo 'ERROR: Secure Boot enabled, unknown or mokutil failed; refusing installation' >&2
        exit 1
        ;;
esac
