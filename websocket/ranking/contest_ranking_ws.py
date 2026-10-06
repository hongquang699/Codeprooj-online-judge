import json
import logging

logger = logging.getLogger('websocket.contest_ranking')

class ContestRankingWebSocketHandler:
    """
    Handles live updates to contest scoreboard grid.
    Flow:
      Submission -> Judge -> Result (AC/WA) -> ScoreCalculator -> Broadcast Scoreboard Row Update
    """
    contest_rooms = {} # { contest_id: set(websockets) }

    @classmethod
    def join_contest(cls, contest_id, websocket):
        if contest_id not in cls.contest_rooms:
            cls.contest_rooms[contest_id] = set()
        cls.contest_rooms[contest_id].add(websocket)
        logger.info(f"Client joined contest scoreboard room: {contest_id}")

    @classmethod
    def leave_contest(cls, contest_id, websocket):
        if contest_id in cls.contest_rooms:
            cls.contest_rooms[contest_id].discard(websocket)

    @classmethod
    async def broadcast_contest_submission_update(cls, contest_id, row_data):
        clients = cls.contest_rooms.get(contest_id, set())
        if not clients:
            return
        payload = json.dumps({
            'type': 'SCOREBOARD_ROW_UPDATE',
            'contest_id': contest_id,
            'row': row_data
        })
        for ws in list(clients):
            try:
                await ws.send(payload)
            except Exception:
                cls.leave_contest(contest_id, ws)
