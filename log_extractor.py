import boto3
import json
from datetime import datetime as dt

from event import Event

class LogExtractor:
    def __init__(self,
    region_name: str, log_group_name: str, start_time: int,
    end_time: int, filter_list: list[str], limit: int = 0, client_type: str = "logs", 
    search_string: str = "") -> None:
        self.region_name = region_name
        self.log_group_name = log_group_name
        self.start_time = start_time
        self.end_time = end_time
        self.filter_list = filter_list
        self.limit = limit
        self.search_string = search_string
        self.client_type = client_type
        self.client = self.create_client()
        self.paginator = self.client.get_paginator('filter_log_events')
        self.events: list[Event] = None
    
    def create_client(self):
        return boto3.client(
            self.client_type,
            self.region_name
        )
    
    def get_events(self):
        raw_events = self.get_raw_events()
        self.events = self.convert_raw_events(raw_events)

    def get_raw_events(self) -> list[dict]:
        raw_events = []
        logs = self.get_paginated_raw_logs()
        for log in logs:
            raw_events.extend(log["events"])
            print(f"Number of events retrieved {len(raw_events)}")
        return raw_events

    def get_client_filter_events(self):
        return self.client.filter_log_events(
            logGroupName=self.log_group_name,
            startTime=self.start_time,
            endTime=self.end_time,
            filterPattern=self.search_string,
        )
    
    def convert_raw_events(self, raw_events: list[dict]) -> list[Event]:
        event_objects = []
        for raw_event in raw_events:
            event = Event(
                raw_event.get("logStreamName"),
                raw_event.get("eventId"),
                raw_event.get("timestamp"),
                raw_event.get("ingestionTime"),
                raw_event.get("message").split(" ")[3],
                raw_event.get("message").split(" ")[4],
                raw_event.get("message").split(" ")[5],
                raw_event.get("message").split(" ")[6],
            )
            event_objects.append(event)
        return event_objects

    def get_paginated_raw_logs(self) -> boto3.client:
        return self.paginator.paginate(
            logGroupName=self.log_group_name,
            startTime=self.start_time,
            endTime=self.end_time,
            filterPattern=self.search_string,
            interleaved = True,
        )

    def filter_events(self) -> list[Event]:
        filtered_events = []
        print(f"Got {len(self.events)} events for filtering")
        for event in self.events:
            if (event.src_port != 53 and event.dst_port != 53):
                continue
            else:
                print(event.src_port, event.dst_port)
                filtered_events.append(event)
        print(f"Number of events after filtering {len(filtered_events)}")
        self.events = filtered_events

    def run(self) -> None:
        self.get_events()
        self.filter_events()