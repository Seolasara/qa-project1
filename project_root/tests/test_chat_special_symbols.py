import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.login_page import LoginPage

# CBAS005: 특수문자 포함 질문 → 응답 확인
def test_CBAS001_chat_basic(driver, login, send_test_message):
    
    send_test_message("$$%⭑ 대한민국의 수도는?")
    print("✅ [PASS] 질문 전송 완료")
    
    # AI 응답 대기 및 확인
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-step-type='assistant_message'] .message-content"))
    )
    time.sleep(3)

    response_box = driver.find_element(By.CSS_SELECTOR, "div[data-step-type='assistant_message'] .message-content")
    response_text = response_box.get_attribute("innerText")

    assert len(response_text) > 0, "⛔ [FAIL] AI 응답 확인 실패"
    print("✅ [PASS] AI 응답 확인 완료")
