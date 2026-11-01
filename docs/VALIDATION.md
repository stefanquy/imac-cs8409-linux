# Validation report — 2026-11-01

## Passed

- Initial preparation copied eight C/header files byte-for-byte from the working snapshot. During provenance research a dated comment notice was added to common/hda_local.h; its declaration content is unchanged. The other seven files still match the original snapshot and the pinned public upstream exactly.
- Ten Python unittest tests cover offline kernels, unsupported-build refusal before make, missing candidates/BTF, wrong vermagic, malformed structures, changed bitfield widths, mismatched layouts, failed compilation and failed verification propagation. Dependency stubs avoid actual installation/build side effects in these unit tests.
- The bitfield-width and pre-build unsupported-kernel tests were observed failing against the original scripts, then passing after the fixes.
- Bash syntax validation of install.sh, uninstall.sh and dkms-build.sh passed.
- A clean build from a disposable source copy succeeded on the active 7.0.0-42-generic kernel. No existing .o/.ko was copied into that build.
- The new verifier passed against both the original working module and the newly compiled module: hda_multi_out 104 bytes; hda_gen_spec 6008 bytes; hda_component 112 bytes; hda_component_parent 488 bytes.
- Source-only tree inspection and common secret-marker checks found no private signing key, credential, ELF module/object, cache or build artifact in the deliverable. The manifest contains hashes, not binary payloads.

A fresh-context read-only review found no new important security defect. Its two minor findings were addressed: build-wrapper tests now stub uname, and the inherited Kbuild dependency comment was corrected. The ten-test suite was rerun after those changes.

## Warnings and deliberate refusals

The compiler emitted a name-difference warning: the kernel recorded x86_64-linux-gnu-gcc while the build used gcc, both reporting Ubuntu 15.2.0-16ubuntu1 / 15.2.0. Build and checks still completed successfully.

The initial staged whitespace check reported three inherited whitespace warnings in common/hda_local.h (original lines 18, 38 and 39). That existing whitespace is preserved; the added comment notice shifts those line numbers. Unified patch context is preserved verbatim too. The check restricted to non-source, non-patch packaging additions passes.

Module BTF generation was skipped because a build-time vmlinux was unavailable. The candidate retained DWARF debug information; pahole read that, and the verifier used the running kernel/module BTF as references. Missing all usable candidate type information would fail verification.

Historical result before the Secure Boot-policy update: `bash install.sh --check` failed closed here: on this EFI environment mokutil reported that Secure Boot is unsupported and returned nonzero. The installer requires an unambiguous successful disabled result. No workaround or permissive fallback was added.

## Not executed / not established

- No privileged installation, DKMS add/build/install/remove, live module replacement, reboot or new audio recording/playback test was performed. Full fresh-system installation/removal testing remains a release checklist item.
- Earlier user-confirmed microphone/speaker/PipeWire success applies to the original working installation, not a runtime test of this newly built module.
- No offline/future-kernel validation or Secure Boot enabled installation was tested or supported.
- No complete ABI proof or full kernel-driver security audit is claimed.
- Exact immediate upstream and local-script origin were subsequently established; see PROVENANCE.md. The specific older Apple-source concern was subsequently resolved for this package; see EGORENKOV-LICENSE-REVIEW.md and its evidence file.

## Reproduce safe checks

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
bash -n install.sh uninstall.sh dkms-build.sh
# In a disposable source copy on the supported running kernel:
bash dkms-build.sh 7.0.0-42-generic
```

Local Git was initialized without a remote. Files are staged for owner review; no identity was invented for a commit. A local initial commit can be made after the owner chooses their author identity. Nothing was uploaded.

## Provenance update verification

Public GitHub blob IDs were checked against the local pinned upstream Git objects; SHA-256 hashes were also recorded. The local header patch was applied to the pinned baseline in a temporary directory and the result matched the packaged header exactly. The original-source manifest remains unchanged as a record of the pre-notice working snapshot. A new clean build/ABI verification and the full ten-test suite were run after adding only licensing/provenance comments to code files.

## Egorenkov license follow-up

Documentation/evidence only; no C/header/build/verifier/script bytes changed in this follow-up. All six historical Apple headers were compared; downloaded source blobs were verified against public Git IDs. The four nonblank change blocks were recorded, and modified legacy helper names/includes were checked absent from packaged code. The earlier GPL2024 source was cross-checked for all 61 initialization register/value entries: 59 have active write-call references and two only commented-out write-call references. The initial stricter active-only check exposed that distinction; the final evidence explicitly records it and makes no runtime-equivalence claim. Existing source hashes and ZIP integrity were checked; no redundant rebuild or hardware test was performed for these documentation-only changes.

## Install/remove script review — 2026-11-01

The ten-test suite and Bash syntax checks passed again. Actual non-mutating probes exercised the installer prerequisite refusal (exit 1), invalid installer arguments (1), invalid uninstaller arguments (2), and the uninstaller's non-root refusal (1). The privileged installation/removal paths were not executed. ShellCheck is unavailable. See SCRIPT-REVIEW.nl.md for partial-failure/reinstall implications and IMAC-TESTPLAN.nl.md for the remaining tests. The installed module path/SHA-256, loaded srcversion and DKMS status were compared before/after and remained equal. No audio was recorded during the review. Script and driver source bytes remain unchanged.

## Secure Boot installer fix — 2026-11-01

Measured mokutil 0.7.2 on this iMac: exit 255, empty stdout, exact unsupported message on stderr. The new standalone policy helper accepts only disabled/0 or that exact unsupported/255 result, combining both streams under LC_ALL=C. The installer calls it only after its existing machine/kernel checks and stages it with the reviewed source allowlist.

Six policy tests exercise disabled, unsupported on either stream, enabled, wrong exit statuses, empty/read errors and conflicting/additional output. The unsupported case and the extra-diagnostic case were observed failing against the extracted original policy, then passing after the fix. All sixteen tests and Bash syntax checks pass. The real installer --check now returns 0 with prerequisites OK. No privileged installer/remover or DKMS mutation was executed. The installed module path/SHA-256, loaded srcversion and DKMS status were compared before/after and remain unchanged. No driver C/header, ABI verifier, build rule or uninstaller behavior changed.
