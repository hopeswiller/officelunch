FROM python:3.8-slim-buster as build-stage

LABEL maintainer="David Boateng Adams <davidba941@gmail.com>"

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install pip requirements
COPY requirements.txt .
# RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . .


###############################################################


FROM python:3.8-slim-buster

WORKDIR /app

COPY --from=build-stage /usr/local /usr/local
COPY --from=build-stage /app /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" hopes && chown -R hopes /app
USER hopes

EXPOSE 8000

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Lunch.wsgi"]


