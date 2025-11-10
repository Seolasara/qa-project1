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
def click_plus(driver):
    """HelpyChat의 '+ 버튼' 클릭 """
    wait = WebDriverWait(driver, 15)

    def _click():
        # + 버튼 대기 및 클릭
        plus_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-haspopup='true'] svg[data-icon='plus']")
            )
        )
        # svg 대신 부모 <button> 클릭
        driver.execute_script("arguments[0].closest('button').click();", plus_button)
        time.sleep(1)

    return _click