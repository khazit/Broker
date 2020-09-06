FROM python:3.7

# Install poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Create working directory
RUN mkdir work
COPY api work
WORKDIR /work

# Install project dependencies
RUN poetry install

# Run Flask app in dev mode
ENTRYPOINT FLASK_ENV=development flask run --host 0.0.0.0

# Network config
EXPOSE 5000
