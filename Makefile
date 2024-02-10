PG_USER := postgres
PG_PASSWORD := 123456
PG_HOST := postgresql
PG_PORT := 5432
PG_DB := dormyboba
ALCH_URL := postgresql://${PG_USER}:${PG_PASSWORD}@${PG_HOST}:${PG_PORT}/${PG_DB}

.PHONY: alchemy-models
alchemy-models:
	poetry run sqlacodegen ${ALCH_URL} --outfile dormyboba_core/model/generated/generated.py

.PHONY: init-db
init-db:
	PGPASSWORD=${PG_PASSWORD} psql -h ${PG_HOST} -U ${PG_USER} -f db/drop.sql
	PGPASSWORD=${PG_PASSWORD} psql -h ${PG_HOST} -U ${PG_USER} -f db/schema.sql
	PGPASSWORD=${PG_PASSWORD} psql -h ${PG_HOST} -U ${PG_USER} -f db/data.sql
	