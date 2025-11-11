import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.login_page import LoginPage

# CBAS005: 이모지 포함 질문 → 응답 확인
def test_CBAS005_chat_emoji(driver, login):
    
    input_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea[placeholder='메시지를 입력하세요...']"))
    )
    input_box.click()
    message = "퀴즈 맞혀봐. 🥬 + 🥒 + 🍅 + 🧅 = ?"
    
    # JS로 값 세팅
    driver.execute_script(
    "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true, cancelable: true }));",
    input_box,
    message
    )
    
    # React가 변경 감지하도록 send_keys('') 한 번 실행
    input_box.send_keys(" ")
    input_box.send_keys("\b") # 공백 입력 후 삭제
    
    send_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button#chat-submit"))
    )
    send_button.click()    
    print("✅ [PASS] 질문 전송 완료")
    
    # AI 응답 대기 및 확인
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-step-type='assistant_message'] .message-content"))
    )
    time.sleep(10)

    response_box = driver.find_element(By.CSS_SELECTOR, "div[data-step-type='assistant_message'] .message-content")
    response_text = response_box.get_attribute("innerText")

    assert len(response_text) > 0, "⛔ [FAIL] AI 응답 확인 실패"
    print("✅ [PASS] AI 응답 확인 완료")
