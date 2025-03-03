from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        await self.broadcast("New user", _start=1)

    async def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, message: str, _start: int = 0):
        """_start был добавлен, что бы отправитель не получал свое же сообщение"""
        for i, connection in enumerate(self.connections, start=_start):
            if i != len(self.connections):
                await connection.send_text(message)

    @classmethod
    async def send_personal_message(cls, message: str, websocket: WebSocket):
        await websocket.send_text(message)


websockets_manager = ConnectionManager()
