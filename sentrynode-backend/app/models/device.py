from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)

    device_name = Column(String(100), nullable=False)
    device_identifier = Column(String(100), unique=True, nullable=False, index=True)

    location = Column(String(100), nullable=True)
    ip_address = Column(String(50), nullable=True)

    status = Column(String(20), default="offline")
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # FK FIXED
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="devices")

    alerts = relationship("Alert", back_populates="device", cascade="all, delete")
    traffic_logs = relationship("TrafficLog", back_populates="device", cascade="all, delete")
    system_metrics = relationship("SystemMetric", back_populates="device", cascade="all, delete")