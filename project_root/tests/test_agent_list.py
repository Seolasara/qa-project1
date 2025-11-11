import time
from selenium.webdriver.common.by import By
from src.pages.login_page import LoginPage
from src.pages.agent_enter_page import AgentEnterPage
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

def test_CSTM020_agent_list(driver,login) :

    # 에이전트 페이지 접속
    agent_page = AgentEnterPage(driver)
    agent_page.open()

    # 에이전트 목록 스크롤
    scrollers = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='virtuoso-scroller']")
    agent_scroller = scrollers[1]

    prev_max_index = -1
    first_index = None

    # 에이전트 갯수 확인
    for i in range(10):
        # 현재 렌더된 에이전트 목록 data-index 추출
        agent_items = agent_scroller.find_elements(By.CSS_SELECTOR, "div[data-index]")
        agent_indexes = [int(item.get_attribute("data-index")) for item in agent_items]
        max_index = max(agent_indexes)

        # 첫 번째 스크롤의 마지막 index 기록
        if i == 0:
            first_index = max_index
            print(f"\n현재 에이전트 목록 갯수 : {first_index}")

        # 더 이상 인덱스가 증가하지 않으면 상위 for문 종료
        if max_index == prev_max_index:
            break

        # 스크롤 내리기
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", agent_scroller)
        time.sleep(1)

        prev_max_index = max_index

    print(f"\n최종 로드된 에이전트 목록 갯수 = {max_index}")

    assert max_index >= first_index, "⛔ [FAIL] 에이전트 목록 확인 실패"
    print("\n✅ [PASS] 에이전트 목록 확인 성공")

