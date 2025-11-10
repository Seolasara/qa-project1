import pytest
from selenium import webdriver
import logging
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from src.pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from src.pages.agent_page import AgentPage


@pytest.fixture(scope="function")
def driver():
    """공통 WebDriver 설정"""
    driver = webdriver.Chrome()
    #driver.maximize_window()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture
def send_test_message(driver):
    """테스트용 메세지 보내는 fixture (메시지를 매개변수로 받아서 전송)"""
    def _create_chat(message):
        # 메시지 입력 및 전송
        message_box = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='메시지를 입력하세요...']")
        message_box.clear()
        message_box.send_keys(message)
        driver.find_element(By.ID, "chat-submit").click()
        time.sleep(3)
    return _create_chat


@pytest.fixture
def login(driver):
    """HelpyChat 로그인 fixture"""
    login_page = LoginPage(driver)
    login_page.page_open()
    login_page.login()
    time.sleep(3)
    return login_page


@pytest.fixture
def new_agent(driver):
    """로그인 후 커스텀 에이전트 생성 페이지로 이동한 상태를 반환"""
    login_page = LoginPage(driver)
    login_page.page_open()
    login_page.login()

    agent_page = AgentPage(driver)
    agent_page.agent_create()
    return agent_page