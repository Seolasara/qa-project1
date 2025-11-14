import time 
import pytest 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from src.pages.login_page import LoginPage 
from src.pages.agent_page import AgentPage 


# --- 필수 입력값없이 생성 시도 --- 
def test_CSTM003_try_without_essential(new_agent): 
    
    # 만들기 버튼 활성화 확인
    try:
        new_agent.wait_for_button()
        button_active = True
    except TimeoutException:
        button_active = False

    assert not button_active, "⛔ [FAIL] 만들기 버튼 활성화"
    print("❎ [XFAIL] 에이전트 생성 실패 - 필수값 미입력") 


# --- 이름 필드만 입력 / 생성 시도 --- 
def test_CSTM004_with_name_input(new_agent): 
    
    # 이름 입력 후 만들기 버튼 활성화 확인
    new_agent.set_name("테스트") 

    try:
        new_agent.wait_for_button()
        button_active = True
    except TimeoutException:
        button_active = False

    assert not button_active, "⛔ [FAIL] 만들기 버튼 활성화"
    print("❎ [XFAIL] 에이전트 생성 실패 - 규칙 미입력") 
