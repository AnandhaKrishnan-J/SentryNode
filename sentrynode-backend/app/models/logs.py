from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class TrafficLog(Base):
    __tablename__ = "traffic_logs"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(
        Integer,
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False
    )

    source_ip = Column(String(50), nullable=False)
    destination_ip = Column(String(50), nullable=False)
    protocol = Column(String(20), nullable=False)

    packet_count = Column(Integer, nullable=False)
    byte_count = Column(Integer, nullable=False)

    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    device = relationship("Device", back_populates="traffic_logs")