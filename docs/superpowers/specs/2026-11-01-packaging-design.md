# Approved local packaging design
Package the existing 1.33.1 Apple iMac18,3 CS8409/CS42L83 driver as a source-only local Git repository. Preserve the working C sources and copyright notices. Add conservative DKMS installation and removal scripts, an English README, GPLv2 text, attribution and a security/publication review. Never change the active installation during preparation. Never publish without explicit approval.

Approaches considered: reproduce the existing binary (rejected: artifacts must not ship); generalize to future kernels (deferred: offline ABI validation is absent); package existing source with conservative kernel support (selected and approved in chat).

Support only x86_64 iMac18,3 with active kernel 7.0.0-42-generic. Unknown ABI or offline targets must fail closed. Preserve a fallback kernel. Hardware success is user-reported unless independently exercised. License provenance gaps must remain explicit publication blockers.
