# QAshboard

## Quick preview

Setup `.env`
```sh
cp .env.example .env
$EDITOR .env
```

Start the containers:
```sh
docker compose up --build
```

Create a buildbot and record the token:
```sh
export BUILDBOT_TOKEN="$(docker compose exec -T backend qbcli buildbot create buildbot-111)"
```

Generate test data:
```sh
python3 scripts/gen_test_data.py -b buildbot-111
```

Post logs:
```sh
curl -X PUT -H "Authorization: Bearer $BUILDBOT_TOKEN" -F 'file=@/path/to/your/log.log' localhost:8000/api/v1/builds/1/logs
```

Then visit `http://localhost:8080`

To reset the database between previews, run:
```sh
docker compose down --volumes
```
