FROM python:3.11-slim

# Need to configure `/test-repo` as mount path in the execution settings
WORKDIR /test-repo

# We can copy the source code, there is no harm in it.
# But execution will mount the the repository at the configured path anyways.
#COPY ./src ./src
#COPY ./test ./test
COPY ./requirements.txt .

ENV PYTHONPATH=/test-repo/src

RUN pip install --no-cache-dir -r requirements.txt

