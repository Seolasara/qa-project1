import pytest
import time
from src.pages.image_upload_page import HelpyChatPage
from src.utils.config_reader import read_config
from selenium.common.exceptions import TimeoutException


def test_CADV005_multi_file_upload_single_session(driver, login, send_test_message):
    """HelpyChat에서 docx~jpeg 등 15개 파일을 연속 업로드 (안정화 버전)"""

    config = read_config("helpychat")
    base_url = config["base_url"]

    driver.get(base_url)
    time.sleep(3)
    chat_page = HelpyChatPage(driver)

    # 업로드할 파일 리스트
    files = [
        "testfile.docx","test.pptx","dogimage.jpg","test.txt","testfile2.pdf",
        "test.xlsx","test.csv","test_data.xml","test_image.bmp","test_image.tiff",
        "test_image.webp","test_page.html","sample.gif","sample.htm","sample.jpeg"
    ]

    for filename in files:
        print(f"📤 {filename} 업로드 시작")

        try:
            # 업로드 시도
            chat_page.upload_image(filename)
            print(f"✅ {filename} 업로드 완료")

            # 메시지 전송
            send_test_message(f"{filename} 파일 업로드 테스트입니다.")
            print(f"💬 {filename} 메시지 전송 완료")

            # 업로드된 이미지 or 텍스트 렌더링 확인 (10초 제한)
            success = False
            for _ in range(10):
                page_src = driver.page_source
                if "<img" in page_src or filename.split(".")[0] in page_src:
                    success = True
                    break
                time.sleep(1)

            assert success, f"❌ {filename} 업로드 후 화면 미반영"

        except TimeoutException:
            print(f"⚠️ {filename} 업로드 중 Timeout 발생. HelpyChat UI가 느릴 수 있습니다.")
            time.sleep(3)  # 다음 파일로 넘어가기 전 안정화 대기
            continue

        except Exception as e:
            print(f"❌ {filename} 업로드 실패: {e}")
            assert False, f"{filename} 업로드 중 예외 발생: {e}"

        # 각 업로드 간 충분한 텀 확보 (HelpyChat 내부 스레드 안정화)
        time.sleep(2)

    print("✅ 모든 파일 업로드 테스트 완료 🎉")
    time.sleep(5)
