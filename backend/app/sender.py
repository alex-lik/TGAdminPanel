import httpx
import anyio

publisher_url: str = "http://10.0.15.4:8012/publish"

async def send_to_publisher_async(
    token: str,
    chat_id: str,
    parse_mode: str,
    text: str = None,
    caption: str = None,
    image_path: str = None,
) -> int:
    data = {
        "token": token,
        "chat_id": chat_id,
        "parse_mode": parse_mode,
        "text": text,
        "caption": caption,
    }
    files = None
    if image_path:
        files = {"image": open(image_path, "rb")}
    async with httpx.AsyncClient() as client:
        response = await client.post(publisher_url, data=data, files=files)
        response.raise_for_status()
        return response.json()["message_id"]

def send_to_publisher(*args, **kwargs):
    # Синхронная обёртка для вызова из Celery (используется anyio)
    return anyio.run(send_to_publisher_async, *args, **kwargs)
