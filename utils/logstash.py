import logging, logstash, re


def create_logger(logger_name):
    logger = logging.getLogger(logger_name)
    if len(logger.handlers) > 0:  # 로거가 이미 존재하는 경우
        return logger

    logger.setLevel(logging.DEBUG)
    log_format = logging.Formatter('\n[%(levelname)s|%(name)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    # 콘솔 스트림, 로그 파일 생성
    console = logging.StreamHandler()
    # file_handler = logging.FileHandler(filename='./test_elk.log')

    # handler 별로 다른 level 설정
    console.setLevel(logging.INFO)
    # file_handler.setLevel(logging.DEBUG)

    # handler 출력 format 지정
    console.setFormatter(log_format)
    # file_handler.setFormatter(log_format)

    # logger에 handler 추가
    logger.addHandler(console)
    # logger.addHandler(file_handler)

    # logstash에 TCP로 전송하는 핸들러
    # stash = logstash.TCPLogstashHandler('{host}', 5044, version=1)
    # stash.setFormatter(log_format)
    # logger.addHandler(stash)
    logger.addHandler(logstash.TCPLogstashHandler('localhost', 5044, version=1))

    return logger