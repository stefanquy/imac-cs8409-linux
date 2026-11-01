# SPDX-License-Identifier: GPL-2.0-only
"""Exercise the real policy script with controlled mokutil responses."""
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SecureBootTests(unittest.TestCase):
    def run_policy(self, stdout='', stderr='', status=0):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            stub = path / 'mokutil'
            stub.write_text(
                '#!/bin/sh\n'
                + 'printf %s ' + shlex.quote(stdout) + '\n'
                + 'printf %s ' + shlex.quote(stderr) + ' >&2\n'
                + 'exit ' + str(status) + '\n'
            )
            stub.chmod(0o755)
            return subprocess.run(
                ['bash', str(ROOT / 'check-secure-boot.sh')],
                env={**os.environ, 'PATH': directory + ':' + os.environ['PATH']},
                capture_output=True, text=True,
            )

    def test_successfully_disabled_is_accepted(self):
        self.assertEqual(self.run_policy('SecureBoot disabled\n').returncode, 0)

    def test_exact_unsupported_result_is_accepted_on_either_stream(self):
        for stream in ('stdout', 'stderr'):
            with self.subTest(stream=stream):
                result = self.run_policy(**{
                    stream: "This system doesn't support Secure Boot\n", 'status': 255,
                })
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('unsupported', result.stdout)

    def test_enabled_is_rejected(self):
        for status in (0, 1):
            with self.subTest(status=status):
                self.assertNotEqual(self.run_policy('SecureBoot enabled\n', status=status).returncode, 0)

    def test_unsupported_with_unexpected_exit_status_is_rejected(self):
        for status in (0, 1, 2, 127):
            with self.subTest(status=status):
                self.assertNotEqual(self.run_policy(
                    "This system doesn't support Secure Boot\n", status=status,
                ).returncode, 0)

    def test_disabled_with_tool_error_is_rejected(self):
        self.assertNotEqual(self.run_policy('SecureBoot disabled\n', status=1).returncode, 0)

    def test_unknown_empty_and_conflicting_outputs_are_rejected(self):
        cases = [
            ('', '', 0),
            ('', 'Failed to read EFI variables\n', 1),
            ('Unknown Secure Boot state\n', '', 0),
            ('SecureBoot disabled\n', 'EFI read warning\n', 0),
            ("This system doesn't support Secure Boot\n", 'EFI read warning\n', 255),
            ("SecureBoot enabled\nThis system doesn't support Secure Boot\n", '', 255),
            ("This system doesn't support Secure Boot (maybe)\n", '', 255),
        ]
        for stdout, stderr, status in cases:
            with self.subTest(stdout=stdout, stderr=stderr, status=status):
                self.assertNotEqual(self.run_policy(stdout, stderr, status).returncode, 0)


if __name__ == '__main__':
    unittest.main()
