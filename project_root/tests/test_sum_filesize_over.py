import pytest
import time
from pathlib import Path
from src.pages.image_upload_page import HelpyChatPage
from src.utils.config_reader import read_config


def test_CADV0013_sequential_add_files_single_message(driver, login, send_test_message):
    """
    ✅ 로그인 후 채팅창을 한 번만 열고
    jpg 파일 3개를 하나씩 순차 첨부 후, 한 메시지로 전송하는 테스트
    """

    # 설정 로드
    config = read_config("helpychat")
    base_url = config["base_url"]

    # 로그인 후 채팅 페이지 진입
    driver.get(base_url)
    time.sleep(3)

    chat_page = HelpyChatPage(driver)

    # 업로드할 파일 리스트
    files = ["18mb.jpg", "6.05mb.jpg"]

    # 파일 2개를 하나씩 첨부 버튼으로 추가
    for filename in files:
        chat_page.upload_image(filename)
        time.sleep(1)

    # 모든 파일 첨부 후 메시지 전송
    send_test_message("합쳐서 20mb 이상인 파일 두 개 첨부 테스트")

    # 업로드 확인
    time.sleep(5)
    page_src = driver.page_source
    for filename in files:
        assert "<img" in page_src or filename.split(".")[0] in page_src, f"{filename} 업로드 실패"
        print(f"✅ {filename} 업로드 확인 완료")

    print("✅ 두 파일 첨부 및 메시지 전송 완료")
    time.sleep(5)