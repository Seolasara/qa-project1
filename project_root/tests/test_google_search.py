import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.config_reader import read_config


def test_CADV032_google_search_request(driver, login, click_plus, send_test_message):
    """HelpyChat 구글 검색 기능 테스트 (강화 안정화 버전)"""

    config = read_config("helpychat")
    base_url = config["base_url"]
    driver.get(base_url)
    wait = WebDriverWait(driver, 20)

    # 1️⃣ + 버튼 클릭
    click_plus()

    # 2️⃣ 구글 검색 버튼 안정화 탐색
    # Helpy에서 메뉴가 뜰 때까지 시간이 걸리므로 presence → clickable 2단계 대기
    google_selector = "div[role='button'] span:contains('구글 검색')"  # CSS4 selector 사용 불가 → 아래 XPATH fallback

    google_btn = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//div[@role='button']//span[contains(text(), '구글 검색')]"
        ))
    )
    wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[@role='button']//span[contains(text(), '구글 검색')]"
        ))
    )
    driver.execute_script("arguments[0].click();", google_btn)
    print("📌 '구글 검색' 버튼 클릭 완료")

    # 3️⃣ 사용자 메시지 전송
    send_test_message("현재 대전 온도 알려줘")
    print("📌 메시지 전송 완료")

    # 4️⃣ Helpy 응답 나오기까지 대기 (assistant_message 기준)
    # 단순 presence만 쓰면 조기 감지 → scrollHeight 변화를 기반으로 응답 도착 감지
    start_time = time.time()
    last_height = 0
    stable = 0

    while time.time() - start_time < 90:
        try:
            # assistant_message가 등장했는지 먼저 체크
            messages = driver.find_elements(
                By.CSS_SELECTOR, "div[data-step-type='assistant_message'] .message-content"
            )
            if messages:
                new_height = driver.execute_script("return document.body.scrollHeight;")

                if new_height == last_height:
                    stable += 1
                else:
                    stable = 0

                last_height = new_height

                if stable >= 3:
                    break
        except:
            pass

        time.sleep(1)

    # 최종 assistant_message 요소
    response_box = wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "div[data-step-type='assistant_message'] .message-content"
        ))
    )
    time.sleep(2)

    # 5️⃣ 텍스트 추출
    response_text = response_box.get_attribute("innerText")
    print(f"📌 Helpy 응답 감지됨:\n{response_text}")

    # 6️⃣ 키워드 기반 테스트 검증
    keywords = ["Daejeon", "대전", "온도", "℃", "°C", "temperature"]
    matched = [kw for kw in keywords if kw.lower() in response_text.lower()]

    assert len(matched) >= 2, f"❌ Helpy 응답에 필요한 정보 부족: {matched}"
    print(f"✅ HelpyChat 구글 검색 테스트 통과 (감지된 키워드: {matched})")