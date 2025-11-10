import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.config_reader import read_config
from src.pages.login_page import LoginPage


def test_CADV032_google_search_request(driver, login, click_plus, send_test_message):
    """HelpyChat 구글 검색 기능 테스트"""

    config = read_config("helpychat")
    base_url = config["base_url"]
    driver.get(base_url)
    wait = WebDriverWait(driver, 15)

    # + 버튼 클릭
    click_plus()

    #'구글 검색' 버튼 클릭
    google_search_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[@role='button']//span[contains(text(), '구글 검색')]"
        ))
    )
    driver.execute_script("arguments[0].click();", google_search_btn)
    print("🔍 '구글 검색' 버튼 클릭 완료")

    # 메시지 전송
    send_test_message("현재 대전 온도 알려줘")

    # 응답 검증
    try:
        response_bubble = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class, 'chat-bubble') or contains(text(), '대전') or contains(text(), '℃') or contains(text(), '온도')]"
            ))
        )
        print("✅ 응답 감지됨 — 구글 검색 기능 정상 작동")
        assert "대전" in response_bubble.text or "온도" in response_bubble.text, "응답에 온도 정보가 없습니다."
    except Exception as e:
        print("❌ 구글 검색 응답이 표시되지 않았습니다 (시간 초과 또는 요소 미탐지)")
        assert False, f"구글 검색 기능 실패: {e}"

    print("✅ 테스트 완료: 구글 검색 요청 및 응답 검증 성공")