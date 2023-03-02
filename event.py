from datetime import datetime
from dataclasses import dataclass

# '2 037161842252 eni-0aa48390372372729 10.89.31.75 10.180.81.5 64069 53 17 1 72 1677744004 1677744035 ACCEPT OK'
@dataclass
class Event:
    log_stream_name: str
    event_id: str
    raw_timestamp: int
    raw_ingestion_time: int
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int