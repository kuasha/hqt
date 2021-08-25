from datetime import timezone
import datetime
from decimal import Decimal
import json


class CustomeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def get_timestamp_utc():
    return datetime.datetime.now(timezone.utc).timestamp()


def get_time_delta_utc(from_timestamp_utc):
    cur_ts_utc = get_timestamp_utc()
    return cur_ts_utc - from_timestamp_utc


def get_answer_fieldname(answer):
    return "answer-" + str(answer)


def get_resource_table_name(resource_name):
    pass
