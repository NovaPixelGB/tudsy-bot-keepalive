# Tudsy bot keepalive

A small GitHub Actions job that logs in through Telethon and interacts with **one exact button** on `@TudsySignalProBot`.

The scheduled workflow is configured for every **5 minutes**, which is GitHub Actions' shortest supported scheduled interval. The schedule is disabled with the `ENABLED` repository variable until credentials and the desired button are configured.

## Secrets (never commit these)

Create these under **Settings → Secrets and variables → Actions → Secrets**:

- `TG_API_HASH` — your Telegram application API hash
- `TG_SESSION` — generated locally with `make_session.py`

Do not put either value in issues, commits, screenshots, or chat messages.

## Variables

The repository uses these Actions variables:

- `TG_API_ID`
- `TARGET_BOT`
- `BUTTON_TEXT`
- `ENABLED`

`BUTTON_TEXT` must exactly match the harmless button you intend to automate, including emoji. The script deliberately does not click arbitrary buttons.

## Generate TG_SESSION locally

```bat
py -m pip install telethon
py make_session.py
```

Telegram may ask for your phone number, login code, and two-step-verification password. Keep all of them private.

## Discover button labels

After the two secrets are set, open **Actions → Tudsy bot interaction → Run workflow**, select `discover`, and run it. The workflow log will list the button labels without clicking anything.

Once `BUTTON_TEXT` is set to the exact intended label and `ENABLED` is `true`, the scheduled job will attempt one matching interaction every five minutes. Telegram rate limits are respected; the script never loops rapidly inside a single run.
