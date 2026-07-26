# QAshboard

## Quick preview

Start the containers:
```sh
docker compose up
```

Generate test data:
```sh
python3 scripts/gen_test_data.py
```

Then visit `http://localhost:8080`

To reset the database between previews, run:
```sh
docker compose down --volumes
```
