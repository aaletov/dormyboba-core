# dormyboba-core
Dormyboba core service

## Local development

Необходимо указать флаг `--config-dir`, соответствующий директории, в которой
лежат конфиги

```bash
poetry run python3 -m dormyboba_core --config-dir=./config
```

### Coverage:

```bash
poetry run pytest --cov=dormyboba_core --cov-report term-missing
```
