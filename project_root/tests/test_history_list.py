import time
from selenium.webdriver.common.by import By
from src.pages.login_page import LoginPage


def test_HIST028_history_list(driver,login,send_test_message) :

    # 테스트용 메세지 전송
    send_test_message("히스토리 목록 최신순 확인용 메세지(답장하지마)")
    time.sleep(3)

    # 히스토리 중 가장 최신대화 출력
    list = driver.find_elements(By.CSS_SELECTOR, '[data-testid="virtuoso-item-list"] [data-index="0"]')
    chat_frist = list[0]
    print(chat_frist.text)
    time.sleep(3)

    assert "히스토리 목록 최신순 확인용 메세지" in chat_frist.text, "⛔ [FAIL] 히스토리 목록 최신순 검증 실패"
    print("✅ [PASS] 히스토리 목록 최신순 검증 성공")

