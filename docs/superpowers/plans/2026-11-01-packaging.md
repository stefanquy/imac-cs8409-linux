# Driver Packaging Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Prepare a clean, reviewable local source repository without changing installed audio.
**Architecture:** Curated source allowlist; conservative DKMS wrapper and separate install/remove scripts; tests exercise refusal paths without privilege.
**Tech Stack:** C/Kbuild, Bash, Python unittest, Git.
**Spec:** ../specs/2026-11-01-packaging-design.md

## Global Constraints
- Keep version 1.33.1 and driver C/header content unchanged.
- No public push, secrets, keys, binaries or build artifacts.
- Only active 7.0.0-42-generic / x86_64 / iMac18,3 supported.
- ABI uncertainty must stop installation; no offline bypass.

## Review Focus
- Existing DKMS registration: refuse overwrite.
- Offline kernel or unsupported machine: refuse before mutation.
- Missing BTF/tool or malformed pahole output: nonzero verification.
- Root source staging: explicit files, reject symlinks, no recursive arbitrary copy.
- Uninstall: remove only this package/version; no unrelated module deletion.

## Task 1: Curated snapshot and provenance
- [x] Copy only Kbuild, dkms.conf, dkms-build.sh, verify-abi.py and eight C/header files.
- [x] Record source hashes, license identifiers and unresolved patch provenance.
- [x] Add GPLv2 text, ignores and publication checklist.

## Task 2: Safe packaging behavior
- [x] Write tests for unsupported kernels, build failure, ABI failure and malformed layout.
- [x] Observe expected failures for new guards before implementing them.
- [x] Add conservative build guard, live BTF references and bitfield width comparison.
- [x] Implement guarded install/remove scripts; syntax-check and test refusal paths.

## Task 3: Documentation and validation
- [x] Document dependencies, install/remove/recovery, reported compatibility and offline limitations.
- [x] Run all tests and clean build + ABI verification in a disposable workspace copy.
- [x] Review security and tracked files; initialize local Git without a remote.
- [x] Deliver source-only archive and repository with honest test evidence and publication blockers.

## Execution record
All packaging tasks completed locally. Provenance review recorded unresolved licensing as a public-release blocker rather than inventing missing authorship. Existing installation was untouched. No commit identity was supplied, so the repository is staged without a commit or remote.

Final fresh-context review found no important new defect. Both minor findings were addressed: make wrapper tests independent of the host kernel, and correct the inherited Kbuild dependency comment. Full suite rerun after fixes.

Provenance follow-up, 2026-11-01: pinned immediate upstream identified and public blobs verified; local script origin confirmed by owner. Only comment/license notices were added to code files; common/hda_local.h now includes a dated modification notice. Earlier blanket provenance uncertainty was replaced with the specific historical Apple-sequence license-scope question in docs/PROVENANCE.md.

Historical-license follow-up, 2026-11-01: exhaustive comparison of all six Egorenkov Apple headers, the original David Jo license issue/commit, and all 61 initialization register/value references now support closing the package-specific origin blocker. Earlier execution-record warnings above are historical and superseded by docs/EGORENKOV-LICENSE-REVIEW.md. No source-code bytes changed in this final follow-up.

Install/remove follow-up, 2026-11-01: syntax, ten unit tests and four non-mutating refusal checks passed. No privileged install/remove was run. Script findings and a Dutch staged test plan were added without changing driver/scripts; firmware prerequisite handling and isolated fresh-system tests remain open.

Secure Boot follow-up, 2026-11-01 (explicitly requested): factor the existing EFI check into check-secure-boot.sh, accept only measured exact unsupported/255 or disabled/0, retain all other refusals. Tests observed RED against extracted original behavior, then GREEN (16 total); real --check passes. Existing installation unchanged; no privileged install/remove or push. This supersedes the earlier firmware-prerequisite blocker.
