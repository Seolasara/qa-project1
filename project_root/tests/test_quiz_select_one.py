import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.config_reader import read_config
from src.pages.login_page import LoginPage


def test_CADV086_quiz_multiple_choice(driver, login, click_plus, send_test_message):
    """HelpyChat 퀴즈 생성 (객관식 4지선다 / 정답 1개 검증)"""

    config = read_config("helpychat")
    base_url = config["base_url"]
    driver.get(base_url)
    wait = WebDriverWait(driver, 40)

    click_plus()

    # 퀴즈 생성 버튼 클릭
    quiz_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='button']//span[contains(text(),'퀴즈 생성')]"))
    )
    driver.execute_script("arguments[0].click();", quiz_button)

    # 메시지 전송 (객관식)
    send_test_message("우리나라 동물에 관한 퀴즈 객관식으로 만들어줘")
    print("💬 메시지 전송 완료")

    # 퀴즈 생성
    print("⏳ 퀴즈 생성 중... (최대 5분 대기)")
    try:
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'완료')]"))
        )
        print("✅ '완료' 문구 감지됨")
    except Exception as e:
        print("❌ '완료' 문구 감지 실패:", e)
        assert False, "'퀴즈 생성 완료' 문구가 표시되지 않았습니다."

    # 렌더링 안정화
    time.sleep(8)

    # 퀴즈 유형 검증
    try:
        quiz_type = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='text-sm truncate' and text()='select_one']"))
        )
        print(f"✅ 퀴즈 유형 확인됨 → {quiz_type.text}")
    except Exception as e:
        print("❌ 퀴즈 유형 'select_one' 감지 실패:", e)
        assert False, "퀴즈 유형이 'select_one'으로 표시되지 않았습니다."

    # 선택지 4개인지 검증
    try:
        options = wait.until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                "//span[@class='font-medium text-xs px-2 py-1 rounded flex-shrink-0 mt-0.5 bg-muted text-muted-foreground']"
            ))
        )
        labels = [opt.text.strip() for opt in options]
        print(f"📋 감지된 선택지: {labels}")

        expected = ["A", "B", "C", "D"]
        for label in expected:
            assert label in labels, f"❌ 선택지 '{label}' 가 표시되지 않았습니다."
        print("✅ 객관식 4지선다 선택지 검증 완료")
    except Exception as e:
        print("❌ 객관식 선택지 감지 실패:", e)
        assert False, "객관식 선택지(A~D)가 올바르게 표시되지 않았습니다."

    # 정답 1개인지 검증
    correct_icons = driver.find_elements(
        By.CSS_SELECTOR, "svg.lucide.lucide-circle-check-big.text-green-600"
    )
    count = len(correct_icons)
    print(f"✅ 감지된 정답 아이콘 개수: {count}")

    assert count == 1, f"❌ 정답 아이콘이 1개가 아닙니다 (현재 {count}개)"
    print("✅ 객관식 퀴즈 검증 성공")

    time.sleep(3)