import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    device_id = Column(
        UUID(as_uuid=True),
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False
    )

    alert_type = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    description = Column(String, nullable=True)

    source_ip = Column(String(50), nullable=True)
    destination_ip = Column(String(50), nullable=True)
    protocol = Column(String(20), nullable=True)

    confidence_score = Column(Float, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)

    # Relationship
    device = relationship("Device", back_populates="alerts")