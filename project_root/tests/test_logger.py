import logging
import time

def test_example():
    logging.info("테스트 시작")
    time.sleep(1)
    logging.debug("중간 단계: sleep 완료")
    logging.warning("경고 메시지 예시")
    logging.error("에러 메시지 예시")
    logging.info("테스트 종료")