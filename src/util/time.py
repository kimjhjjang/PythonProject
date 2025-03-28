import time
from datetime import datetime, timedelta


# 현재 시간을 "yyyyMMddHHmm" 형식의 문자열로 변환
def get_current_ymdhm():
    return datetime.now().strftime("%Y%m%d%H%M")


def get_formatted_ymd(dt, glue=''):
    return dt.strftime('{}'.format(glue).join(['%Y', '%m', '%d']))


def get_current_ymd(glue=''):
    return get_formatted_ymd(datetime.now(), glue)


def get_elapsed_ymd(days, glue=''):
    dt = datetime.now()
    dt += timedelta(days=days)
    return get_formatted_ymd(dt, glue)


def get_current_full_time():
    # 현재 시간을 "yyyy-MM-ddTHH:mm:ss" 형식으로 변환
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def get_current_time_for_index():
    # 현재 시간을 "yyyyMMdd-HHmmss" 형식으로 변환
    return '{}0'.format(datetime.now().strftime("%Y%m%d-%H%M%S"))


def get_current_time_long():
    """
    시간을 'YYYYMMDDHHMMSS' 형식의 문자열로 변환합니다.
    :param input_time: datetime 객체 (기본값: 현재 시간)
    :return: 문자열로 변환된 시간 (예: '20230801170000')
    """
    return datetime.now().strftime('%Y%m%d%H%M%S')


def get_current_millis():
    return int(time.time() * 1000)


def gen_ymdh(from_dt, to_dt):
    # 문자열을 datetime 객체로 변환
    start = datetime.strptime(from_dt, '%Y-%m-%d')
    end = datetime.strptime(to_dt, '%Y-%m-%d')

    # 1시간씩 증가하면서 'YYYYMMDDHH' 형식의 문자열 생성
    while start < end:
        yield start.strftime('%Y%m%d%H')
        start += timedelta(hours=1)


class Timer(object):

    count = 0
    time = 0.0

    def __init__(self):
        pass


    def measure(self, count, st, et):
        if count:
            self.count += count
            self.time += (et-st)


    def __str__(self):
        #print(f"Elapsed time: {elapsed_time:.6f} seconds")
        return f"COUNT : {self.count}, ELAPSED TIME : {self.time:.3f} SECONDS"
