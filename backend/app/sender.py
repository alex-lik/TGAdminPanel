import httpx
publisher_url: str = "http://10.0.15.4:8012/publish"

async def send_to_publisher(
    token: str,
    chat_id: str,
    parse_mode: str,
    text: str = None,
    caption: str = None,
    image_path: str = None,
) -> int:
    """
    Отправляет данные на сервис-отправщик и возвращает message_id.
    """
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


async def get_message_status(publisher_url: str, message_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{publisher_url}/status/{message_id}")
        r.raise_for_status()
        return r.json()