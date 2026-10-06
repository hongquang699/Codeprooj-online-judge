"""
Testcase Manager for Judge System.
Unified coordinator for fetching, caching, and organizing testcases into subtasks.
"""

import os
from typing import List, Dict
from .loader import TestcaseLoader
from .cache import TestcaseCache
from .subtask import TestCaseInfo, SubtaskInfo

class TestcaseManager:
    def __init__(self, problem_base_dir: str):
        self.problem_base_dir = os.path.abspath(problem_base_dir)
        self.cache = TestcaseCache()

    def get_testcases(self, problem_code: str) -> List[TestCaseInfo]:
        """
        Returns all testcases for a problem, utilizing caching where possible.
        """
        cached = self.cache.get(problem_code)
        if cached is not None:
            return cached

        problem_dir = os.path.join(self.problem_base_dir, problem_code)
        testcases = TestcaseLoader.load_from_directory(problem_dir)
        
        # Also check storage/testcases/{problem_code} if empty
        if not testcases:
            storage_cases = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..", "storage", "testcases", problem_code
            )
            if os.path.exists(storage_cases):
                testcases = TestcaseLoader.load_from_directory(storage_cases)

        self.cache.put(problem_code, testcases)
        return testcases

    def get_subtasks(self, problem_code: str, total_points: float = 100.0) -> List[SubtaskInfo]:
        """
        Organizes testcases into subtasks with proportional points.
        """
        testcases = self.get_testcases(problem_code)
        if not testcases:
            return []

        # Group by subtask_id
        grouped: Dict[int, List[TestCaseInfo]] = {}
        for tc in testcases:
            grouped.setdefault(tc.subtask_id, []).append(tc)

        subtask_list: List[SubtaskInfo] = []
        num_subtasks = len(grouped)
        pts_per_subtask = round(total_points / max(1, num_subtasks), 2)

        for st_id in sorted(grouped.keys()):
            cases = grouped[st_id]
            subtask_list.append(SubtaskInfo(
                subtask_id=st_id,
                points=pts_per_subtask,
                scoring_method="all_or_nothing",
                depends_on=[st_id - 1] if st_id > 1 else [],
                testcases=cases
            ))

        return subtask_list
