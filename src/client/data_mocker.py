from src.util import *

# "msgKey": "zCKqaj5hES.6eRx0U",
# "msgKey": RandomString.TimeEncodedString"


def gen_random_message_key():
    return '{}.{}'.format(gen_random_string(10), encode_time(get_current_ymdhm()))


def gen_random_request_id():
    return gen_random_string(prefix='SMS', length=5)


def gen_random_client_key(req_id):
    return '{}_{}'.format(req_id, gen_random_number(4))


def gen_random_corp_id():
    return gen_random_string(prefix='COM', length=7)


def gen_random_project_id():
    return gen_random_string(prefix='PJT', length=7)


def gen_random_api_key():
    return gen_random_string(prefix='API', length=7)


def get_sub_key(d):
    msg_key = get_value(d, 'msgKey')
    if msg_key is None:
        raise KeyError('no such key({}) in d({})'.format(msg_key, d))

    split = msg_key.split('.')
    if len(split) == 2:
        return decode_time(split[1])[:10]
    return None


def get_collection_name(d):
    sub_key = get_sub_key(d)
    if sub_key is None:
        return None

    v = get_value(d, 'mongoConf')
    if v is None:
        return None

    return '{}_{}'.format(v, sub_key)


class DataMocker(object):

    def __init__(self):
        pass


    @staticmethod
    def gen_spam_halt_num_random_data(count):
        for _ in range(count):
            yield DataMocker.build_spam_halt_num_random_data()


    # 예제 CSV 1 ROW
    # 1,20240215-0000002,001,,,01012341234,,,20230801170000,20230901170000,02
    @staticmethod
    def build_spam_halt_num_random_data():

        return [
            '1',
            get_current_time_for_index(),
            '001',
            '',
            '',
            gen_random_phone_number('010', sep=''),
            '',
            '',
            get_current_time_long(),
            get_current_time_long(),
            '02'
        ]

    @staticmethod
    def gen_spam_halt_num_data(count):
        for i in range(count):
            yield DataMocker.build_spam_halt_num_data(count)


    @staticmethod
    def build_spam_halt_num_data(limit):

        return [
            '1',
            get_current_time_for_index(),
            '001',
            '',
            '',
            gen_phone_number('010', limit, sep=''),
            '',
            '',
            get_current_time_long(),
            get_current_time_long(),
            '02'
        ]


    @staticmethod
    def gen_mongo_q_data(count):
        for _ in range(count):
            for data in DataMocker.build_mongo_q_random_data():
                yield data


    @staticmethod
    def build_mongo_q_random_data():

        message_key = gen_random_message_key()

        phone_number = gen_random_phone_number('010')
        work_data = DataMocker.build_work_insert_data(message_key, phone_number)

        yield {
            "@class": "kr.co.uplus.cm.gw.model.redis.CmMongoDb$CmQMongoDto",
            "workType": "INSERT",
            "mongoConf": "CM_MSG_INFO",
            "workData": work_data,
            "msgKey": message_key,
            "ymd": None,
        }

        if coin_flip():

            work_data = DataMocker.build_work_update_data()

            yield {
                "@class": "kr.co.uplus.cm.gw.model.redis.CmMongoDb$CmQMongoDto",
                "workType": "UPDATE",
                "mongoConf": "CM_MSG_INFO",
                "workData": work_data,
                "msgKey": message_key,
                "ymd": None,
            }


    @staticmethod
    def gen_mongo_q_insert_data(count):
        for _ in range(count):
            yield DataMocker.build_mongo_q_random_insert_data()


    @staticmethod
    def gen_mongo_q_insert_data_bulk(count, batch):
        buffer = []

        for _ in range(count):
            data = DataMocker.build_mongo_q_random_insert_data()
            buffer.append(data)

            if len(buffer) == batch:
                yield buffer  # 리스트 반환
                buffer = []  # 리스트 초기화

        # 남아 있는 데이터 반환
        if buffer:
            yield buffer


    @staticmethod
    def build_mongo_q_random_insert_data():

        message_key = gen_random_message_key()

        phone_number = gen_random_phone_number('010')
        work_data = DataMocker.build_work_insert_data(message_key, phone_number)

        return {
            "@class": "kr.co.uplus.cm.gw.model.redis.CmMongoDb$CmQMongoDto",
            "workType": "INSERT",
            "mongoConf": "CM_MSG_INFO",
            "workData": work_data,
            "msgKey": message_key,
            "ymd": None,
        }


    @staticmethod
    def build_work_insert_data(message_key, phone_number):

        corp_id = gen_random_corp_id()
        project_id = gen_random_project_id()
        api_key = gen_random_api_key()
        req_id = gen_random_request_id()
        client_key = gen_random_client_key(req_id)

        ymd = get_current_ymd('-')
        full_time = get_current_full_time()
        millis = get_current_millis()

        reject_phone_number = gen_random_phone_number('080')

        sms_msg = DataMocker.build_sms_message(
            req_id,
            phone_number,
            '(광고) 광고 문자입니다. 무료수신거부 {}'.format(reject_phone_number)
        )

        return {
            "@class": "kr.co.uplus.cm.gw.model.mongo.CmMsgInfoDto",
            "msgKey": message_key,
            "corpId": corp_id,
            "projectId": project_id,
            "apiKey": api_key,
            "cliKey": client_key,
            "webReqId": req_id,
            "ymd": ymd,
            "regDt": full_time,
            "expireRegDt": [
                "java.util.Date",
                millis
            ],
            "phone": phone_number,
            "smsMsg": sms_msg,
            "payType": "PRE",
            "lineType": "NORMAL",
            "relay": None,
            "ch": "SMS",
            "campaignId": "",
            "deptCode": "",
            "senderType": "C",
            "tmpltCode": None,
            "productCode": "SMS",
            "cashId": None,
            "amount": None,
            "status": "1000",
            "spamSeq": None,
            "fbReqCnt": 0,
            "chGwKey": None,
            "extResultCode": None,
            "gwResultCode": None,
            "gwResultDesc": None,
            "cliResultCode": None,
            "inOut": None,
            "cashProcDt": None,
            "reqDt": None,
            "rptDt": None,
            "kisaOrigCode": None,
            "fbInfoLst": None,
            "msgSendHistLst": None,
            "cuid": None,
            "mmsMsg": None,
            "rcsMsg": None,
            "alimtalkMsg": None,
            "friendtalkMsg": None,
            "pushMsg": None,
            "chLst": None
        }


    @staticmethod
    def build_sms_message(req_id, callback, message):
        return {
            "@class": "kr.co.uplus.cm.gw.model.gw.api.msg.SmsMsg",
            "callback": callback,
            "msg": message,
            "webReqId": req_id,
            "clickUrlYn": "N",
            "urlIds": {
                "@class": "java.util.HashMap"
            },
            "filterYn": "N",
            "filterGrpLst": [
                "java.util.ArrayList",
                []
            ],
            "resvYn": None,
            "resvReqDt": None,
            "agency": {
                "@class": "kr.co.uplus.cm.gw.model.gw.api.msg.CommonMsg$Agency",
                "kisaOrigCode": "301150183",
                "rcsAgencyId": None,
                "rcsAgencyKey": None
            },
            "campaignId": "",
            "deptCode": "",
            "interYn": "N",
            "recvInfoLst": None,
            "fbInfoLst": None,
            "productCode": "SMS",
            "telco": None
        }


    @staticmethod
    def gen_mongo_q_update_data(count):
        for _ in range(count):
            yield DataMocker.build_mongo_q_random_update_data()


    @staticmethod
    def build_mongo_q_random_update_data():

        message_key = gen_random_message_key()

        work_data = DataMocker.build_work_update_data()

        return {
            "@class": "kr.co.uplus.cm.gw.model.redis.CmMongoDb$CmQMongoDto",
            "workType": "UPDATE",
            "mongoConf": "CM_MSG_INFO",
            "workData": work_data,
            "msgKey": message_key,
            "ymd": None,
        }

    # msgSendHistLst=[MsgSendInfo(reqDt=2024-11-15T14:27:48, rptDt=2024-11-15T14:27:49, relay=LMESSAGE, ch=ALIMTALK, resultCode=7318)
    # msgSendHistLst=[MsgSendInfo(reqDt=2024-11-14T17:49:36, rptDt=2024-11-14T17:49:38, relay=LMESSAGE, ch=FRIENDTALK, resultCode=7318)]
    # msgSendHistLst=[MsgSendInfo(reqDt=2024-11-14T14:20:48, rptDt=null, relay=LGU, ch=RCS, resultCode=24001)

    @staticmethod
    def build_work_update_data():

        req_cnt = gen_random_number(1)

        req_dt = get_current_full_time()
        rpt_dt = get_current_full_time()

        return {
            "@class": "kr.co.uplus.cm.gw.model.mongo.CmUpdMsgInfoDto",
            "fbReqCnt": req_cnt,
            "msgSendHistLst": [
                "java.util.ArrayList",
                [
                    {
                        "@class": "kr.co.uplus.cm.gw.model.mongo.MsgSendInfo",
                        "reqDt": req_dt,
                        "rptDt": rpt_dt,
                        "relay": "LMESSAGE",
                        "ch":"ALIMTALK",
                        "resultCode": 7318
                    },
                    {
                        "@class": "kr.co.uplus.cm.gw.model.mongo.MsgSendInfo",
                        "reqDt": req_dt,
                        "rptDt": rpt_dt,
                        "relay": "LMESSAGE",
                        "ch": "FRIENDTALK",
                        "resultCode": 7318
                    },
                    {
                        "@class": "kr.co.uplus.cm.gw.model.mongo.MsgSendInfo",
                        "reqDt": req_dt,
                        "rptDt": rpt_dt,
                        "relay": "LGU",
                        "ch": "RCS",
                        "resultCode": 24001
                    }
                ]
            ]
        }
