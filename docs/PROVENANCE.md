# Source and patch provenance — researched 2026-11-01

## Verified immediate upstream

Repository: [petershevchenko/imac-sound](https://github.com/petershevchenko/imac-sound).
Pinned baseline: [`08f974ecf409b4a5482fcb5564e776d9db427b6e`](https://github.com/petershevchenko/imac-sound/commit/08f974ecf409b4a5482fcb5564e776d9db427b6e), 2026-06-30, author Peter Shev. The functional v1.33 change is [`c0b26d4f11c0ed4dea35a799a1d19a4b802fe9b3`](https://github.com/petershevchenko/imac-sound/commit/c0b26d4f11c0ed4dea35a799a1d19a4b802fe9b3).

The baseline was found in a separate local checkout. Crucially, its Git blob IDs were independently checked against the public GitHub tree API at the pinned commit; the remote URL alone was not treated as proof. See provenance.json for the measured hashes.

Seven working-snapshot files match the baseline exactly:

- codecs/cirrus/cs8409.c
- codecs/cirrus/cs8409.h
- codecs/cirrus/cs8409-tables.c
- codecs/generic.h
- codecs/side-codecs/hda_component.h
- common/hda_auto_parser.h
- common/hda_jack.h

The original working Kbuild also exactly matches upstream. Its repository copy now has a license marker and clearer dependency comments, without build-rule changes.

## The one local driver/header patch

The original working common/hda_local.h differs from the pinned baseline by exactly one added declaration, at the end of struct hda_multi_out:

```c
struct snd_kcontrol *share_spdif_kctl;
```

The separate local v1.33 checkout has precisely the same uncommitted one-line change. Its ABI audit report, dated 2026-11-01, records reconstruction of field order/type from the running Ubuntu 7.0.0-42-generic kernel's BTF; it explicitly does not claim byte identity with an unavailable Ubuntu source header. No unknown additional C changes were found.

Independent public corroboration: [armin-haghi/imac-cs8409-linux-audio hda_local.h at b08d0745e1b78d6949d5a231d91351e73ddf8079](https://github.com/armin-haghi/imac-cs8409-linux-audio/blob/b08d0745e1b78d6949d5a231d91351e73ddf8079/hda_local.h) includes the same field and explains the Ubuntu layout mismatch. That header carries GPL-2.0-or-later. Its blob is 1af810e1c371f5c4456535a08f3e487343fe5009. This proves an independently available GPL source for the declaration, not that the local edit was copied from that repository.

The packaged header retains its GPL-2.0-or-later marker and Takashi Iwai notice. It now also carries a dated local modification notice. [patches/0001-local-abi-and-notice.patch](../patches/0001-local-abi-and-notice.patch) reproduces the complete difference from Peter's pinned baseline, including that notice. Applying this patch is not required for normal builds: the checked-in header already contains it.

## Local packaging and verification code

On 2026-11-01 the owner explicitly confirmed in this chat that the supplied 1.33.1 verify-abi.py, dkms-build.sh and dkms.conf were made in their earlier ChatGPT/Codex sessions, rather than copied from a separately identified external source. This is owner testimony, not a public Git history. Their original hashes remain in original-source-sha256.json.

The local ABI-audit script cites armin-haghi's verifier as a reference. The supplied four-structure verifier is a different, shorter implementation; no exact upstream blob match was established. Credit that public verifier for the BTF-checking approach, without claiming that its offline support, implementation or broader checks were imported. The owner-confirmed local files and this preparation's new scripts/tests/documentation use GPL-2.0-only as the project's distribution choice. No personal author identity has been invented.

Preparation changes: refuse unsupported/offline kernels before make; compare bitfield widths; read component reference types from loaded BTF; add guarded install/uninstall scripts and tests. None changes the C driver behavior. No permissive upstream skip-ABI option was imported.

## Licenses and retained notices

The pinned [upstream debian/copyright](https://github.com/petershevchenko/imac-sound/blob/08f974ecf409b4a5482fcb5564e776d9db427b6e/debian/copyright) explicitly names Peter Shev (2024–2026) and Cirrus Logic, offers the work under GPL-2.0-or-later, and records the GPL-2.0-only exception for cs8409-tables.c. A byte-verified unmodified copy is retained as UPSTREAM-COPYRIGHT. Original per-file SPDX and Takashi Iwai notices are retained as well.

Thus the immediate iMac implementation has an explicit GPL grant; it is no longer of unknown upstream origin. GPL version 2 is the common distribution basis for this package; GPL-2.0-or-later notices on individual files remain intact. LICENSE contains the full GPLv2 text, including source-redistribution and dated-modification conditions in sections 1–2. Attribution does not replace compliance with those conditions.

## Earlier lineage: follow-up resolved the package-specific concern

The first research pass identified unmarked Apple headers in Egorenkov's d8c9001418e6172099a0907f022534f152e29d71 tree and left their origins open. A complete follow-up now accounts for all six headers. Three are byte-identical to David Jo's earlier source; the other three differ only by one removed initializer, one extra break, and two small generic mixer-helper adjustments. The changed legacy helper routines are not shipped here. Egorenkov's changes in the main C/header files retain their explicit GPL SPDX notices.

The original “Missing license” discussion was found in [davidjo issue 126](https://github.com/davidjo/snd_hda_macbookpro/issues/126), followed by the project's [2024-06-16 GPLv2 license addition, commit 259cc39e243daef170f145ba87ad134239b5967f](https://github.com/davidjo/snd_hda_macbookpro/commit/259cc39e243daef170f145ba87ad134239b5967f). This is a source with an explicit license covering the earlier implementation, rather than merely another fork's GPL assertion.

All 61 register/value entries of the packaged CS42L83 initialization table also occur in that licensed snapshot's vendor-write call text. Of these, 59 have uncommented call references and two have only commented-out call references. These are data-origin checks, not a runtime/order-equivalence claim.

The [full follow-up report](EGORENKOV-LICENSE-REVIEW.md) and [machine-readable evidence](egorenar-license-evidence.json) record exact blobs, every nonblank delta and per-entry source line references. They supersede the earlier blanket Egorenkov-license warning for this package. No new standalone license grant for all files in the historical Egorenkov repository is asserted; those six legacy headers are not added to this package.

## Release decision

**Established:** exact immediate upstream; Peter's explicit patch license and author notice; all eight working driver/header files accounted for; the sole local ABI change; owner-confirmed local packaging origin; preserved SPDX notices, GPL text, hashes and reproducible patch.

**Specific historical source/license-origin blocker: closed for this package**, based on the exhaustive six-header comparison and the explicit GPL earlier-source corpus. GPL version 2 remains the common distribution basis. See the scoped conclusion in EGORENKOV-LICENSE-REVIEW.md; this is not a new license declaration for the entire old Egorenkov fork.

Fresh DKMS installation/removal and runtime tests of the newly packaged build remain separate technical release checklist items. Public publication still requires explicit owner approval. Nothing has been uploaded, pushed or installed during this investigation.
