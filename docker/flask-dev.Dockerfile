FROM python:3.7

# Install poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Create working directory
RUN mkdir work
COPY api/broker work/broker
COPY api/app.py work/app.py
COPY api/pyproject.toml work/pyproject.toml
WORKDIR /work

# Install project dependencies
RUN poetry update

# Run Flask app in dev mode
ENTRYPOINT ["flask", "run", "--reload", "--host", "0.0.0.0"]

# Network config
EXPOSE 5000
