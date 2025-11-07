import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.pages.login_page import LoginPage


def test_HIST018_agent_btn(driver,login) :

    # 에이전트 버튼 클릭
    agent_btn = driver.find_element(By.CSS_SELECTOR, "a[href='/ai-helpy-chat/agent']")
    agent_btn.click()
    time.sleep(3)
    
    # 검증
    assert "https://qaproject.elice.io/ai-helpy-chat/agent" in driver.current_url, "⛔ [FAIL] 에이전트 버튼 실행 실패"
    print("✅ [PASS] 에이전트 버튼 실행 완료")
