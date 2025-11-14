import time 
import pytest 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from src.pages.login_page import LoginPage 
from src.pages.agent_page import AgentPage 


# --- 필수값으로만 에이전트 생성(이름,규칙) --- 
def test_CSTM005_with_essential_field(new_agent): 
    # 필수값 이름/규칙 입력 
    new_agent.set_name("테스트") 
    new_agent.set_rules("테스트") 
    
    # 만들기 클릭 / 저장 클릭
    new_agent.click_create()
    new_agent.click_save()

    # 에이전트 생성 메세지 확인
    text = new_agent.wait.until(EC.presence_of_element_located((By.ID, "notistack-snackbar"))).text.strip()
    assert "에이전트가 생성 되었습니다." in text, "⛔ [FAIL] 생성 실패"
    print("✅ [PASS] 에이전트 생성 완료") 


# --- 극단적 입력(이모지) ---
def test_CSTM008_extreme_input(new_agent):

    emoji = "🙂"

    # JavaScript로 이름 필드 입력 / 강제 이벤트 실행
    name = new_agent.driver.find_element(*new_agent.locators["name_field"])
    name.click()
    new_agent.driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
            name,
            emoji
        )
    name.send_keys(" ")  # React 감지용
    name.send_keys("\b")
    time.sleep(0.5)

    # JavaScript로 규칙 필드 입력 / 강제 이벤트 실행
    rules = new_agent.driver.find_element(*new_agent.locators["rules_field"])
    rules.click()
    new_agent.driver.execute_script(
        "arguments[0].value = arguments[1];"
        "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
        rules,
        emoji
    )
    rules.send_keys(" ") # React 감지용
    rules.send_keys("\b")
    
    # 만들기/저장 클릭
    new_agent.click_create()
    new_agent.click_save()

    # 에이전트 생성 메세지 확인
    text = new_agent.wait.until(EC.presence_of_element_located((By.ID, "notistack-snackbar"))).text.strip()
    assert "에이전트가 생성 되었습니다." in text, "⛔ [FAIL] 생성 실패"
    print("✅ [PASS] 에이전트 생성 완료") 


# --- 극단적 입력(미지원 언어) --- 
def test_CSTM009_unavailable_language(new_agent): 

    # 필수값 이름/규칙 입력 
    new_agent.set_name("هههههههههه") 
    new_agent.set_rules("هههههههههه") 
    
    new_agent.click_create()
    new_agent.click_save()

    # 에이전트 생성 메세지 확인
    text = new_agent.wait.until(EC.presence_of_element_located((By.ID, "notistack-snackbar"))).text.strip()
    assert "에이전트가 생성 되었습니다." in text, "⛔ [FAIL] 생성 실패"
    print("✅ [PASS] 에이전트 생성 완료") 