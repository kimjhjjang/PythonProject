import logging

from logging.handlers import RotatingFileHandler
from src.util import gen_random_string


def setup_logging(log_name):

    if not log_name:
        log_name = gen_random_string(10)

    # 로거 생성
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 파일 핸들러
    #file_handler = logging.FileHandler("./logs/{}.log".format(log_name))
    #file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    #file_handler.setFormatter(file_formatter)
    
    # 파일 로테이션 핸들러
    rotating_handler = RotatingFileHandler("./logs/{}.log".format(log_name), maxBytes=50000000, backupCount=10)
    rotating_handler.setFormatter(formatter)

    # 핸들러 추가
    logger.addHandler(console_handler)
    logger.addHandler(rotating_handler)
