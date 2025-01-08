# python 버전 선택
FROM python:3.9.19

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사
COPY . /app/

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 애플리케이션 실행
CMD ["python", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
