import os
import time 
import pytest 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.pages.login_page import LoginPage 
from src.pages.agent_page import AgentPage 


# --- 한줄 소개 극단적 입력 --- 
def test_CSTM012_extreme_input(new_agent): 

    # 수값 이름/규칙/극단적 한줄 소개 입력 
    new_agent.set_name("테스트4") 
    new_agent.set_rules("테스트4") 
    new_agent.set_description("테스트4" + "4" * 298)
    
    # 한줄 소개 오류 메세지 확인
    message_element = new_agent.wait.until(EC.visibility_of_element_located((By.XPATH, "//p[text()='한줄 소개는 최대 300자입니다']")))
    message_text = message_element.get_attribute("innerText").strip()
    assert message_text == "한줄 소개는 최대 300자입니다", "⛔ [FAIL] 예상대로 오류메시지 표시X"
    print("❎ [XFAIL] 한줄 소개는 최대 300자입니다")

    # 3. 만들기 버튼 비활성화 확인
    try:
        new_agent.wait_for_button()
        button_active = True
    except TimeoutException:
        button_active = False

    assert not button_active, "⛔ [FAIL] 예상대로 만들기 버튼 비활성화X"

    print("❎ [XFAIL] 에이전트 생성 실패 - 한줄 소개 극단적 입력") 