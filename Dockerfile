FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production
ENV TMP_DIR=/tmp/ocr-api
ENV USE_GPU=false
ENV OCR_LANG=en
ENV OCR_USE_ANGLE_CLS=true
ENV MAX_UPLOAD_SIZE_MB=20

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Install PaddlePaddle CPU version by default
RUN pip install --no-cache-dir paddlepaddle==2.6.1

COPY app /app/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]