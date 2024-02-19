FROM python:3.12-bookworm as builder
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /usr/src/dormyboba-core
COPY . ./
RUN ${HOME}/.local/bin/poetry build
FROM python:3.12-bookworm
WORKDIR /app
COPY --from=builder /usr/src/dormyboba-core/dist ./
COPY config /config
RUN export WHL=$(ls *.whl) && pip install ./${WHL}
EXPOSE 50051 
CMD ["python3", "-m", "dormyboba_core", "--config-dir", "/config"]
