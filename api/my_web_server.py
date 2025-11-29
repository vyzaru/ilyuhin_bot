from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import asyncio

app = FastAPI(title="Telegram Mini App")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="webapp"), name="static")

# WebSocket для реального времени
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Обрабатываем данные от клиента
            await websocket.send_text(f"Server received: {data}")
    except Exception as e:
        print(f"WebSocket error: {e}")

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def serve_web_app():
    with open("webapp/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# API endpoints
@app.post("/api/telegram-data")
async def receive_telegram_data(request: Request):
    """Получаем данные из Telegram Web App"""
    data = await request.json()
    print("📨 Данные от Telegram:", data)
    
    # Здесь можно обработать данные и отправить в бота
    return JSONResponse({
        "status": "success",
        "message": "Data received",
        "data": data
    })

@app.get("/api/user/{user_id}")
async def get_user_info(user_id: int):
    """Пример API для получения информации о пользователе"""
    return {
        "user_id": user_id,
        "name": "Test User",
        "premium": False
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Telegram Web App"}

if __name__ == "__main__":
    ssl_config = {
        "ssl_keyfile": "localhost+2-key.pem",
        "ssl_certfile": "localhost+2.pem"
    }
    
    print("🚀 Запуск FastAPI с SSL...")
    print("📱 Web App доступен: https://localhost:8443")
    print("🔧 API документация: https://localhost:8443/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",  # Доступ с других устройств в сети
        port=8443,
        **ssl_config
    )