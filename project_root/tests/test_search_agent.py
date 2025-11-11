import time
from selenium.webdriver.common.by import By
from src.pages.login_page import LoginPage
from src.pages.agent_enter_page import AgentEnterPage

def test_HIST020_search_agent(driver,login) :

    # 에이전트 페이지 접속
    agent_page = AgentEnterPage(driver)
    agent_page.open()

    # 에이전트 검색 
    search_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='AI 에이전트 검색']").send_keys("엘리스")
    time.sleep(5)
    
    # 검색 결과
    search_result = driver.find_element(By.CSS_SELECTOR, "a.MuiCard-root")
    print("검색 결과:", search_result.text)

    assert "엘리스" in search_result.text, "⛔ [FAIL] 에이전트 검색 실패"
    print("✅ [PASS] 에이전트 검색 성공")





