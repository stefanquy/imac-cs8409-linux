# Apple iMac18,3 CS8409 / CS42L83 Linux audio driver

Source-only packaging of a locally patched Linux HDA driver, driver version **1.33.1**. Intended for Apple iMac18,3 (27-inch 2017) on **x86_64 Ubuntu, active kernel `7.0.0-42-generic`**.

**Experimental source release.** Exact immediate upstream and local patch origin are now documented. The historical Apple-source question was resolved for this package by a full source comparison and the original GPL license history; see [provenance research](docs/PROVENANCE.md), [ATTRIBUTION.md](ATTRIBUTION.md) and the [publication checklist](docs/PUBLICATION.md).

This repository preserves the working C driver behavior and bundled private HDA headers. The sole locally adapted header also carries a dated modification notice. Packaging scripts have changed since the original installation; package version remains 1.33.1. The installer deliberately refuses to overwrite an existing 1.33.1 installation or another registered CS8409 DKMS package. No prebuilt modules or signing material are distributed.

## Compatibility and evidence

| Configuration / feature | Evidence |
| --- | --- |
| iMac18,3, x86_64, kernel 7.0.0-42-generic | User's working configuration; machine identity and running kernel also inspected locally |
| Internal microphone, internal speakers, PipeWire after reboot | User confirmed recording/playback worked in the preceding conversation |
| Original DKMS module | User reported installed at `/lib/modules/7.0.0-42-generic/updates/dkms/snd-hda-codec-cs8409.ko.zst` |
| Targeted ABI checks on existing module | All four checks passed locally |
| This repository's scripts and clean build | See [validation report](docs/VALIDATION.md) |
| Other kernels, iMac models, architectures | Unsupported by this package |
| Headphones/headset mic, HDMI, suspend/resume, hotplug, long-term reliability | Not functionally tested in this packaging session |

Build success and matching four structure layouts do not establish complete ABI compatibility or functional audio correctness.

## Requirements

Use the supported kernel as the **currently running** kernel. Keep its matching headers and a working boot entry. Install dependencies through your trusted Ubuntu package sources:

```bash
sudo apt install build-essential dkms python3 dwarves kmod mokutil linux-headers-$(uname -r)
```

`pahole` is provided by `dwarves` on common Ubuntu configurations; package naming may differ. The stock audio stack must already be loaded, with readable BTF for `vmlinux`, `snd_hda_codec_generic` and `snd_hda_scodec_component` under `/sys/kernel/btf/`. The build must retain debug type information usable by `pahole`.

After the iMac18,3 model check, the installer accepts exactly two EFI results from `LC_ALL=C mokutil --sb-state`: exit 0 with `SecureBoot disabled`, or exit 255 with exactly `This system doesn't support Secure Boot` (the measured mokutil 0.7.2 result on this iMac). The latter may arrive on stdout or stderr. Enabled, empty, unreadable, conflicting or otherwise unknown results stop installation; extra diagnostics and unexpected exit codes are rejected. `check-secure-boot.sh` implements this policy and is included in source staging. Secure Boot signing/enrollment is outside this installer; do not bypass verification or share private signing keys.

Before testing on an already working iMac, read the [script review](docs/SCRIPT-REVIEW.nl.md) and [step-by-step safe iMac test plan (Dutch)](docs/IMAC-TESTPLAN.nl.md). Full install/remove testing requires a separate test installation; the recognized unsupported-firmware prerequisite now passes, while full installation/removal remains untested.

## Check and build without installing

Read the scripts first. Run from a trusted checkout that other users cannot modify concurrently:

```bash
bash install.sh --check
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
bash dkms-build.sh "$(uname -r)"
```

`--check` checks prerequisites only; it does not prove ABI compatibility. The build command writes local build artifacts and runs ABI validation, but does not install or load a module. To keep the repository pristine, build a separate copy. Direct `make` is diagnostic only: it bypasses the packaging verifier and must not be followed by manual installation.

## Install on a fresh, supported system

```bash
sudo bash install.sh
dkms status
modinfo -n snd_hda_codec_cs8409
```

The installer stages a fixed allowlist of files in `/usr/src/snd-hda-codec-cs8409-imac-patched-1.33.1`, then asks DKMS to add, build, verify and install. Verification failure prevents the DKMS build from succeeding. There is no force option, download step, module reload, automatic reboot or fallback to an unchecked binary.

