"""
Unit tests for Judge Security and Sandbox Isolation integration.
"""

import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
for p in (BASE_DIR, PROJECT_ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

from security.judge_security.resource_limits import ResourceLimiter
from security.judge_security.privilege_drop import PrivilegeDropper
from security.judge_security.syscall_policy import SyscallPolicy
from security.judge_security.syscall_policy.seccomp_filter import SeccompFilter
from security.judge_security.isolated_runner import IsolatedRunnerHelper
from sandbox.security import SecurityScanner

class TestJudgeSecurity(unittest.TestCase):
    def test_resource_limits_calculation(self):
        limits = ResourceLimiter.get_default_limits(time_limit_sec=2.0, memory_limit_mb=512)
        self.assertEqual(limits['cpu_time_limit_sec'], 2.0)
        self.assertEqual(limits['memory_limit_bytes'], 512 * 1024 * 1024)
        self.assertEqual(limits['max_processes'], 1)
        self.assertEqual(limits['target_uid'], 65534)
        self.assertEqual(limits['target_gid'], 65534)

    def test_syscall_policy_whitelist_and_blacklist(self):
        # Whitelisted I/O and memory
        self.assertTrue(SyscallPolicy.is_syscall_allowed('read'))
        self.assertTrue(SyscallPolicy.is_syscall_allowed('write'))
        self.assertTrue(SyscallPolicy.is_syscall_allowed('mmap'))
        self.assertTrue(SyscallPolicy.is_syscall_allowed('exit_group'))

        # Prohibited dangerous system calls
        self.assertFalse(SyscallPolicy.is_syscall_allowed('socket'))
        self.assertFalse(SyscallPolicy.is_syscall_allowed('connect'))
        self.assertFalse(SyscallPolicy.is_syscall_allowed('clone'))
        self.assertFalse(SyscallPolicy.is_syscall_allowed('fork'))
        self.assertFalse(SyscallPolicy.is_syscall_allowed('execve'))
        self.assertFalse(SyscallPolicy.is_syscall_allowed('ptrace'))
        self.assertFalse(SyscallPolicy.is_syscall_allowed('kill'))

    def test_security_scanner_detects_malicious_cpp(self):
        malicious_cpp = """
        #include <iostream>
        #include <sys/socket.h>
        int main() {
            system("rm -rf /");
            return 0;
        }
        """
        is_safe, violations = SecurityScanner.scan_source("cpp", malicious_cpp)
        self.assertFalse(is_safe)
        self.assertGreater(len(violations), 0)

    def test_security_scanner_detects_malicious_python(self):
        malicious_py = "import os\nos.system('whoami')"
        is_safe, violations = SecurityScanner.scan_source("python", malicious_py)
        self.assertFalse(is_safe)
        self.assertGreater(len(violations), 0)

    def test_security_scanner_allows_clean_algorithm_code(self):
        clean_cpp = """
        #include <iostream>
        #include <vector>
        #include <algorithm>
        using namespace std;
        int main() {
            int a, b;
            if (cin >> a >> b) {
                cout << a + b << endl;
            }
            return 0;
        }
        """
        is_safe, violations = SecurityScanner.scan_source("cpp", clean_cpp)
        self.assertTrue(is_safe)
        self.assertEqual(len(violations), 0)

    def test_isolated_runner_helper(self):
        preexec = IsolatedRunnerHelper.get_preexec_fn(
            time_limit_sec=1.0,
            memory_limit_mb=256
        )
        # On Windows, preexec must be None; on Linux, it must be a callable
        if os.name == 'nt':
            self.assertIsNone(preexec)
        else:
            self.assertTrue(callable(preexec))

if __name__ == '__main__':
    unittest.main()
