from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime

def datetime_to_proto(dt: datetime) -> Timestamp:
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts

def proto_to_datetime(ts: Timestamp) -> datetime:
    return ts.ToDatetime()
