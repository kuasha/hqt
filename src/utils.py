from datetime import timezone
import datetime


def get_timestamp_utc():
    return datetime.datetime.now(timezone.utc).timestamp()


def get_time_delta_utc(from_timestamp_utc):
    cur_ts_utc = get_timestamp_utc()
    return cur_ts_utc - from_timestamp_utc
