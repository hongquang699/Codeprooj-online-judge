import json
import logging

logger = logging.getLogger('websocket.rating')

class RatingWebSocketHandler:
    user_sockets = {} # { user_id: set(websockets) }

    @classmethod
    def register_user(cls, user_id, websocket):
        if user_id not in cls.user_sockets:
            cls.user_sockets[user_id] = set()
        cls.user_sockets[user_id].add(websocket)

    @classmethod
    def unregister_user(cls, user_id, websocket):
        if user_id in cls.user_sockets:
            cls.user_sockets[user_id].discard(websocket)

    @classmethod
    async def send_rating_change(cls, user_id, rating_data):
        clients = cls.user_sockets.get(user_id, set())
        if not clients:
            return
        payload = json.dumps({
            'type': 'RATING_UPDATE_NOTIFICATION',
            'data': rating_data
        })
        for ws in list(clients):
            try:
                await ws.send(payload)
            except Exception:
                cls.unregister_user(user_id, ws)
