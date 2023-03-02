import boto3
import time
from datetime import datetime as dt
from datetime import timedelta

from log_extractor import LogExtractor

REGION = ""
LOG_GROUP_NAME = ""
SEARCH_STRING = ""
CLIENT_TYPE = "logs"
LIMIT = 10000

startTimeHuman = '2023-03-02T08:30:00.101+01:00'
endTimeHuman = '2023-03-02T09:00:00.101+01:00'
start_time = dt.strptime(startTimeHuman, '%Y-%m-%dT%H:%M:%S.%f+01:00')
end_time =dt.strptime(endTimeHuman, '%Y-%m-%dT%H:%M:%S.%f+01:00')
start_timestamp = int(start_time.timestamp()) * 1000
end_timestamp = int(end_time.timestamp()) * 1000


def main():
       
    
    vpc = LogExtractor(
    region_name=REGION, log_group_name=LOG_GROUP_NAME,
    start_time=start_timestamp, end_time=end_timestamp,
    limit=LIMIT, search_string=SEARCH_STRING, client_type=CLIENT_TYPE
    )
    vpc.run()
    print(len(vpc.events))

 
if __name__ == "__main__":
    main()
