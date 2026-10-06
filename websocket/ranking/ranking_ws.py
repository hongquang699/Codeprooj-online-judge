import json
import asyncio
import logging

logger = logging.getLogger('websocket.ranking')

class RankingWebSocketHandler:
    """
    Handles live updates to global ranking & country/school leaderboards.
    Clients subscribe to channel: 'ranking:global' or 'ranking:country:<name>'
    """
    subscriptions = set()

    @classmethod
    def register(cls, websocket):
        cls.subscriptions.add(websocket)
        logger.info(f"Client subscribed to global ranking updates. Active clients: {len(cls.subscriptions)}")

    @classmethod
    def unregister(cls, websocket):
        cls.subscriptions.discard(websocket)

    @classmethod
    async def broadcast_rank_update(cls, update_data):
        """
        Broadcasts top rank shifts when a participant finishes a problem or ratings update.
        """
        if not cls.subscriptions:
            return
        payload = json.dumps({
            'type': 'GLOBAL_RANKING_UPDATE',
            'data': update_data
        })
        for ws in list(cls.subscriptions):
            try:
                await ws.send(payload)
            except Exception:
                cls.unregister(ws)
