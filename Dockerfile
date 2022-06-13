FROM python:stretch

ARG PASS
ENV PASS=${PASS}

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


ENTRYPOINT ["gunicorn", "-b", ":80", "app:app"]
# ENTRYPOINT ["python", "test.py"]