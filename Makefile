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
	PGPASSWORD=${PG_PASSWORD} psql -h ${PG_HOST} -U ${PG_USER} -f db/1_drop.sql
	PGPASSWORD=${PG_PASSWORD} psql -h ${PG_HOST} -U ${PG_USER} -f db/2_schema.sql
	PGPASSWORD=${PG_PASSWORD} psql -h ${PG_HOST} -U ${PG_USER} -f db/3_data.sql

image_time=$(shell git rev-parse --short HEAD)
.PHONY: docker-image
docker-image:
	docker build -t dormyboba-core:${image_time} .
	docker tag dormyboba-core:${image_time} dormyboba-core:latest

