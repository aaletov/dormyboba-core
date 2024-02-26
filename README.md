# dormyboba-core
Dormyboba core service

## Local development

Необходимо указать переменную среды `CONFIG_DIR`, соответствующий директории, в которой
лежат конфиги

```bash
CONFIG_DIR=./config poetry run python3 -m dormyboba_core
```

### Coverage:

```bash
poetry run pytest --cov=dormyboba_core --cov-report term-missing
```