If you already have the working driver, **leave it installed** while reviewing this repository. This installer is not an in-place migration tool. Do not uninstall working audio merely to test packaging.

After successful installation and review, reboot manually. Check `uname -r`, `dkms status`, and `modinfo -n snd_hda_codec_cs8409`. Then test microphone recording and speaker playback at a low volume. No new recording/playback test was performed during repository preparation.

If installation fails, retain the error and inspect `/var/lib/dkms/snd-hda-codec-cs8409-imac-patched/1.33.1/` for DKMS logs. A failed registration/source staging directory may remain for diagnostics; reruns refuse overwrite. Do not use `--force` to defeat this protection.

## ABI verification and kernel updates

The wrapper refuses any target other than the active `7.0.0-42-generic` kernel **before compilation**. The Python verifier additionally checks exact running-kernel identity, module vermagic and these four layouts:

- `hda_multi_out`
- `hda_gen_spec`
- `hda_component`
- `hda_component_parent`

It compares size and ordered member offset/size tuples, including bitfield bit offsets and widths. References come from **loaded** generic/component BTF plus the running kernel BTF base. Missing tools/types/BTF, unparsed members, mismatches and subprocess errors return nonzero. There is no permissive or skip-ABI mode.

This is a targeted layout check, not a complete ABI proof: member names/types, all kernel interfaces and all runtime behavior are not covered. Linux does not provide a stable internal module ABI. The bundled private headers require particular care.

**Offline validation is not implemented.** A DKMS build triggered during installation of a new, not-yet-running kernel will fail. `AUTOINSTALL="yes"` is retained so DKMS attempts remain visible, but it does not mean future kernels are supported. Kernel package configuration may report errors. Do not reboot into a new kernel expecting this patched audio to work. Retain the known working kernel; do not remove it during cleanup. Updating support requires offline ABI design, review and hardware tests, not editing the allowlist alone.

## Uninstall and recovery

**This removes the same package/version as the current working 1.33.1 driver. Do not run it as a test on an installation you intend to preserve. It has no dry-run mode.**

```bash
sudo bash uninstall.sh
dkms status
modinfo -n snd_hda_codec_cs8409
```

This removes only DKMS package `snd-hda-codec-cs8409-imac-patched/1.33.1` across its registered kernels. DKMS handles its recorded original modules. The script does not manually delete stock modules or unload the active driver; it retains the `/usr/src` source directory. Review results before rebooting. Stock audio may lack the microphone fix.

If audio fails after a kernel change, boot the retained working kernel through the boot menu. If a module is absent or DKMS cannot restore the stock module, repair the matching Ubuntu kernel module package using trusted package sources. Never copy a `.ko` from another kernel. Keep a record of the original working DKMS state before any migration.

## License, attribution and security

[LICENSE](LICENSE) contains GNU GPL version 2. The bundled C/header files retain their individual SPDX identifiers: `cs8409-tables.c` is GPL-2.0-only; the other seven files are GPL-2.0-or-later. New packaging files are offered under GPL-2.0-only. The direct upstream is Peter Shev’s imac-sound at commit 08f974ecf409b4a5482fcb5564e776d9db427b6e. Its explicit GPL notice is preserved. The earlier Egorenkov-source concern is closed for this package; see the [scoped license review](docs/EGORENKOV-LICENSE-REVIEW.md).

The immediate source is [Peter Shev’s pinned imac-sound revision](https://github.com/petershevchenko/imac-sound/tree/08f974ecf409b4a5482fcb5564e776d9db427b6e), built on the Linux CS8409 driver family. Seven C/header files exactly match its public Git blobs; the complete difference in the eighth is recorded in [the local patch](patches/0001-local-abi-and-notice.patch). See [attribution](ATTRIBUTION.md), [security review](SECURITY.md), [source hashes](docs/original-source-sha256.json) and [publication checklist](docs/PUBLICATION.md). Publication target: [stefanquy/imac-cs8409-linux](https://github.com/stefanquy/imac-cs8409-linux). Full fresh-system installation/removal and new-build audio validation remain open; see the publication checklist.
