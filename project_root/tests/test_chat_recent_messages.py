import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.login_page import LoginPage

# CBAS074: 최근 메시지 보기
def test_CBAS074_chat_basic(driver, login, send_test_message):
    
    send_test_message("오늘 주요 기사 내용 요약해줘")
    
    # 마지막 응답 대기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-step-type='assistant_message'] .message-content"))
    )
    print("✅ [PASS] 마지막 응답 확인 완료")
    time.sleep(10)
    
    # 스크롤바 생성
    
    
    # 최근 메시지 보기 버튼 확인 및 클릭
    arrow_down_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.inline-flex.items-center.justify-center.gap-2.h-9.w-9.rounded-full"))
    )
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(arrow_down_button)
    )
    arrow_down_button.click()
    print("✅ [PASS] 최근 메시지 보기 버튼 클릭 완료")
    time.sleep(1)
    
    # 마지막 메시지로 자동 스크롤 이동 확인
    last_message = driver.find_element(By.CSS_SELECTOR, "div[data-step-type='assistant_message']:last-child")
    is_visible = driver.execute_script(
        "var rect = arguments[0].getBoundingClientRect(); return (rect.top >= 0 && rect.bottom <= window.innerHeight);",
        last_message
    )

    assert is_visible, "⛔ [FAIL] 최근 메시지로 자동 스크롤 이동 실패"
    print("✅ [PASS] 최근 메시지 보기 확인 완료")
    