# SPDX-License-Identifier: GPL-2.0-or-later
# Packaging comments updated 2026-11-01; original author notices in docs/UPSTREAM-COPYRIGHT.
# Out-of-tree build of the Cirrus CS8409 HDA codec with Apple iMac18,3 support.
# Private HDA headers are bundled under common/ and codecs/. Matching kernel
# headers, build tools and ABI verification tools are required; see README.md.
ccflags-y += -I$(src)/common

snd-hda-codec-cs8409-y := codecs/cirrus/cs8409.o codecs/cirrus/cs8409-tables.o
obj-m += snd-hda-codec-cs8409.o
