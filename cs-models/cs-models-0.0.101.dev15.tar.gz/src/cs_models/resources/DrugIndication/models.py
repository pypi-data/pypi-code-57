from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from ...database import Base


class DrugIndicationModel(Base):
    __tablename__ = "drug_indications"

    id = Column(Integer, primary_key=True)
    set_id = Column(String(128), nullable=False, index=True)
    lowercase_indication = Column(String(128), nullable=False, index=True)
    indication = Column(String(128), nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
