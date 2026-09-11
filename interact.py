import asyncio
import os

from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.sessions import StringSession

TARGET_BOT = os.getenv("TARGET_BOT", "@TudsySignalProBot").strip()
BUTTON_TEXT = os.getenv("BUTTON_TEXT", "").strip()
MODE = os.getenv("MODE", "click").strip().lower()


def required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required configuration: {name}")
    return value


async def get_buttons(client):
    found = []
    async for message in client.iter_messages(TARGET_BOT, limit=25):
        if not message.buttons:
            continue
        for row in message.buttons:
            for button in row:
                text = (button.text or "").strip()
                if text:
                    found.append((message, button, text))
    return found


async def main():
    api_id = int(required("TG_API_ID"))
    api_hash = required("TG_API_HASH")
    session = required("TG_SESSION")

    client = TelegramClient(StringSession(session), api_id, api_hash)
    await client.connect()

    try:
        if not await client.is_user_authorized():
            raise RuntimeError("TG_SESSION is not authorized. Generate a fresh session with make_session.py.")

        me = await client.get_me()
        print(f"Connected as {getattr(me, 'first_name', '')}. Target: {TARGET_BOT}")

        buttons = await get_buttons(client)
        if not buttons:
            print("No buttons found in the target bot's 25 most recent messages.")
            return

        labels = []
        for _, _, text in buttons:
            if text not in labels:
                labels.append(text)
        print("Available button labels:")
        for label in labels:
            print(f" - {label}")

        if MODE == "discover" or not BUTTON_TEXT:
            print("Discovery only; no button was clicked.")
            return

        for message, button, text in buttons:
            if text.casefold() == BUTTON_TEXT.casefold():
                print(f"Clicking exact button {text!r} on message {message.id}.")
                try:
                    result = await button.click()
                    if isinstance(result, str):
                        print("Button returned a URL/string instead of a Telegram callback; no browser was opened.")
                    else:
                        print("Button interaction completed.")
                except FloodWaitError as exc:
                    print(f"Telegram rate limit: wait {exc.seconds} seconds before trying again.")
                return

        print(f"Configured BUTTON_TEXT {BUTTON_TEXT!r} was not found; nothing clicked.")

    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
