from sqlalchemy.orm import Session
from app.models.logs import TrafficLog
from app.models.user import User

def list_traffic_logs(db: Session, current_user: User, limit: int = 100, offset: int = 0):
    # Depending on requirements, we might filter logs by devices owned by current_user
    # For now, let's fetch all (assuming admin access or global view as implemented in other services)
    
    query = db.query(TrafficLog)
    total = query.count()
    logs = query.order_by(TrafficLog.timestamp.desc()).offset(offset).limit(limit).all()
    
    return total, logs
