from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TrafficLogBase(BaseModel):
    device_id: int
    source_ip: str
    destination_ip: str
    protocol: str
    packet_count: int
    byte_count: int
    timestamp: datetime

class TrafficLogResponse(TrafficLogBase):
    id: int

    class Config:
        from_attributes = True

class TrafficLogListResponse(BaseModel):
    total: int
    items: List[TrafficLogResponse]
