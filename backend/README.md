# QAshboard Backend

## Usage

Start the backend and watch for changes for development:

```sh
docker compose up backend --build --watch
```

---

Use the CLI to manage buildbots:

```sh
docker compose exec backend qbcli buildbot --help
```

In production, the database port won't be exposed even to localhost, so the CLI must be run using `docker compose exec`.

---

View the API documentation at:

http://localhost:8000/docs
