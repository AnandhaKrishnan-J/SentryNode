from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

from app.db.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String, nullable=False)
    device_identifier = Column(String, unique=True, nullable=False, index=True)

    location = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)

    status = Column(String, default="offline")  # online / offline
    last_seen = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: One Device → Many Alerts
    alerts = relationship(
        "Alert",
        back_populates="device",
        cascade="all, delete"
    )

