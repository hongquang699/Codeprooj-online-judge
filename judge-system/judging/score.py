"""
Scoring and Aggregation Engine for Judge System.
Calculates overall points, accuracy percentage, and final verdict.
"""

from typing import List, Dict, Any
from .verdict import Verdict

class Scorer:
    @staticmethod
    def calculate_submission_result(
        testcase_results: List[Dict[str, Any]],
        total_problem_points: float = 100.0
    ) -> Dict[str, Any]:
        """
        Aggregates individual testcase results into a final submission outcome.
        """
        if not testcase_results:
            return {
                "verdict": Verdict.SE,
                "score": 0.0,
                "points_earned": 0.0,
                "max_points": total_problem_points,
                "passed_count": 0,
                "total_count": 0,
                "time_ms": 0,
                "memory_kb": 0,
                "message": "No testcases were evaluated."
            }

        total_cases = len(testcase_results)
        passed_cases = sum(1 for r in testcase_results if r.get("verdict") == Verdict.AC)
        
        # Max time and memory across all testcases
        max_time_ms = max(r.get("time_ms", 0) for r in testcase_results)
        max_mem_kb = max(r.get("memory_kb", 0) for r in testcase_results)

        # Points proportional to passed tests if no subtasks
        pts_earned = round((passed_cases / total_cases) * total_problem_points, 2)
        score_percent = round((pts_earned / total_problem_points) * 100.0, 1)

        # Overall verdict
        all_verdicts = [r.get("verdict", Verdict.SE) for r in testcase_results]
        if all(v == Verdict.AC for v in all_verdicts):
            final_verdict = Verdict.AC
        else:
            final_verdict = Verdict.get_worst(all_verdicts)

        return {
            "verdict": final_verdict,
            "score": score_percent,
            "points_earned": pts_earned,
            "max_points": total_problem_points,
            "passed_count": passed_cases,
            "total_count": total_cases,
            "time_ms": max_time_ms,
            "memory_kb": max_mem_kb,
            "testcases": testcase_results
        }
