from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class SystemMetric(Base):
    __tablename__ = "system_metrics"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(
        Integer,
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False
    )

    cpu_usage = Column(Float, nullable=False)
    memory_usage = Column(Float, nullable=False)
    packet_rate = Column(Float, nullable=False)
    bandwidth_usage = Column(Float, nullable=False)

    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    device = relationship("Device", back_populates="system_metrics")