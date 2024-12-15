FROM ubuntu:22.04

# Set noninteractive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    git \
    ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN crawl4ai-setup
RUN playwright install-deps 

# Create output directory and set permissions
RUN mkdir -p /app/output && chmod -R 777 /app/output

# Copy only necessary files
COPY *.py ./
COPY *.txt ./

# Command to run your application
CMD ["python3", "main.py"]