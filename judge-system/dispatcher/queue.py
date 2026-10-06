"""
Submission Queue for Judge System Dispatcher.
Thread-safe priority queue supporting memory and optional Redis backends.
"""

import queue
import time
import threading
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass(order=True)
class PrioritizedJob:
    priority: int  # Lower number = higher priority (e.g. 1 for Contest, 10 for Practice)
    timestamp: float
    job_id: str = field(compare=False)
    data: Dict[str, Any] = field(compare=False)

class SubmissionQueue:
    def __init__(self, backend_type: str = "memory", redis_url: Optional[str] = None):
        self.backend_type = backend_type
        self.redis_url = redis_url
        self._mem_queue = queue.PriorityQueue()
        self._jobs: Dict[str, PrioritizedJob] = {}
        self._lock = threading.RLock()
        self.paused = False

    def push(self, job_id: str, data: dict, priority: int = 10):
        """Pushes a submission job to the priority queue."""
        job = PrioritizedJob(
            priority=priority,
            timestamp=time.time(),
            job_id=job_id,
            data=data
        )
        with self._lock:
            self._jobs[job_id] = job
            self._mem_queue.put(job)

    def pop(self, timeout: Optional[float] = 1.0) -> Optional[dict]:
        """Pops the highest priority job from the queue."""
        if self.paused:
            return None
        try:
            job: PrioritizedJob = self._mem_queue.get(timeout=timeout)
            with self._lock:
                if self.paused:
                    self._mem_queue.put(job)
                    return None
                if self._jobs.pop(job.job_id, None) is None:
                    return None
                return job.data
        except queue.Empty:
            return None

    def size(self) -> int:
        """Returns the number of jobs waiting in queue."""
        with self._lock:
            return len(self._jobs)

    def get_job(self, job_id: str) -> Optional[dict]:
        """Looks up job data by ID."""
        with self._lock:
            job = self._jobs.get(job_id)
            return job.data if job else None

    def list_jobs(self) -> list:
        with self._lock:
            return [dict(job_id=j.job_id, priority=j.priority, submitted_at=j.timestamp,
                         submission_id=j.data.get('submission_id'),
                         problem_code=j.data.get('problem_code'), language=j.data.get('language'))
                    for j in sorted(self._jobs.values())]

    def cancel(self, job_id: str) -> bool:
        with self._lock:
            return self._jobs.pop(job_id, None) is not None
