# Security review and reporting

Review date: 2026-11-01. Scope: source-only packaging and limited static inspection; not a full kernel-driver security audit.

## Controls

- Curated input: eight C/header files plus the four original build/verifier files. No recursive copy of the original tree; compiled modules, objects, caches and backups were excluded.
- Installation uses a fixed package/version, source-file allowlist, root-owned destination and fixed system PATH. It rejects source symlinks, an existing destination and any existing CS8409 DKMS registration. Use a trusted checkout with no untrusted concurrent writers; checks do not defend against a malicious user changing files during installation.
- The wrappers contain no remote download, network command, secret collection, audio capture, automatic reboot or live module reload. They do not implement their own signing/key management. Delegated DKMS builds may generate local signing keys/certificates by default; never export those materials with source or test logs.
- Build failure and ABI uncertainty propagate as nonzero exit codes. No unchecked binary fallback. Future/offline kernels are refused.
- The component ABI reference is the loaded module's BTF, avoiding an on-disk component that may differ from the running instance.
- Uninstall delegates package-specific removal/restoration to DKMS; it never recursively deletes module directories.
- On the supported iMac18,3, EFI Secure Boot policy accepts only disabled/exit 0 or the exact recognized unsupported message/exit 255, with C locale and both output streams checked together. Enabled, unknown, additional diagnostics and other exit codes are refused. No private keys/certificates are bundled.

## Limits and risks

Kernel drivers execute with kernel privileges and may crash or damage audio hardware if incorrect. Hardware initialization, locking, power management and all driver memory-safety properties have not been comprehensively audited here. The ABI parser covers four structure layouts, not types/names or every kernel interface. A matching layout is necessary for these checks, not sufficient for full safety.

Root installation is not transactional. A failure can leave staged source, a DKMS registration or an installed-on-disk module; review diagnostics and use scoped DKMS removal as appropriate. A reboot is always a separate manual action. Package version 1.33.1 is deliberately unchanged from the working installation; the installer refuses replacement to avoid silently changing that installation.

Source inspection and repository scans check common private-key/credential markers and binary/artifact extensions. No scanner proves absence of every possible secret or malicious code. Git ignores are convenience controls, not publication authorization. Exact immediate derivative provenance has been established. The package-specific older Apple-source concern was resolved by the follow-up comparison; see ATTRIBUTION.md and docs/EGORENKOV-LICENSE-REVIEW.md. This does not replace the technical release tests.

## Reporting

No public security contact has been established. Do not publish sensitive vulnerability details or credentials in a public issue. Establish a private maintainer contact before public release; never post module-signing private keys or full system logs containing personal data.
