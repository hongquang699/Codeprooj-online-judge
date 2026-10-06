# Multi-language Judge Environment
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    python3 \
    python3-pip \
    openjdk-17-jdk-headless \
    nodejs \
    rustc \
    golang-go \
    fp-compiler \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir psutil pyyaml

WORKDIR /app/judge-system

COPY . /app/judge-system/

EXPOSE 9999

HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:9999/api/v1/health || exit 1

CMD ["python3", "judge-server/main.py"]
