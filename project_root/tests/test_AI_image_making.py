import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.config_reader import read_config
from src.pages.login_page import LoginPage


def test_CADV090_image_generation(driver, login, click_plus, send_test_message):
    """HelpyChat 이미지 생성 테스트"""

    config = read_config("helpychat")
    base_url = config["base_url"]
    driver.get(base_url)
    wait = WebDriverWait(driver, 30)

    click_plus()

    image_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[@role='button']//span[contains(text(), '이미지 생성')]"
        ))
    )
    driver.execute_script("arguments[0].click();", image_button)
    print("🖼️ '이미지 생성' 버튼 클릭 완료")

    # 현재 페이지 기준 기존 이미지 src 수집
    initial_imgs = driver.find_elements(By.TAG_NAME, "img")
    initial_srcs = [img.get_attribute("src") for img in initial_imgs]
    print(f"📸 현재 페이지에 존재하는 초기 이미지 개수: {len(initial_srcs)}")

    send_test_message("고양이 일러스트 생성")

    # 실제 새 이미지 탐색 (iframe 포함)
    print("⏳ AI 이미지 렌더링 대기")
    img_detected = False
    max_wait = 120
    poll_interval = 5

    for elapsed in range(0, max_wait, poll_interval):
        new_srcs = set()
        # 기본 DOM에서 수집
        imgs = driver.find_elements(By.TAG_NAME, "img")
        new_srcs.update([i.get_attribute("src") for i in imgs if i.get_attribute("src")])

        # iframe 내부도 검사
        frames = driver.find_elements(By.TAG_NAME, "iframe")
        for idx, frame in enumerate(frames):
            try:
                driver.switch_to.frame(frame)
                frame_imgs = driver.find_elements(By.TAG_NAME, "img")
                new_srcs.update([i.get_attribute("src") for i in frame_imgs if i.get_attribute("src")])
                driver.switch_to.default_content()
            except Exception:
                driver.switch_to.default_content()
                continue

        # 비교: 새로운 src가 생겼는가?
        added_imgs = [src for src in new_srcs if src not in initial_srcs]
        if added_imgs:
            print(f"✅ 새 이미지 감지됨 → {len(added_imgs)}개 추가")
            img_detected = True
            break
        else:
            print(f"⏳ {elapsed}초 경과 — 아직 새 이미지 없음 ({len(new_srcs)}개 감지됨)")
            time.sleep(poll_interval)

    # 검증
    assert img_detected, "❌ AI 생성 이미지가 실제로 렌더링되지 않았습니다."
    print("✅ HelpyChat 이미지 생성 테스트 통과 — 실제 새 이미지 렌더링 확인됨")

    time.sleep(3)
