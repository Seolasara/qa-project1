import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.config_reader import read_config
from src.pages.login_page import LoginPage


def test_CADV068_ppt_create_flow(driver, login, click_plus, send_test_message):
    """HelpyChat PPT 생성 테스트"""

    config = read_config("helpychat")
    base_url = config["base_url"]
    driver.get(base_url)
    wait = WebDriverWait(driver, 20)

    # + 버튼 클릭
    click_plus()

    # 메뉴의 PPT 생성 버튼 클릭
    ppt_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[@role='button']//span[contains(text(), 'PPT 생성')]"
        ))
    )
    driver.execute_script("arguments[0].click();", ppt_button)

    send_test_message("겨울에 주로 먹는 음식에 대한 ppt 만들어줘")

    print("⏳ 생성 버튼 로딩 대기 (3초)...")
    time.sleep(3)

    # ▶ 생성 버튼 클릭
    try:
        create_button = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@class,'MuiButton-root') and contains(normalize-space(.), '생성')]"
            ))
        )
        driver.execute_script("arguments[0].click();", create_button)
    except Exception as e:
        assert False, "'생성' 버튼 클릭 실패"

    # PPT 생성 완료 문구 대기 및 검증
    try:
        complete_msg = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//p[contains(text(),'프레젠테이션 생성이 완료되었습니다')]"
            ))
        )
        print("✅ 프레젠테이션 생성 완료 문구 감지됨")
        assert "프레젠테이션 생성이 완료되었습니다" in complete_msg.text
    except Exception as e:
        print("❌ '프레젠테이션 생성이 완료되었습니다!' 문구를 찾지 못했습니다:", e)
        assert False, "'프레젠테이션 생성 완료' 문구가 표시되지 않았습니다."

    print("✅ PPT 생성 및 완료 문구 검증 성공")