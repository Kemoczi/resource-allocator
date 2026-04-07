from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint
from.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    device = Column(String, nullable=False)
    interface_id = Column(String, nullable=False)
    phy_speed = Column(String, nullable=False)
    optics = Column(String, nullable=False)
    assigned = Column(Boolean, nullable=False, default=False)

    __table__args = (
        UniqueConstraint("device", "interface_id", name="uq_device_interface")
    )