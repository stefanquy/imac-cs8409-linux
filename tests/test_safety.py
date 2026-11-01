# SPDX-License-Identifier: GPL-2.0-only
import importlib.util
import contextlib
import io
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('abi', ROOT / 'verify-abi.py')
abi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(abi)

class SafetyTests(unittest.TestCase):
    def test_bitfield_width_changes_are_incompatible(self):
        one = 'unsigned int flag:1; /* 0: 0 4 */\n/* size: 4, members: 1 */'
        two = 'unsigned int flag:2; /* 0: 0 4 */\n/* size: 4, members: 1 */'
        with patch.object(abi, 'run', return_value=one):
            first = abi.layout('unused', 'sample')
        with patch.object(abi, 'run', return_value=two):
            second = abi.layout('unused', 'sample')
        self.assertNotEqual(first, second)

    def test_unparsed_members_fail(self):
        with patch.object(abi, 'run', return_value='/* size: 8, members: 1 */'):
            with self.assertRaises(RuntimeError):
                abi.layout('unused', 'sample')

    def test_offline_kernel_is_rejected(self):
        result = subprocess.run(['python3', str(ROOT/'verify-abi.py'), '--kver',
                                 'not-running', '--module', '/missing'], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'offline', result.stderr)

    def test_missing_candidate_fails(self):
        with patch('sys.argv', ['verify-abi.py', '--kver', os.uname().release,
                                '--module', '/definitely/missing/module.ko']):
            with self.assertRaisesRegex(RuntimeError, 'Candidate module missing'):
                abi.main()

    def test_wrong_vermagic_fails(self):
        with patch('sys.argv', ['verify-abi.py', '--kver', os.uname().release,
                                '--module', str(ROOT/'Kbuild')]), \
             patch.object(abi, 'run', return_value='wrong-kernel SMP'):
            with self.assertRaisesRegex(RuntimeError, 'Kernel version mismatch'):
                abi.main()

    def test_missing_loaded_btf_fails(self):
        with patch('sys.argv', ['verify-abi.py', '--kver', os.uname().release,
                                '--module', str(ROOT/'Kbuild')]), \
             patch.object(abi, 'run', return_value=os.uname().release+' SMP'), \
             patch.object(Path, 'is_file', side_effect=[True, False]):
            with self.assertRaisesRegex(RuntimeError, 'BTF source missing'):
                abi.main()

    def test_layout_mismatch_fails(self):
        with patch('sys.argv', ['verify-abi.py', '--kver', os.uname().release,
                                '--module', str(ROOT/'Kbuild')]), \
             patch.object(abi, 'run', return_value=os.uname().release+' SMP'), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(abi, 'layout', side_effect=[(4, ((0, 4),)), (8, ((0, 8),))]):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(abi.main(), 1)

    def test_unsupported_build_never_calls_make(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            marker = path/'called'
            (path/'make').write_text('#!/bin/sh\ntouch "'+str(marker)+'"\nexit 0\n')
            (path/'make').chmod(0o755)
            result = subprocess.run(['bash', str(ROOT/'dkms-build.sh'), 'unsupported'],
                env={**os.environ, 'PATH':str(path)+':'+os.environ['PATH']}, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(marker.exists(), 'unsupported kernel reached make')

    def test_failed_build_never_runs_verifier(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            marker = path/'verified'
            for name, body in [('uname', 'echo 7.0.0-42-generic'), ('make', 'exit 9'), ('python3', 'touch "'+str(marker)+'"')]:
                (path/name).write_text('#!/bin/sh\n'+body+'\n')
                (path/name).chmod(0o755)
            result = subprocess.run(['bash', str(ROOT/'dkms-build.sh'), '7.0.0-42-generic'],
                env={**os.environ, 'PATH':str(path)+':'+os.environ['PATH']}, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(marker.exists())

    def test_verifier_failure_propagates(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            for name, body in [('uname', 'echo 7.0.0-42-generic'), ('make', 'exit 0'), ('python3', 'exit 2')]:
                (path/name).write_text('#!/bin/sh\n'+body+'\n')
                (path/name).chmod(0o755)
            result = subprocess.run(['bash', str(ROOT/'dkms-build.sh'), '7.0.0-42-generic'],
                env={**os.environ, 'PATH':str(path)+':'+os.environ['PATH']}, capture_output=True)
            self.assertEqual(result.returncode, 2)

if __name__ == '__main__':
    unittest.main()
