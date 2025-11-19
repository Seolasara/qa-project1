import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.login_page import LoginPage

# CBAS015: 응답 클립보드 복사 및 붙여넣기
def test_CBAS015_ans_copy(driver, login, send_test_message):
    
    send_test_message("응답 클립보드 복사 및 붙여넣기 테스트 입니다.")
    print("✅ [PASS] 질문 전송 완료")
    
    # AI 응답 대기 및 확인
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-step-type='assistant_message'] .message-content"))
    )

    response_box = driver.find_element(By.CSS_SELECTOR, "div[data-step-type='assistant_message'] .message-content")
    response_text = response_box.get_attribute("innerText")

    response_div = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-step-type='assistant_message']"))
    )
    
    # 클립보드 복사 버튼 확인
    copy_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button:has(svg.lucide-copy)"))
    )
    
    # 클립보드 복사 버튼 클릭
    copy_button.click()
    print("✅ [PASS] 클립보드 복사 버튼 클릭 완료")
    
    # 클립보드 복사 버튼 아이콘이 체크 표시로 변경 확인
    check_icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button svg.lucide-check"))
    )
    assert check_icon.is_displayed(), "⛔ [FAIL] 클립보드 복사 후 체크 표시로 변경 실패"
    print("✅ [PASS] 클립보드 복사 아이콘 체크 표시로 변경")

    # 질문 입력란에 붙여넣기 성공 확인
    input_box = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='메시지를 입력하세요...']")
    driver.execute_script("arguments[0].value = arguments[1];", input_box, response_text)
    pasted_text = input_box.get_attribute("value")
    assert pasted_text == response_text, "⛔ [FAIL] 붙여넣기 실패"
    print("✅ [PASS] 붙여넣기 성공")
