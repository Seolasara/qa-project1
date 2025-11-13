import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.config_reader import read_config

class ChatPage:
    def __init__(self, driver):
        self.driver = driver
        # 요소 정의
        self.input_box = (By.CSS_SELECTOR, "textarea[placeholder='메시지를 입력하세요...']")
        self.send_button = (By.CSS_SELECTOR, "button#chat-submit")
        self.response_area = (By.CSS_SELECTOR, "div[data-step-type='assistant_message'] .message-content")

    # 메시지 입력
    def enter_message(self, text):
        input_el = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.input_box)
        )
        input_el.clear()
        input_el.send_keys(text)
        time.sleep(1)  # React 감지 대기

    # 메시지 전송
    def click_send(self):
        send_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.send_button)
        )
        send_btn.click()

    # AI 응답 대기 및 반환
    def wait_for_response(self, timeout=20):
        """마지막 AI 응답이 실제 텍스트를 가질 때까지 대기"""
        end_time = time.time() + timeout
        last_response = ""
        
        while time.time() < end_time:
            responses = self.driver.find_elements(*self.response_area)
            if responses:
                # text로 가져오기
                last_response = responses[-1].text.strip()
                if last_response:  # 실제 텍스트가 있으면 반환
                    return last_response
            time.sleep(0.5)
        
        # 타임아웃
        all_texts = [el.text.strip() for el in self.driver.find_elements(*self.response_area)]
        print("\n[DEBUG] 감지된 response 목록:")
        for t in all_texts:
            print("-", t[:120])
        raise AssertionError("⛔ [FAIL] AI 응답이 제한 시간 내 도착하지 않음")