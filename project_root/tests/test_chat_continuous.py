import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.login_page import LoginPage
from src.pages.chat_page import ChatPage

# CBAS002: 연속 질문 → 응답 확인
def test_CBAS002_chat_continuous(driver, login):
    
    chat = ChatPage(driver)

    # 첫 번째 질문
    first_question = "오늘 서울 날씨 어때?"
    chat.enter_message(first_question)
    chat.click_send()
    print(f"✅ [PASS] 첫 번째 질문 전송 완료: {first_question}")

    first_response = chat.wait_for_response()
    assert len(first_response) > 0, "⛔ [FAIL] 첫 번째 AI 응답 확인 실패"
    print("✅ [PASS] 첫 번째 AI 응답 확인 완료")

    # 두 번째 질문 (연속 질문)
    second_question = "그럼 내일은?"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(chat.input_box)
    )
    chat.enter_message(second_question)
    chat.click_send()
    print(f"✅ [PASS] 두 번째 질문 전송 완료: {second_question}")

    second_response = chat.wait_for_response()
    assert len(second_response) > 0, "⛔ [FAIL] 두 번째 AI 응답 확인 실패"
    print("✅ [PASS] 두 번째 AI 응답 확인 완료")
    