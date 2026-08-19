import base64
import logging
import httpx

logger = logging.getLogger("uvicorn.error")

async def send_marz_sms(phone: str, message: str) -> None:
    """Sends SMS notification using the Marz SMS HTTP API."""
    # if not phone or not settings.MARZ_USER:
    #     logger.warning("Marz SMS skipped: missing phone or API credentials.")
    #     return

    try:
        formatted_phone = phone.replace("+", "").strip()
        payload = {
            "recipient": formatted_phone,
            "message": message
        }

        # credentials = f"{settings.MARZ_USER}:{settings.MARZ_SECRET}"
        # encoded_creds = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        headers = {
            # "Authorization": f"Basic {encoded_creds}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "https://sms.wearemarz.com/api/v1/sms/send",
                json=payload,
                headers=headers
            )
            response.raise_for_status()

        logger.info(f"Marz SMS successfully sent to {formatted_phone}")
    except Exception as e:
        logger.error(f"Marz SMS Failed to {phone}: {str(e)}")