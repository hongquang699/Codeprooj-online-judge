"""
Testcase Loader for Judge System.
Loads input and expected output testcases from disk or problem package directory.
"""

import os
import glob
import re
from typing import List
from .subtask import TestCaseInfo

class TestcaseLoader:
    @staticmethod
    def load_from_directory(problem_dir: str) -> List[TestCaseInfo]:
        """
        Loads testcases from a directory containing .in and .out / .ans files.
        Looks in 'cases/', 'testcases/', or directly in problem_dir.
        """
        cases_dir = problem_dir
        for sub in ["cases", "testcases", "tests"]:
            candidate = os.path.join(problem_dir, sub)
            if os.path.isdir(candidate):
                cases_dir = candidate
                break

        if not os.path.exists(cases_dir):
            return []

        # Find all .in files
        in_files = glob.glob(os.path.join(cases_dir, "*.in"))
        
        # Natural sort
        def natural_keys(text):
            return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', text)]

        in_files.sort(key=natural_keys)

        testcases: List[TestCaseInfo] = []
        for idx, in_path in enumerate(in_files, start=1):
            base_name = os.path.splitext(in_path)[0]
            
            # Check for matching .out or .ans
            out_path = base_name + ".out"
            if not os.path.exists(out_path):
                out_path = base_name + ".ans"
            
            if not os.path.exists(out_path):
                continue

            try:
                with open(in_path, "r", encoding="utf-8", errors="replace") as f:
                    in_data = f.read()
                with open(out_path, "r", encoding="utf-8", errors="replace") as f:
                    out_data = f.read()
            except Exception:
                continue

            case_name = os.path.basename(base_name)
            
            # Detect subtask from name if patterned: subtask1_case01 or s1_01
            subtask_id = 1
            m = re.search(r'(?:subtask|s|st)[_-]?(\d+)', case_name, re.IGNORECASE)
            if m:
                subtask_id = int(m.group(1))

            testcases.append(TestCaseInfo(
                id=idx,
                name=case_name,
                input_data=in_data,
                expected_output=out_data,
                subtask_id=subtask_id,
                points=10.0
            ))

        return testcases
