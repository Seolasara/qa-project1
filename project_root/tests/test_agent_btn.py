import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.pages.login_page import LoginPage
from src.pages.agent_enter_page import AgentEnterPage

def test_HIST018_agent_btn(driver,login) :

    # 에이전트 페이지 접속
    agent_page = AgentEnterPage(driver)
    agent_page.open()
    
    # 검증
    assert agent_page.is_opened(), "⛔ [FAIL] 에이전트 버튼 실행 실패"
    print("✅ [PASS] 에이전트 버튼 실행 완료")