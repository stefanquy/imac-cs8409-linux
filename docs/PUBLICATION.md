# Public-release checklist

This is an experimental source publication. The owner authorized publication to stefanquy/imac-cs8409-linux on 2026-11-01. The unchecked technical items below remain open and are not claimed as passing.

- [x] Curated source-only copy; original driver C/header bytes preserved.
- [x] GPLv2 text and existing file notices preserved.
- [x] Installation, uninstall, ABI limitations and recovery documented.
- [x] Establish exact immediate upstream URL/revision and byte-verify its public Git blobs: see docs/PROVENANCE.md and docs/provenance.json.
- [x] Record Peter Shev’s explicit GPL grant and preserve upstream author/copyright notices verbatim.
- [x] Record the owner’s confirmation that the supplied local 1.33.1 scripts were created in their ChatGPT/Codex sessions.
- [x] Resolve the package-specific Egorenkov Apple-source concern through all-six-header comparison, David Jo’s original license issue and GPLv2 addition, and packaged-data/helper checks. See EGORENKOV-LICENSE-REVIEW.md for the scoped conclusion; this does not create a license grant for the entire historical fork.
- [x] Add a dated notice to the locally modified header, preserve per-file SPDX tags, and record the local project’s GPLv2 packaging terms. Save a reproducible baseline patch.
- [ ] Have the owner review the security report and hardware/support claims.
- [x] Review installer/remover and exercise only non-mutating syntax/unit/refusal checks on the working iMac; see SCRIPT-REVIEW.nl.md.
- [x] Resolve the known mokutil 0.7.2 unsupported result with exact output/exit-255 matching; enabled, diagnostics and unknown results remain rejected. Six new policy tests and the actual non-mutating --check pass. This does not replace the separate install/remove test.
- [ ] Follow IMAC-TESTPLAN.nl.md for a fresh DKMS install/remove on a separately booted, recoverable test system with private module/DKMS/source/boot trees. This was deliberately not done on working audio. Document the retained-source-map reinstall refusal.
- [ ] Test recording/playback using the newly packaged build, then update compatibility evidence. Prior user success refers to the earlier installation.
- [ ] Review `git ls-files` and `git diff --cached` before any commit or upload; inspect history too. Never add keys, credentials, recordings, logs, binaries, object files or backups.
- [ ] Select a maintainer identity/security contact and license notices for new packaging contributions.
- [x] Owner explicitly authorized public publication to stefanquy/imac-cs8409-linux on 2026-11-01. No stable release or completed fresh-system install/remove test is implied.

Keep the known working kernel. Do not advertise automatic future-kernel compatibility or offline ABI verification.
