from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
    ForeignKey,
)

from ...database import Base


class NDCModel(Base):
    __tablename__ = "ndc"

    id = Column(Integer, primary_key=True)
    spl_id = Column(String(128), nullable=False)
    appl_no = Column(String(128), nullable=False)
    appl_type = Column(String(128), nullable=False)
    spl_set_id = Column(String(128), nullable=True)
    product_ndc = Column(String(128), nullable=True, index=True)
    route = Column(String(128), nullable=True, index=True)
    dosage_form = Column(String(128), nullable=True)
    generic_name = Column(String(128), nullable=True)
    labeler_name = Column(String(128), nullable=True)
    labeler_subsidiary_id = Column(
        Integer, ForeignKey("subsidiaries.id"), nullable=True,
    )
    brand_name = Column(String(128), nullable=True)
    marketing_category = Column(String(128), nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    __table_args__ = (UniqueConstraint("spl_id", "product_ndc",),)
