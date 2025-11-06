import pytest
from selenium import webdriver
import logging
import os
from datetime import datetime

@pytest.fixture(scope="function")
def driver():
    """공통 WebDriver 설정"""
    driver = webdriver.Chrome()
    #driver.maximize_window()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture(scope="session", autouse=True)
def setup_logger():
    """프로젝트 전체 공용 로거 설정 (모든 테스트 자동 적용)"""

    # 📂 로그 폴더 생성
    base_dir = os.path.dirname(os.path.dirname(__file__))
    log_dir = os.path.join(base_dir, "reports", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # 📄 로그 파일명
    log_file = os.path.join(
        log_dir, f"helpychat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    # 🧩 기본 로거 설정
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # 모든 로그 레벨 허용

    # 📋 포맷 지정
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # 💾 파일 핸들러
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 💻 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logging.info("=== ✅ 전역 로거 설정 완료 ===")
    yield
    logging.info("=== 🧾 테스트 세션 종료 ===")