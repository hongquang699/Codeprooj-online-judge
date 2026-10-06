#!/bin/bash
set -e

echo "=== Installing VNOI Judge System Dependencies ==="

# Update package lists
if command -v apt-get &> /dev/null; then
    apt-get update
    apt-get install -y \
        build-essential \
        gcc \
        g++ \
        python3 \
        python3-pip \
        python3-venv \
        openjdk-17-jdk \
        rustc \
        golang-go \
        nodejs \
        fp-compiler \
        curl \
        jq
fi

# Python dependencies
pip install --upgrade pip
pip install psutil pyyaml

echo "=== VNOI Judge System Dependencies Installed Successfully ==="
