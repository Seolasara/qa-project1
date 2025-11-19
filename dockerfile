# --- 1. 베이스 이미지: OpenJDK 17 + slim ---
FROM openjdk:17-slim

# --- 2. 환경 변수 ---
ENV WORKDIR=/app
ENV ALLURE_DIR=/app/reports/allure

# --- 3. 작업 디렉토리 생성 ---
RUN mkdir -p ${WORKDIR} ${ALLURE_DIR}
WORKDIR ${WORKDIR}

# --- 4. Python 설치 + 필수 패키지 ---
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip curl unzip git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# --- 5. Allure CLI 설치 ---
RUN curl -o /tmp/allure.zip -L https://github.com/allure-framework/allure2/releases/download/2.27.1/allure-2.27.1.zip && \
    unzip /tmp/allure.zip -d /opt/ && \
    ln -s /opt/allure-2.27.1/bin/allure /usr/bin/allure && \
    rm /tmp/allure.zip

# --- 6. Python 패키지 설치 ---
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# --- 7. 프로젝트 코드 복사 ---
COPY project_root/ ./project_root/

# --- 8. pytest 기본 실행 명령 ---
# 필요 시 Jenkins에서 CMD를 override 가능
CMD ["pytest", "project_root/tests", "--alluredir=reports/allure", "--capture=tee-sys", "--junit-xml=reports/all-results.xml"]
