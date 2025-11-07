import pytest
import time
from src.pages.login_page import LoginPage
from src.pages.image_upload_page import HelpyChatPage
from src.utils.config_reader import read_config


def test_CADV001_image_upload_success(driver):

    config = read_config("helpychat")
    base_url = config["base_url"]
    login_id = config["login_id"]
    login_pw = config["login_pw"]

    login_page = LoginPage(driver)
    login_page.page_open()
    login_page.login()
    time.sleep(3)

    driver.get(base_url)
    time.sleep(3)

    chat_page = HelpyChatPage(driver)

    chat_page.upload_image("dogimage.jpg")
    chat_page.send_message("이 이미지에 대해 설명해줘")

    assert "<img" in driver.page_source
    assert "이 이미지에 대해 설명해줘" in driver.page_source

    time.sleep(15)