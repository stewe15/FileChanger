from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import uvicorn
import re

app = FastAPI()
users = {}
recipient_name = ['' for i in range(10)]
resivents = []
file_name = ['' for i in range(10)]

class Us:
    user = ''
    data = ''
    file_name = ''

@app.websocket("/ws/getUsers")
async def getUsers(websocket: WebSocket):
    await websocket.accept()

    try:
        for ws, name in users.items():
            await websocket.send_text(name)
        await websocket.close()
    except WebSocketDisconnect:
        await websocket.close()

global sender_name

global filename
@app.websocket("/ws/getFile")
async def get_file(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    info = data.split('\t')

    sender_name = info[0]

    recipient_name[0] = info[1]

    file_name[0] = info[2]
    await websocket.send_text("Отправлено")



@app.websocket("/ws/fl")
async def get_f(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_bytes()
    res = Us()
    res.user = recipient_name[0]
    res.data = data
    res.file_name = file_name[0]
    resivents.append(res)
@app.websocket("/ws/fl_nm")
async def getFileName(websocket: WebSocket):
    await websocket.accept()
    nm = await websocket.receive_text()
    pat = r'\.\w*'
    for i in range(len(resivents)):
        if nm == resivents[i].user:
            kod = re.findall(pat,resivents[i].file_name)
            otp = 'EF'+kod[0]
            await websocket.send_text(otp)
    await websocket.close()
@app.websocket("/ws/got")
async def got(websocket: WebSocket):
    await websocket.accept()
    nm = await websocket.receive_text()
    for i in range(len(resivents)):
        if nm == resivents[i].user:
            await websocket.send_bytes(resivents[i].data)
            del resivents[i]
    await websocket.close()
@app.websocket("/ws/listen")
async def listen(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    users[websocket] = data
    try:
        await asyncio.sleep(300)
        del users[websocket]
        await websocket.close()
    except WebSocketDisconnect:
        del users[websocket]
        await websocket.close()

