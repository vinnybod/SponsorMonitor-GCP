FROM python:3-alpine

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PIP_NO_CACHE_DIR=off

WORKDIR /usr/src/sponsormonitor

RUN apk update && \
    apk add --no-cache build-base libffi-dev openssl-dev

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir uvicorn

COPY . .

EXPOSE 5000

CMD ["uvicorn", "sm:app", "--host", "0.0.0.0", "--port", "5000"]