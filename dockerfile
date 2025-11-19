# --- 1. 베이스 이미지 ---
FROM python:3.12-slim

# --- 2. 환경 변수 ---
ENV WORKDIR=/app
ENV ALLURE_DIR=/app/reports/allure

# --- 3. 작업 디렉토리 생성 ---
RUN mkdir -p ${WORKDIR} ${ALLURE_DIR}
WORKDIR ${WORKDIR}

# --- 4. 시스템 의존성 설치 (Allure CLI용) ---
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk-headless curl unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# --- 5. Allure CLI 설치 ---
RUN curl -o /tmp/allure.zip -L https://github.com/allure-framework/allure2/releases/download/2.27.1/allure-2.27.1.zip && \
    unzip /tmp/allure.zip -d /opt/ && \
    ln -s /opt/allure-2.27.1/bin/allure /usr/bin/allure && \
    rm /tmp/allure.zip

# --- 6. Python 패키지 설치 ---
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# --- 7. 테스트 코드 복사 ---
COPY project_root/ ./project_root/

# --- 8. pytest 실행 예시 ---
# 컨테이너 실행 시 pytest 실행
CMD ["pytest", "project_root/tests", "--alluredir=reports/allure", "--capture=tee-sys", "--junit-xml=reports/all-results.xml"]
