# Egorenkov Apple-code license review — 2026-11-01

## Decision for this package

**Close the specific historical-source/license-origin blocker for the packaged driver on a GPL version 2 distribution basis.** The earlier warning was based on missing license markers in six older headers before their contents had been fully compared. The deeper comparison accounts for all six headers, identifies the actual earlier implementation and its explicit GPL license, and finds no unexplained substantial Apple implementation introduced in an unmarked Egorenkov header.

This is a source-provenance assessment for the files actually shipped here. It does not create a license grant for the whole Egorenkov repository, claim that GitHub metadata grants rights, or claim that every historical revision was explicitly licensed in 2022. Keep the full GPLv2 text and all original notices. The remaining release tasks are technical installation/runtime validation and owner publication approval.

## 1. The earlier implementation has an explicit GPL license

The original license question is public: [davidjo/snd_hda_macbookpro issue 126, “Missing license”](https://github.com/davidjo/snd_hda_macbookpro/issues/126). The discussion distinguishes the Cirrus SPDX notices from David Jo's Apple work and asks for a repository license.

The repository then added the GPLv2 LICENSE in [commit 259cc39e243daef170f145ba87ad134239b5967f](https://github.com/davidjo/snd_hda_macbookpro/commit/259cc39e243daef170f145ba87ad134239b5967f), dated 2024-06-16, with the message “Added license file as requested.” The issue was closed as completed. The commit records its author display name as Src User, without a linked GitHub author account in the fetched response; this report does not invent a personal identity for that author. The maintainer davidjo participates in the linked license discussion. The [LICENSE at that exact commit](https://github.com/davidjo/snd_hda_macbookpro/blob/259cc39e243daef170f145ba87ad134239b5967f/LICENSE) is GPL version 2, Git blob 31bf790b7eb0b985889e6b9ce854d310ab02d00a.

The GPL2024 source tree still contains the Apple implementation and register programming routines. This is a concrete earlier-source grant, rather than relying on another fork's description or MODULE_LICENSE metadata. No assumption of a new standalone permission from Egorenkov is needed for David Jo's implementation as found in that licensed source.

## 2. Complete comparison of the six unmarked Egorenkov headers

Compared every Apple-specific header added by [Egorenkov's sole Apple-support commit d8c9001418e6172099a0907f022534f152e29d71](https://github.com/egorenar/snd-hda-codec-cs8409/commit/d8c9001418e6172099a0907f022534f152e29d71) against [David Jo's earlier 18f0201b67d1d50f99526453e833f585b5b28321 tree](https://github.com/davidjo/snd_hda_macbookpro/tree/18f0201b67d1d50f99526453e833f585b5b28321), dated 2022-05-18.

| Egorenkov header | Complete non-whitespace difference from earlier David Jo file |
| --- | --- |
| patch_cirrus_boot84.h | None; identical Git blob |
| patch_cirrus_real84.h | None; identical Git blob |
| patch_cirrus_real84_i2c.h | None; identical Git blob |
| patch_cirrus_apple.h | Removes one force_status_change initializer |
| patch_cirrus_new84.h | Adds one break in get_hda_cvt_setup_apple_8409 |
| patch_cirrus_hda_generic_copy.h | Adds a default mixer access flag and a snprintf length/error guard |

There is no additional multi-function Apple implementation hidden among these differences. All nonblank changes, original/public blob IDs and SHA-256 values are recorded in [egorenar-license-evidence.json](egorenar-license-evidence.json). Whitespace-only differences were classified separately; comments and statements were not silently removed before comparing.

Egorenkov also modified patch_cs8409.c and patch_cs8409.h, whose explicit GPL-2.0-or-later SPDX notices remained in place. His integration Makefile is not used here: this package's Kbuild is derived from Peter Shev's explicitly licensed tree. Signed-off-by is retained as authorship/history evidence, not treated as a substitute license.

## 3. Check relevance to the packaged implementation

None of the six legacy headers is shipped or included by this package. The changed legacy routines get_hda_cvt_setup_apple_8409, add_control and add_control_with_pfx are not defined in the packaged C/header source; force_status_change is also absent. Peter's implementation uses the modern kernel generic-codec interfaces instead of importing those legacy helper files.

As further corroboration, both mixer-helper changes can be found in explicitly [GPL-2.0-or-later Linux hda_generic.c at f155f3b3ed1af23884ffaffe8a669722b87ac9d6](https://github.com/torvalds/linux/blob/f155f3b3ed1af23884ffaffe8a669722b87ac9d6/sound/pci/hda/hda_generic.c). That 2023 source is evidence of the licensed helper implementation, not proof of where a 2022 edit was copied from. These helpers are not bundled here in either case. The isolated break and deletion are not a separate shipped Apple implementation block; no legal conclusion about the copyrightability of a single statement is required for this exclusion.

The packaged CS42L83 initialization table contains **61 register/value entries**. Every pair is present in vendor-write call text in the Apple/boot/real/i2c source files of David Jo's **GPL2024 snapshot**: 59 have uncommented call references and two (0x1209/0x01 and 0x2001/0x01) have only commented-out call references. Both kinds identify published register data; they do not establish what that version executes. [The per-entry references](egorenar-license-evidence.json) record source paths and line numbers. Matching register/value pairs corroborates data provenance; it does not prove ordering, control flow, independent authorship or that every hardware constant is copyrightable. The conclusion therefore does not depend on simply declaring all reverse-engineered data public domain.

The actual packaged C/header implementation remains the previously verified Peter Shev v1.33 baseline plus the documented one-field local ABI adaptation and dated comment. Peter's explicit GPL notice is retained in UPSTREAM-COPYRIGHT. Local packaging origin was confirmed by the owner in this chat.

## 4. Scope and publication conditions

The specific concern was an unidentified, possibly unlicensed substantial Apple implementation by Egorenkov surviving in this package. The exhaustive six-header comparison and explicitly licensed earlier corpus now account for that material. Accordingly the specific source-origin blocker is closed for this package; the old blanket “unresolved Egorenkov license” release warning is superseded by this report.

This conclusion does not independently certify every copyright contributor's title, confer a license on an unshipped historical file, or authorize a public push. Use GPLv2 as the common distribution basis; do not infer that all historical material can be relicensed GPLv3 merely from GPL-2.0-or-later markers elsewhere. Preserve existing file markers, original notices, the full license text and local dated-change notices.

No maintainers were contacted. No issue, email, pull request or public repository was created. No driver source or runtime behavior changed in this follow-up. Fresh DKMS install/remove and new-build audio tests remain open in PUBLICATION.md, and public publication still requires the owner's explicit approval.
