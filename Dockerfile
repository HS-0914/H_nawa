# 베이스 이미지: Python 3.11 + 슬림한 OS
FROM python:3.11-slim

# 필수 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    curl unzip fonts-liberation libnss3 libatk-bridge2.0-0 \
    libxss1 libasound2 libgtk-3-0 libxshmfence1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 워킹 디렉토리 설정
WORKDIR /app

# 프로젝트 파일 복사
COPY . .

# Python 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Playwright 브라우저 엔진 설치
RUN playwright install --with-deps

# Uvicorn으로 FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
