FROM python:3.7

# Install poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Create working directory
RUN mkdir work
COPY runner/runner.py work/runner.py
COPY runner/pyproject.toml work/pyproject.toml
WORKDIR /work

# Install project dependencies
RUN poetry update

ENTRYPOINT ["python", "runner.py"]
