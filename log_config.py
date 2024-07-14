import logging
import sys
from logging.handlers import TimedRotatingFileHandler

def get_logger(name=None):
    # 로거 이름을 지정하지 않으면 호출한 모듈의 이름을 사용
    logger = logging.getLogger(name or __name__)
    # 이미 핸들러가 설정되어 있다면 추가 설정을 하지 않음
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # 로그 포맷 설정
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # 파일 핸들러 설정 (TimedRotatingFileHandler 사용)
    file_handler = TimedRotatingFileHandler('app.log', when="midnight", interval=1)
    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y%m%d"

    # 스트림 핸들러 설정 (콘솔 출력용)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # 로거에 핸들러 추가
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger