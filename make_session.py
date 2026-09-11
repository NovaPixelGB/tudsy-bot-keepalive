import asyncio
from getpass import getpass

from telethon import TelegramClient
from telethon.sessions import StringSession


def ask_api_id():
    while True:
        value = input("Telegram API ID: ").strip()
        try:
            return int(value)
        except ValueError:
            print("API ID must contain numbers only.")


async def main():
    print("This runs only on your computer and creates a reusable Telegram session string.")
    print("Keep the resulting TG_SESSION private. Do not post it in chat or screenshots.\n")

    api_id = ask_api_id()
    api_hash = getpass("Telegram API hash (hidden): ").strip()

    client = TelegramClient(StringSession(), api_id, api_hash)
    await client.start()
    session = client.session.save()

    print("\nCopy the value below into the GitHub Actions secret named TG_SESSION:\n")
    print(session)
    print("\nKeep this value secret.")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
