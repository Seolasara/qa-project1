import time 
import os
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from src.pages.login_page import LoginPage 
from src.pages.agent_page import AgentPage 


def test_CSTM019_agent_preview(driver,new_agent): 

    # 전체 설정한 에이전트 생성
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(project_root, "src", "resources", "20.5mb.jpg")
    new_agent.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[data-testid='plusIcon']"))).click()
    image_input = new_agent.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))).send_keys(image_path)
    image = new_agent.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'img.MuiAvatar-img')))

    new_agent.set_name("미리보기 테스트용 에이전트")
    new_agent.set_description("미리보기 테스트용 한줄소개")
    new_agent.set_rules("미리보기 테스트용 에이전트 입니다.")
    new_agent.set_start_message("안녕하세요 미리보기 테스트용 에이전트 입니다.")
    new_agent.upload_file("testfile2.pdf")
    new_agent.checkbox_functions("search", "browsing", "image", "execution")

    time.sleep(5)

    # 미리보기 
    pre_name = driver.find_element(By.CSS_SELECTOR, "div.css-o58jes h6.MuiTypography-h6").text
    pre_desc = driver.find_element(By.CSS_SELECTOR, "div.css-o58jes p.MuiTypography-body1").text
    pre_rule = driver.find_element(By.CSS_SELECTOR, "div.eawehs30 p.MuiTypography-body1").text

    assert (pre_name == "미리보기 테스트용 에이전트" and
        pre_desc == "미리보기 테스트용 한줄소개" and
        pre_rule == "안녕하세요 미리보기 테스트용 에이전트 입니다."), "⛔ [FAIL] 미리보기 확인 실패"
    print("✅ [PASS] 미리보기 성공")



