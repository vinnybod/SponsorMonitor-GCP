FROM python:3.8-slim

ARG USER=appuser

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PIP_NO_CACHE_DIR off
ENV PATH /home/$USER/.local/bin:$PATH

RUN useradd --create-home $USER
WORKDIR /home/$USER/src/sponsormonitor
USER $USER

COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers=2", "--threads=4", "--worker-class=gthread", "--log-file=-", "--access-logfile=-", "--worker-tmp-dir=/dev/shm", "-k", "uvicorn.workers.UvicornWorker", "sm:app"]