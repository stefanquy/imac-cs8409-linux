# Attribution and licensing

Exact immediate source: [petershevchenko/imac-sound, commit 08f974ecf409b4a5482fcb5564e776d9db427b6e](https://github.com/petershevchenko/imac-sound/tree/08f974ecf409b4a5482fcb5564e776d9db427b6e), including Peter Shev's v1.33 implementation. Seven C/header files are exact copies; common/hda_local.h has one additional ABI field and a dated local notice. See [full provenance](docs/PROVENANCE.md), [hash evidence](docs/provenance.json) and [local patch](patches/0001-local-abi-and-notice.patch).

## Notices preserved

- **Cirrus Logic, Inc. and Cirrus Logic International Semiconductor Ltd., 2021:** CS8409 driver, tables, header and component header.
- **Peter Shev, 2024–2026:** iMac CS42L83/TAS5764 implementation and project changes; the upstream notice/grant is preserved verbatim in [docs/UPSTREAM-COPYRIGHT](docs/UPSTREAM-COPYRIGHT).
- **Takashi Iwai:** common/hda_local.h (2004), common/hda_jack.h (2011), common/hda_auto_parser.h and codecs/generic.h (2012); existing per-file notices retained.
- **Alexander Egorenkov:** integration of David Jo’s earlier Apple implementation; the complete six-header comparison and license evidence are documented below.
- **armin-haghi:** public Ubuntu share_spdif_kctl fix and BTF ABI-checking reference at b08d0745e1b78d6949d5a231d91351e73ddf8079. This is supporting provenance/reference, not the source of the packaged v1.33 C implementation.
- **davidjo/snd_hda_macbookpro contributors:** original Apple reverse engineering and register-programming implementation underlying the older headers, now traced directly through exact blob comparisons. The explicit GPLv2 license addition is commit 259cc39e243daef170f145ba87ad134239b5967f; no direct import of entire legacy headers into this package is asserted.
- **Local project contributions, 2026-11-01:** BTF-based header adaptation and ChatGPT/Codex-assisted packaging, verification and documentation. The owner confirmed the origin of the supplied 1.33.1 scripts; no individual copyright identity was invented.

## Distribution terms

LICENSE contains GNU GPL version 2. cs8409-tables.c is GPL-2.0-only. The other seven driver/header files retain GPL-2.0-or-later. Kbuild originates in Peter's GPL-2.0-or-later tree and retains that license. Local packaging, verifier, shell scripts, tests and documentation are offered under GPL-2.0-only. GPLv2 is the common distribution basis for the package; preserve the individual notices and full license text. Changes to the locally modified header are dated in-file and documented as a patch.

## Historical-license follow-up

The direct Peter Shev fork and all local changes are accounted for. The former question about Egorenkov's six unmarked Apple headers is now resolved for this package by a complete comparison to David Jo's earlier implementation, the explicit GPLv2 source/license history, and checks showing that the altered legacy helpers are not shipped here. See [the detailed decision](docs/EGORENKOV-LICENSE-REVIEW.md) and [hash/delta/source-line evidence](docs/egorenar-license-evidence.json).

This does not license the entire old Egorenkov repository on its maintainers' behalf. Preserve original notices and GPLv2 distribution terms. Technical install/runtime validation and explicit owner approval for publication remain required; no public push has occurred.
