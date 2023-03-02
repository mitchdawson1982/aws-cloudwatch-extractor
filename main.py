import boto3
import time
from datetime import datetime as dt
from datetime import timedelta

from log_extractor import LogExtractor

REGION_NAME = "eu-west-2"
VPC_LOG_GROUP_NAME = "staff-device-dns-dhcp-production-vpc-flow-logs-log-group"
VPC_FILTER_STRING = "?10.180.80.5 ?10.180.81.5" # -"10.180.80" "ACCEPT OK"
PRIMARY_FILTER_LIST = ["10.180.80.5", "10.180.81.5"]
DNS_FILTER_STRING = ""
CLIENT_TYPE = "logs"
LIMIT = 10000

startTimeHuman = '2023-03-02T08:30:00.101+01:00'
endTimeHuman = '2023-03-02T09:00:00.101+01:00'
start_time = dt.strptime(startTimeHuman, '%Y-%m-%dT%H:%M:%S.%f+01:00')
end_time =dt.strptime(endTimeHuman, '%Y-%m-%dT%H:%M:%S.%f+01:00')
start_timestamp = int(start_time.timestamp()) * 1000
end_timestamp = int(end_time.timestamp()) * 1000

print(start_timestamp, end_timestamp)



def main():
       
    
    vpc = LogExtractor(
    region_name=REGION_NAME, log_group_name=VPC_LOG_GROUP_NAME,
    start_time=start_timestamp, end_time=end_timestamp, filter_list=PRIMARY_FILTER_LIST,
    limit=LIMIT, search_string=VPC_FILTER_STRING, client_type=CLIENT_TYPE
    )
    vpc.run()
    print(len(vpc.events))

 
if __name__ == "__main__":
    main()
