# TeleReddit Mini-App

Learning project combining a Telegram bot, API and React mini-app.

Solo-developed by [Vojislav Beric](https://github.com/Goodworkid0).

## What it does

- FastAPI/aiogram bot and API experiment.
- React/TypeScript Telegram mini-app interface.
- Telegram authentication and webhook examples.

## Stack

Python · FastAPI · aiogram · React · TypeScript · Vite

## Getting started

The backend uses Poetry and Python 3.10–3.12. Configure `backend/.env` from its example with your bot token and app URL.

```sh
cd backend
poetry install --no-root
cp .env.example .env
poetry run uvicorn app.main:app --reload
```

For the interface, run `npm install` and `npm run dev` in `webapp/`. Telegram integration requires a reachable app URL and your own bot configuration.

## Project status

Initial public source snapshot. Python syntax and source manifests were checked for publication; full application, infrastructure and external-service integration tests have not been run for this release. Local credentials, databases, sessions, uploaded content and machine-specific deployment files are excluded.

## License

Original project code is available under the [MIT License](LICENSE). External dependencies retain their respective licences.
