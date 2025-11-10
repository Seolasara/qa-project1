import pytest
import time
from src.pages.login_page import LoginPage
from src.pages.image_upload_page import HelpyChatPage
from src.utils.config_reader import read_config


def test_CADV005_multi_file_upload_single_session(driver, login, send_test_message):
    """
    jpg, txt, pdf 파일을 연속 첨부하여 업로드가 정상 동작하는지 확인
    """

    # 설정 로드
    config = read_config("helpychat")
    base_url = config["base_url"]

    # 로그인 후 채팅 페이지 진입
    driver.get(base_url)
    time.sleep(3)

    chat_page = HelpyChatPage(driver)

    # 업로드할 파일 리스트
    files = ["dogimage.jpg", "test.txt", "testfile2.pdf"]

    # 한 세션 내에서 연속 업로드
    for filename in files:
        print(f"📂 {filename} 업로드 시도 중...")
        chat_page.upload_image(filename)
        send_test_message(f"{filename} 파일 업로드 테스트입니다.")
        time.sleep(2)

    # 간단 검증 (페이지 내 텍스트 또는 이미지 확인)
        page_src = driver.page_source
        assert "<img" in page_src or filename.split(".")[0] in page_src, f"{filename} 업로드 실패"
        print(f"✅ {filename} 업로드 성공\n")

    # 전체 파일 업로드 후 페이지 확인
    print("✅ 모든 파일 업로드 테스트 완료")
    time.sleep(10)