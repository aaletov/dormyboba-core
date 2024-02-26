FROM python:3.10.13-slim-bookworm as builder
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /usr/src/dormyboba-core
COPY . ./
RUN ${HOME}/.local/bin/poetry build
FROM python:3.10.13-slim-bookworm
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get purge -y --auto-remove
WORKDIR /app
COPY --from=builder /usr/src/dormyboba-core/dist ./
COPY config /config
RUN export WHL=$(ls *.whl) && pip install ./${WHL}
EXPOSE 50051
CMD ["python3", "-m", "dormyboba_core", "--config-dir", "/config"]
