FROM python:3.10-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget unzip curl gnupg ca-certificates openjdk-11-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------
# 1) Google Chrome 설치
# ---------------------------------------------------------
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# ---------------------------------------------------------
# 2) ChromeDriver 버전 자동 매칭 설치
# ---------------------------------------------------------
RUN CHROME_VERSION=$(google-chrome --version | sed -E 's/.* ([0-9]+)\..*/\1/') \
    && DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}") \
    && wget -q "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip

# ---------------------------------------------------------
# 3) Allure 설치
# ---------------------------------------------------------
RUN wget -qO allure.tgz https://github.com/allure-framework/allure2/releases/latest/download/allure-commandline.tgz \
    && tar -xzf allure.tgz -C /opt/ \
    && ln -s /opt/allure-*/bin/allure /usr/bin/allure \
    && rm allure.tgz

# ---------------------------------------------------------
# 4) Python 기본 설정
# ---------------------------------------------------------
WORKDIR /workspace

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PATH="/workspace/venv/bin:$PATH"

CMD ["bash"]
