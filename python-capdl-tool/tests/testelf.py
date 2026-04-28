#!/usr/bin/env python3
#
# Copyright 2020, Data61, CSIRO (ABN 41 687 119 230)
#
# SPDX-License-Identifier: BSD-2-Clause
#

import unittest
from pathlib import Path

from capdl import ELF
from tests import CapdlTestCase

RESOURCES = Path(__file__).parent / 'resources'


class TestElf(CapdlTestCase):

    def _load(self, name):
        return ELF(str(RESOURCES / name))

    def test_arm_elf(self):
        elf = self._load('arm-hello.bin')
        self.assertIn(elf.get_arch(), [40, 'EM_ARM', 'ARM'])
        elf.get_spec()  # smoke test: must not raise

    def test_ia32_elf(self):
        elf = self._load('ia32-hello.bin')
        self.assertEqual(elf.get_arch(), 'x86')
        elf.get_spec()  # smoke test: must not raise

    def test_symbol_lookup_unstripped(self):
        elf = self._load('unstripped.bin')
        self.assertEqual(elf.get_arch(), 'x86')
        # Address cross-checked against objdump.
        self.assertEqual(elf.get_symbol_vaddr('_start'), 0x08048d48)

    def test_symbol_lookup_stripped_arch(self):
        elf = self._load('stripped.bin')
        self.assertEqual(elf.get_arch(), 'x86')

    def test_symbol_lookup_stripped_raises(self):
        elf = self._load('stripped.bin')
        # Stripped binaries have no symbol table; lookup must fail loudly
        # rather than silently returning a bogus address.
        with self.assertRaises(Exception):  # narrow this — see note below
            elf.get_symbol_vaddr('_start')


if __name__ == '__main__':
    unittest.main()