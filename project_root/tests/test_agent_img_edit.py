import time
import platform
import os
from selenium.webdriver.common.by import By
from src.pages.login_page import LoginPage
from src.pages.agent_page import AgentPage
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def test_CSTM026_my_agent_img_edit(driver, new_agent):

    # 수정용 에이전트 생성
    new_agent.set_name("이미지 수정 테스트용 에이전트") 
    new_agent.set_description("이미지 한줄 소개 테스트")
    new_agent.set_rules("이미지 수정 테스트") 
    new_agent.set_start_message("이미지 테스트 에이전트 입니다.")
    new_agent.upload_file("testfile2.pdf")
    new_agent.checkbox_functions("search", "browsing", "image", "execution")
    new_agent.click_create()
    new_agent.click_save()
    time.sleep(3)

    # 뒤로가기
    back_btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="뒤로가기"]')
    back_btn.click()

    # 내 에이전트 이동
    my_agent_btn = driver.find_element(By.LINK_TEXT, "내 에이전트")
    my_agent_btn.click()
    time.sleep(3)

    # 에이전트 선택
    first_agent = driver.find_elements(By.CSS_SELECTOR, 'button svg[data-testid="penIcon"]')[0]
    first_agent.click()
    time.sleep(3)

    # 랜덤이미지 수정
    new_agent.wait.until(EC.element_to_be_clickable((new_agent.locators["image_button"]))).click()
    new_agent.driver.find_element(By.XPATH, "//li[normalize-space(text())='이미지 생성기']").click()
    image = new_agent.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.MuiAvatar-img')))
    time.sleep(3)

    back_btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="뒤로가기"]')
    back_btn.click()
    time.sleep(3)

    img = new_agent.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="Agent avatar"]'))
    )

    assert img.is_displayed(), "⛔ [FAIL] 이미지 수정 실패"
    print("✅ [PASS] 이미지 수정 완료") 