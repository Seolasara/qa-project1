from selenium.webdriver.common.by import By
import time

class AgentEnterPage:
    """HelpyChat 에이전트 페이지 객체"""

    def __init__(self, driver):
        self.driver = driver
        self.url = "https://qaproject.elice.io/ai-helpy-chat/agent"
        self.agent_btn = (By.CSS_SELECTOR, "a[href='/ai-helpy-chat/agent']")

    # 에이전트 페이지 접속
    def open(self):
        agent_btn = self.driver.find_element(*self.agent_btn)
        agent_btn.click()
        time.sleep(3)

    # 페이지 접속 검증
    def is_opened(self):
        return self.url in self.driver.current_url